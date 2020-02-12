import datetime
import json
import os
import uuid
from configparser import ConfigParser

import jmespath
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker

from mop.azure.comprehension.operations.policy_states import PolicyStates
from mop.azure.comprehension.resource_management.policy_definitions import PolicyDefinition
from mop.azure.connections import request_authenticated_session
from mop.azure.utils.create_configuration import CONFVARIABLES, change_dir, OPERATIONSPATH
from mop.db.basedb import BaseDb


class PolicyCompliance(BaseDb):

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

    def reduce_policy_definition_list(self, subscription_list, metadata_category=None,
                                      include=['BuiltIn', 'Static', 'Custom']):
        models = self.get_db_model(self.engine)
        DimPolicies = models.classes.policydefinitions

        session = self.Session()
        pf = session.query(DimPolicies).all()

        policies_found = list()
        for row in pf:
            policies_found.append(row.policy_definition_name)

        bulk_insert = list()

        policy_definitions = PolicyDefinition()
        for subscription_item in subscription_list:

            response = policy_definitions.policy_definitions_by_subscription_req(subscription_item)

            results = response.json()
            policies = results['value']
            for policy in policies:

                policy_type = policy['properties']['policyType']

                if policy_type in include:
                    policy_name = policy['name']
                    policy_category = ""
                    if 'category' in policy['properties']['metadata']:
                        policy_category = policy['properties']['metadata']['category']

                        if metadata_category is not None and \
                            'category' in policy['properties']['metadata'] and \
                            metadata_category in policy_category:
                            if 'description' in policy['properties']:
                                policy_description = policy['properties']['description']
                            else:
                                policy_description = policy['properties']['displayName']
                            print(policy['name'])
                            policy = DimPolicies(policy_definition_name=policy['name'],
                                                 policy_description=policy_description,
                                                 policy_display_name=policy['properties']['displayName'],
                                                 policy_type=policy['properties']['policyType'],
                                                 metadata_category=policy['properties']['metadata']['category'])

                            policies_found.append(policy.policy_definition_name)
                            bulk_insert.append(policy)
                        else:
                            NotImplementedError

            session.bulk_save_objects(bulk_insert)
            session.commit()

    def compile_sci(self):

        management_grp = self.config['DEFAULT']['management_grp_id']
        models = self.get_db_model(self.engine)
        FactCompliance = models.classes.factcompliance
        DimPolicies = models.classes.policydefinitions
        CompiledSCI = models.classes.compiled_sci
        Subscription = models.classes.subscriptions

        session = self.Session()
        utc = datetime.datetime.utcnow()
        batch_uuid = uuid.uuid4()

        join_query = session.query(FactCompliance, DimPolicies, Subscription).join(DimPolicies,
                                                                                   FactCompliance.policy_definition_name == DimPolicies.policy_definition_name).outerjoin(
            Subscription, FactCompliance.subscription_id == Subscription.subscription_id)

        results = join_query.all()
        bulk_insert = list()

        for row in results:
            compiled_sci = CompiledSCI(
                tenant_id=row.factcompliance.tenant_id,
                management_grp=management_grp,
                subscription_id=row.factcompliance.subscription_id,
                subscription_display_name=row.subscriptions.subscription_display_name,
                policy_metadata_category=row.policydefinitions.metadata_category,
                policy_definition_name=row.factcompliance.policy_definition_name,
                policy_display_name=row.policydefinitions.policy_display_name,
                policy_description=row.policydefinitions.policy_description,
                policy_definition_id=row.factcompliance.policy_definition_id,
                policy_compliant_resources=row.factcompliance.compliant,
                policy_noncompliant_resources=row.factcompliance.noncompliant,
                total_resources_measured=row.factcompliance.total_resources_measured,
                percent_in_compliance=row.factcompliance.percent_compliant,
                created=utc,
                batch_uuid=batch_uuid
            )

            bulk_insert.append(compiled_sci)

        session.bulk_save_objects(bulk_insert)
        session.commit()

    def save_subscription_policies_by_category(self, category, subscription_id=None):

        policy_definitions = PolicyDefinition()

        # create a configured "Session" class

        # create a Session
        session = Session()
        # Execute returns a method the can be executed anywhere more than once
        models = self.get_db_model(self.engine)
        subscriptions = models.classes.subscriptions
        DimPolicies = models.classes.policydefinitions

        session = self.Session()
        results = session.query(subscriptions).all()

        bulk_insert = list()
        batch_uuid = uuid.uuid4()


        created = datetime.datetime.utcnow()

        try:

            for row in results:

                policy_definition_list = policy_definitions.list_subscription_policy_definition_by_category(
                    subscriptionId=row.subscription_id,
                    category=category)
                if policy_definition_list is None:
                    continue

                for policy in policy_definition_list:

                    policy['name']
                    if policy:
                        displayName = policy['properties']['displayName']
                        if 'description' in policy['properties']:
                            description = policy['properties']['description']
                        else:
                            description = policy['properties']['displayName']
                        policyType = policy['properties']['policyType']
                        if 'category' in policy['properties']['metadata']:
                            category = policy['properties']['metadata']['category']
                        else:
                            category = ''

                        policy = DimPolicies(policy_definition_name=policy['name'],
                                             policy_description=description,
                                             policy_display_name=displayName,
                                             policy_type=policyType,
                                             subscriptionid=row.subscription_id,
                                             metadata_category=category,
                                             created=created,
                                             modified=created,
                                             batch_uuid=batch_uuid)

                        bulk_insert.append(policy)

        finally:
            session.bulk_save_objects(bulk_insert)
            session.commit()

    def summarize_fact_compliance(self, category, subscription_id=None):

        policy_states = PolicyStates()
        # create a configured "Session" class

        # create a Session
        # Execute returns a method the can be executed anywhere more than once
        models = self.get_db_model(self.engine)
        FactCompliance = models.classes.factcompliance
        DimPolicies = models.classes.policydefinitions
        subscriptions = models.classes.subscriptions
        session = self.Session()

        session = self.Session()
        if subscription_id is not None:
            subscriptions_list = session.query(subscriptions).filter_by(subscription_id=subscription_id)
        else:
            subscriptions_list = session.query(subscriptions).all()

        jmespath_expression = jmespath.compile("value[*]")

        for subscription in subscriptions_list:
            tenant_id = subscription.tenant_id
            subscription_id = subscription.subscription_id
            subcription_policies = session.query(DimPolicies).filter(DimPolicies.subscriptionid == subscription_id)

            print(subscription_id)
            if subcription_policies:
                for sub_policy in subcription_policies:
                    policy_states_of_definition = policy_states.policy_states_summarize_for_policy_definition(
                        subscriptionId=subscription_id,
                        policyDefinitionName=sub_policy.policy_definition_name).json()

                    if 'value' in policy_states_of_definition:
                        values = policy_states_of_definition['value']
                        for value in values:
                            if 'results' in  value:
                                policy_state_results = value['results']

                                if "resourceDetails" in policy_state_results:
                                    resourceDetails = policy_state_results["resourceDetails"]
                                    if resourceDetails is not None and len(resourceDetails) > 0:
                                        print("resourceDetails found!")
                                    else:
                                        print("resourceDetails not found")
                                if "policyDetails" in policy_state_results:
                                    policyDetails = policy_state_results["policyDetails"]
                                    if policyDetails is not None and len(policyDetails) > 0:
                                        print("policyDetails found!")
                                    else:
                                        print("policyDetails not found")
                                if 'policyAssignments' in policy_states_of_definition['value']:
                                    policyAssignments_list = policy_states_of_definition['value']['policyAssignments']

                                    if policyAssignments_list is not None and len(policyAssignments_list) > 0:
                                        print("policyAssignments found!")
                                    else:
                                        print("policyAssignments not found")

    def summarize_query_results_for_policy_definitions(self):
        """
        Compiles statistics concerning policy definitions using existing records in the factcompliance
        :return:
        """

        models = self.get_db_model(self.engine)
        FactCompliance = models.classes.factcompliance
        DimPolicies = models.classes.policydefinitions

        session = self.Session()
        results = session.query(FactCompliance).all()
        pf = session.query(DimPolicies).all()

        policies_found = list()
        for row in pf:
            policies_found.append(row.policy_definition_name)

        bulk_insert = list()

        try:

            for row in results:
                print(row.subscription_id, row.policy_definition_name)
                if row.policy_definition_name not in policies_found:
                    with request_authenticated_session() as req:
                        policy = PolicyDefinition().get_policy_definitions(row.subscription_id,
                                                                           row.policy_definition_name, req)
                        if policy:
                            policy_defintion = policy()
                        else:
                            if row.policy_definition_id:
                                policy = PolicyDefinition().policy_definition_via_policyDefinitionId(
                                    row.policy_definition_id)
                                policy_defintion = policy.json()

                        if policy:
                            displayName = policy_defintion['properties']['displayName']
                            if 'description' in policy_defintion['properties']:
                                description = policy_defintion['properties']['description']
                            else:
                                description = policy_defintion['properties']['displayName']
                            policyType = policy_defintion['properties']['policyType']
                            if 'category' in policy_defintion['properties']['metadata']:
                                category = policy_defintion['properties']['metadata']['category']
                            else:
                                category = ''
                            print(displayName)
                            policy = DimPolicies(policy_definition_name=row.policy_definition_name,
                                                 policy_description=description,
                                                 policy_display_name=displayName,
                                                 policy_type=policyType,
                                                 metadata_category=category)

                            policies_found.append(policy.policy_definition_name)
                            bulk_insert.append(policy)
        finally:
            session.bulk_save_objects(bulk_insert)
            session.commit()

    def summarize_subscriptions(self, tenant_id, management_grp):
        # create a configured "Session" class

        # create a Session
        session = Session()
        # Execute returns a method the can be executed anywhere more than once
        models = self.get_db_model(self.engine)
        subscriptions = models.classes.subscriptions
        FactCompliance = models.classes.factcompliance
        session = self.Session()
        results = session.query(subscriptions).all()

        for row in results:
            print(row.subscription_display_name)
            if row.subscription_id:
                df = subscription_policy_compliance(row.subscription_id)
                if df is None: continue
                bulk_insert = list()
                for index, dfrow in df.iterrows():
                    fact = FactCompliance(
                        tenant_id=tenant_id,
                        subscription_id=row.subscription_id,
                        policy_definition_name=dfrow['policy_definition_name'],
                        policy_definition_id=dfrow['policy_definition_id'],
                        compliant=dfrow['compliant'],
                        noncompliant=dfrow['noncompliant'],
                        total_resources_measured=dfrow['total_resources_measured'],
                        percent_compliant=dfrow['percent_compliant'])
                    bulk_insert.append(fact)
                session.bulk_save_objects(bulk_insert)
                session.commit()


