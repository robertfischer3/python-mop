import json
import os
import unittest
from configparser import ConfigParser

from dotenv import load_dotenv

from mop.azure.utils.create_configuration import OPERATIONSPATH, change_dir, TESTVARIABLES
from mop.azure.resources.policy_definitions import PolicyDefinitions

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

    def test_something(self):
        subscriptionId = self.config['DEFAULT']['subscription_id']
        policy_definitions = PolicyDefinitions()
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



        self.assertEqual(True, True)

if __name__ == '__main__':
    unittest.main()
