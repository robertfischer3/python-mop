import json
import os
import unittest
from configparser import ConfigParser

from dotenv import load_dotenv

from mop.azure.utils.create_configuration import OPERATIONSPATH, change_dir, TESTVARIABLES
from mop.azure.resources.policy_definitions import PolicyDefinition

class TestPolicyDefinitionsCase(unittest.TestCase):

    def setUp(self) -> None:
        load_dotenv()
        with change_dir(OPERATIONSPATH):
            self.config = ConfigParser()
            self.config.read(TESTVARIABLES)
        # The driver often needs to be obtained from the database publisher
        self.driver = "{ODBC Driver 17 for SQL Server}"
        # Server is the IP address or DNS of the database server
        self.server = "172.17.0.1"
        # Can be any database name, as long as you are consistent
        self.database = "TestDB2"
        # Never place passwords in code.  Your just asking for trouble otherwise
        self.password = os.environ["DATABASEPWD"]
        # Do not use SA in production
        user = "SA"

    def test_get_policy_definition(self):

        policy_definitions = PolicyDefinition()
        result = policy_definitions.get_policy_definition('501541f7-f7e7-4cd6-868c-4190fdad3ac9')

        print(result)

    def test_policy_definitions_by_subscription(self):
        subscriptionId = self.config['DEFAULT']['subscription_id']
        policy_definitions = PolicyDefinition()
        defintion_list_function = policy_definitions.policy_definitions_by_subscription(subscriptionId=subscriptionId)
        results = defintion_list_function()
        policies = results['value']
        for policy in policies:
            print(subscriptionId)
            print(policy['name'])
            if 'category' in policy['properties']['metadata']:
                if policy['properties']['metadata']['category'] in 'Nestle Security':
                   print(['properties']['metadata']['category'])

            print(policy['properties']['displayName'])
            if policy['properties']['description']:
                print(policy['properties']['description'])

    def test_policy_definitions_list_by_management_group(self):

        managementGroupId = self.config['DEFAULT']['management_grp_id']
        search_category = 'Nestle Security'


        policy_definitions = PolicyDefinition()

        defintion_list_function = policy_definitions.policy_definitions_list_by_management_group(managementGroupId)
        results = defintion_list_function()

        policies = results['value']
        for policy in policies:
            policy_type = policy['properties']['policyType']
            if policy_type not in ['BuiltIn', 'Static']:
                policy_name = policy['name']
                policy_category = ""
                if 'category' in policy['properties']['metadata']:
                    policy_category = ['properties']['metadata']['category']

                policy_display_name = policy['properties']['displayName']
                if policy['properties']['description']:
                    policy_description = policy['properties']['description']


        self.assertEqual(True, True)

if __name__ == '__main__':
    unittest.main()