def determine_compliance_ratio(resourceDetails):
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


def subscription_policy_compliance(subscriptionId):
    with change_dir(OPERATIONSPATH):
        config = ConfigParser()
        config.read(CONFVARIABLES)

    jmespath_expression = jmespath.compile("value[*].policyAssignments[*].policyDefinitions[*]")
    jmespath_results = jmespath.compile("[0].results.resourceDetails")
    scour_policy = PolicyStates()
    response = scour_policy.policy_states_summarize_for_subscription(subscriptionId)
    if response is None:
        response = scour_policy.policy_states_summarize_for_subscription(subscriptionId)

    # Execute returns a method the can be executed anywhere more than once
    result = response.json()
    df = pd.DataFrame(columns=['subscription_id',
                               'policy_definition_name',
                               'policy_definition_id',
                               'compliant',
                               'noncompliant',
                               'total_resources_measured',
                               'percent_compliant'])
    jmes_result = jmespath_expression.search(result)

    if jmespath_expression is None or jmes_result is None or jmes_result[0] is None:
        return
    else:
        # flatten results
        try:

            policyresults = jmes_result[0][0]
            for policyresult in policyresults:
                policy_definition_name = str(policyresult['policyDefinitionId']).split('/')[-1]
                resourceDetails = jmespath.search('results.resourceDetails[*]', policyresult)

                compliance_ratio = determine_compliance_ratio(resourceDetails)
                new_row = {'subscription_id': subscriptionId,
                           'policy_definition_name': policy_definition_name,
                           'policy_definition_id': policyresult['policyDefinitionId'],
                           'compliant': compliance_ratio['compliant'],
                           'noncompliant': compliance_ratio['noncompliant'],
                           'total_resources_measured': compliance_ratio['total_resources_measured'],
                           'percent_compliant': compliance_ratio['percent_compliant'],
                           }

                df = df.append(new_row, ignore_index=True)

        except IndexError:
            return None

    return df
