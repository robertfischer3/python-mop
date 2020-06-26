import datetime
import json
import os
import uuid
from configparser import ConfigParser
import aiohttp
import asyncio
from aiohttp import ClientSession

import jmespath

from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker

from mop.azure.analysis.baseline.aggregate_sql_subscriptions import AggregateSQLSubscriptions
from mop.azure.comprehension.resource_management.policy_assignments import PolicyAssignments
from mop.azure.comprehension.resource_management.policy_definitions import PolicyDefinition
from mop.azure.utils.create_configuration import CONFVARIABLES, change_dir, OPERATIONSPATH
from mop.db.basedb import BaseDb


class ProcessAssignments(BaseDb):

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

    def create_policy_assignment_with_management_group_policy(self, management_grp_id, policy_definition_body,
                                                              subcription_id):
        policy_assignment = PolicyAssignments()
        if 'name' in policy_definition_body:
            policyDefinitionName = policy_definition_body['name']
        else:
            self.assertTrue(False, msg="Policy Definition Name not found")

        if policyDefinitionName:
            policy_assignment_response = policy_assignment.create_management_group_policy_assignment_at_subscription_level(
                managementGroupId=management_grp_id,
                subscriptionId=subcription_id,
                policyDefinitionName=policyDefinitionName)

            if policy_assignment_response and policy_assignment_response.status_code in range(200, 299):
                print("Policy assignment {} with code {} in subscription {}".format(policyDefinitionName,
                                                                                    policy_assignment_response.status_code,
                                                                                    subcription_id))
            elif policy_assignment_response and policy_assignment_response.status_code not in range(200, 299):
                print(policy_assignment_response)

            return policy_assignment_response



    def get_filtered_management_grp_policy_definitions(self, management_grp_id, category=None):

        policy_definition_list = list()

        policy_definition = PolicyDefinition()
        response = policy_definition.policy_definitions_list_by_management_group(management_grp_id)

        if response.status_code in range(200, 299):
            policy_definition_json =  response.json()
            if 'value' in policy_definition_json:

                if category is not None:
                    for policy in policy_definition_json['value']:
                        if 'properties' in policy and 'metadata' in policy['properties'] and 'category' in policy['properties']['metadata']:
                            if category == policy['properties']['metadata']['category']:
                                policy_definition_list.append(policy)
                else:
                    policy_definition_list = policy_definition_json['value']



        return policy_definition_list

    def get_management_group_assignments_for_member_subscriptions(self, management_grp_id, category):
        """
        This test creates a policy assignment for definitions the exist on the file system
        :return:
        """

        batch_uuid = uuid.uuid4()

        aggregate_subscriptions = AggregateSQLSubscriptions()
        subscriptions = aggregate_subscriptions.list_subscriptions()
        assignment_policy_list = list()

        policy_definitions_list = self.get_filtered_management_grp_policy_definitions(management_grp_id=management_grp_id, category=category)
        # subscriptions.reverse()

        for subscription in subscriptions:
            policy_assignment = dict()
            policy_assignment['management_grp_id'] = management_grp_id
            policy_assignment['subscription_id'] = subscription.subscription_id
            policy_assignment['policy_definitions'] = policy_definitions_list

            assignment_policy_list.append(policy_assignment)

        return assignment_policy_list
