import datetime
import json
import os
import uuid

import sys
import logging

from azure.cosmos import CosmosClient
from configparser import ConfigParser

# Create a logger for the 'azure' SDK
logger = logging.getLogger('azure')
logger.setLevel(logging.DEBUG)

# Configure a console output
handler = logging.StreamHandler(stream=sys.stdout)
logger.addHandler(handler)


import jmespath
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker

from azure.cosmos import CosmosClient, PartitionKey, exceptions
from mop.azure.analysis.policy_compliance import PolicyCompliance
from mop.azure.comprehension.operations.policy_states import PolicyStates
from mop.azure.comprehension.resource_management.policy_definitions import PolicyDefinition
from mop.azure.comprehension.operations.policy_insights2 import PolicyInsights2
from mop.framework.azure_connections import request_authenticated_azure_session
from mop.azure.utils.create_configuration import CONFVARIABLES, change_dir, OPERATIONSPATH
from mop.db.basedb import BaseDb


class SummaryForPolicyDefinition(BaseDb):

    def __init__(self, db_server_instance="instance01"):
        load_dotenv()
        with change_dir(OPERATIONSPATH):
            self.config = ConfigParser()
            self.config.read(CONFVARIABLES)

        sql_instance = self.config['SQLSERVER'][db_server_instance]
        sql_instance = json.loads(sql_instance.replace("\'", "\""))
        self.server = sql_instance['server']
        self.database = sql_instance['database']
        self.username = sql_instance['username']
        self.driver = sql_instance['db_driver']
        self.dialect = sql_instance['dialect']

        self.password = os.environ['DATABASEPWD']

        self.get_db_engine()
        self.Session = sessionmaker(bind=self.engine)

        url = self.config['COSMOSDB']['uri_01']
        key = os.environ['COSMODB_KEY']

        self.CosmosDBclient = CosmosClient(url, credential=key)

    def summarize_fact_compliance_for_definition(self, subscription_id, policy_definition_name):

        jmespath_expression = jmespath.compile("value[*].policyAssignments[*].policyDefinitions[*]")
        policy_states = PolicyStates()
        batch_uuid = uuid.uuid4()
        created = datetime.datetime.utcnow()

        # create a configured "Session" class

        # create a Session
        # Execute returns a method the can be executed anywhere more than once
        models = self.get_db_model(self.engine)
        FactCompliance = models.classes.factcompliance
        subscriptions = models.classes.subscriptions

        session = self.Session()
        if subscription_id is not None:
            subscriptions_list = session.query(subscriptions).filter_by(subscription_id=subscription_id)
        else:
            subscriptions_list = session.query(subscriptions).all()

        for subscription in subscriptions_list:
            tenant_id = subscription.tenant_id
            print("Subscription: {}, Policy Name {}".format(subscription.subscription_id, policy_definition_name))
            policy_states_of_definition = policy_states.policy_states_summarize_for_policy_definition(
                subscriptionId=subscription.subscription_id,
                policyDefinitionName=policy_definition_name).json()

            jmes_result = jmespath_expression.search(policy_states_of_definition)

            if jmespath_expression is None or jmes_result is None or jmes_result[0] is None or len(jmes_result[0]) == 0:
                continue
            else:
                # flatten results
                policyresults = jmes_result[0][0]
                bulk_insert = list()
                for policyresult in policyresults:
                    policy_definition_name = str(policyresult['policyDefinitionId']).split('/')[-1]
                    resourceDetails = jmespath.search('results.resourceDetails[*]', policyresult)

                    compliance_ratio = self.determine_compliance_ratio(resourceDetails)

                    fact = FactCompliance(
                        tenant_id=tenant_id,
                        subscription_id=subscription.subscription_id,
                        policy_definition_name=policy_definition_name,
                        compliant=compliance_ratio['compliant'],
                        noncompliant=compliance_ratio['noncompliant'],
                        total_resources_measured=compliance_ratio['total_resources_measured'],
                        percent_compliant=compliance_ratio['percent_compliant'],
                        batch_uuid=batch_uuid,
                        created=created,
                        modified=created)
                    bulk_insert.append(fact)

                session.bulk_save_objects(bulk_insert)
                session.commit()

    def summarize_policy_defintions_for_all_management_grp(self, management_group_id, policy_definition_name_like,
                                                           metadata_category):
        """
        This method take the policy definition and find the statistics and saves it to the fact table
        Submit a policy definition name without a wild card to pull back a single policy definition name
        :param policy_definition_name:
        """

        batch_uuid = uuid.uuid4()
        created = datetime.datetime.utcnow()

        database_name = 'policyinsights'
        comsos_database = self.get_cosmodb(database_name)

        container_name = 'policydefintionresults'
        partition_key = "/{}".format(metadata_category.strip().lower().replace(' ', ''))
        self.cosmos_container_client = self.get_cosmosdb_container(container_name, comsos_database, partition_key)

        # create a configured "Session" class

        # create a Session
        # Execute returns a method the can be executed anywhere more than once
        policy_definition_cls = PolicyDefinition()

        models = self.get_db_model(self.engine)
        subscriptions_model = models.classes.subscriptions
        policy_definition_model = models.classes.policydefinitions

        session = self.Session()
        subscriptions = session.query(subscriptions_model).all()
        policies = session.query(policy_definition_model).filter(
            policy_definition_model.metadata_category == metadata_category,
            policy_definition_model.policy_definition_name.like('security-pol-%')).all()

        policy_compliance = PolicyCompliance()

        for subscription in subscriptions:
            for policy_definition in policies:
                self.summarize_fact_compliance_for_definition(category=metadata_category,
                                                              policy_definition_name=policy_definition.policy_definition_name,
                                                              tenant_id=subscription.tenant_id,
                                                              subscription_id=subscription.subscription_id,
                                                              batch_uuid=batch_uuid)

    def summarize_fact_compliance_for_definition(self, category, policy_definition_name, tenant_id, subscription_id,
                                                 batch_uuid):
        """
        This method captures the results for a policy compliance within a single subscription
        publishes results to non-SQL Cosmos DB
        :param category:
        :param policy_definition_name:
        :param subscription_id:
        """
        policy_states = PolicyStates()

        created = datetime.datetime.utcnow()

        # create a configured "Session" class
        print("Subscription: {}, Policy Name {}".format(subscription_id, policy_definition_name))

        '''
        Retreive the states for a policy and subscription
        '''
        policy_states_of_definition_response = policy_states.policy_states_summarize_for_policy_definition(
            subscriptionId=subscription_id,
            policyDefinitionName=policy_definition_name)
        '''
        The Rest API may fail to pull back states for many reasons.
        Failed states are skipped for various reasons but mostly, some results are better than none
        You are free to act differently.
        '''
        if not policy_states_of_definition_response.status_code in range(200, 299):
            print("Skipping with Error {} Subscription: {}, Policy Name {}".format(
                policy_states_of_definition_response.status_code, subscription_id,
                policy_definition_name))
            return

        policy_states_of_definitions_json = policy_states_of_definition_response.json()

        if 'value' in policy_states_of_definitions_json:
            policy_states_of_definitions = policy_states_of_definitions_json['value']
            for policy_states_of_definition in policy_states_of_definitions:
                policy_states_of_definition['category'] = category
                policy_states_of_definition['policy_definition_name'] = policy_definition_name
                policy_states_of_definition['tenant_id'] = tenant_id
                policy_states_of_definition['subscription_id'] = subscription_id
                policy_states_of_definition['batch_uuid'] = str(batch_uuid)

                self.cosmos_container_client.upsert_item(policy_states_of_definition)
        else:
            return 0

    def get_cosmosdb_container(self, container_name, database, partition_key):
        container = None
        try:
            container = database.create_container(id=container_name,
                                                  partition_key=PartitionKey(path=partition_key))
        except exceptions.CosmosResourceExistsError:
            container = database.get_container_client(container_name)
        except exceptions.CosmosHttpResponseError:
            raise
        finally:
            if container is not None:
                return container

    def get_cosmodb(self, database_name):
        try:
            database = self.CosmosDBclient.create_database(database_name)
        except exceptions.CosmosResourceExistsError:
            database = self.CosmosDBclient.get_database_client(database_name)
        return database

    def determine_compliance_ratio(self, resourceDetails):

        compliance_dict = dict()
        if len(resourceDetails) <= 2:
            complianceState = resourceDetails[0]
            if complianceState['complianceState'] in 'compliant':
                compliance_dict["compliant"] = int(complianceState["count"])
            else:
                compliance_dict["noncompliant"] = int(complianceState["count"])
        if len(resourceDetails) == 2:
            complianceState = resourceDetails[1]
            if complianceState['complianceState'] in 'compliant':
                compliance_dict["compliant"] = int(complianceState["count"])
            else:
                compliance_dict["noncompliant"] = int(complianceState["count"])
        if not 'compliant' in compliance_dict:
            compliance_dict["compliant"] = 0
        if not 'noncompliant' in compliance_dict:
            compliance_dict['noncompliant'] = 0

        compliance_dict['total_resources_measured'] = compliance_dict["compliant"] + compliance_dict['noncompliant']
        compliance_dict['percent_compliant'] = compliance_dict["compliant"] / compliance_dict[
            'total_resources_measured'] * 100

        return compliance_dict
