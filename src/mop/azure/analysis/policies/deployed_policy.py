import datetime
import json
import os
import uuid
from configparser import ConfigParser

import jmespath
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker
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


    def summarize_policy_defintions_for_all_management_grp(self, management_group_id, metadata_category=None):
        """
        This aggregrates all the policy definitions at the management group level an places them in a table
        :param policy_definition_name:
        """

        batch_uuid = uuid.uuid4()
        created = datetime.datetime.utcnow()

        # create a configured "Session" class

        # create a Session
        # Execute returns a method the can be executed anywhere more than once
        policy_definition_cls = PolicyDefinition()

        models = self.get_db_model(self.engine)
        subscriptions_model = models.classes.subscriptions
        policy_definition_model = models.classes.policydefinitions

        session = self.Session()
        subscriptions = session.query(subscriptions_model).all()

        policy_definitions_response = policy_definition_cls.get_policy_definitions_list_by_management_group(management_group_id)
        if policy_definitions_response.status_code in range(200, 299):
            policy_definitions_list = policy_definitions_response.json()['value']

            for policy_definition in policy_definitions_list:
                category, displayName, policyType, description = ""

                policyDefinitionName = policy_definition['name']
                policy_id = policy_definition['id']
                if 'metadata' in policy_definition['properties'] and 'category' in policy_definition['properties']['metadata']:
                    category = policy_definition['properties']['metadata']['category']

                if 'displayName' in policy_definition['properties']:
                    displayName = policy_definition['properties']['displayName']

                if 'policyType' in policy_definition['properties']:
                    policyType = policy_definition['properties']['policyType']

                if 'description' in policy_definition['properties']:
                    description = policy_definition['properties']['description']

        #TODO finish this code
