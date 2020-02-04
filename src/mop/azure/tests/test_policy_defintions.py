import json
import os
import unittest
from configparser import ConfigParser

from dotenv import load_dotenv

from mop.azure.utils.create_configuration import OPERATIONSPATH, change_dir, TESTVARIABLES
from mop.azure.comprehension.resource_management.policy_definitions import PolicyDefinition

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

    def test_policy_definition_via_policyDefinitionId(self):

        policy_definitions = PolicyDefinition()
        policyDefinitionId = "/subscriptions/82746ea2-9f97-4313-b21a-e9bde3a0a241/providers/microsoft.authorization/policydefinitions/glbl-pr-sec-storage-auditencryption-pol"
        response = policy_definitions.policy_definition_via_policyDefinitionId(policyDefinitionId)
        json_response = response.json()
        print(json_response)

    def test_get_policy_definition(self):

        policy_definitions = PolicyDefinition()
        result = policy_definitions.get_policy_definition('glbl-pr-sec-storage-https-pol')

        print(result)

    def test_policy_definitions_by_subscription(self):
        """

        :return:
        """

        subscriptionId = self.config['DEFAULT']['subscription_id']

        policy_definitions = PolicyDefinition()
        defintion_list_function = policy_definitions.policy_definitions_by_subscription_req(subscriptionId=subscriptionId)

        results = defintion_list_function.json()
        policy_definitions = json.dumps(results, indent=4, ensure_ascii=False)
        with open("test_policy_definitions_subscription.json", "w") as json_results:
            json_results.write(policy_definitions)

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
        """

        :return:
        """

        managementGroupId = self.config['DEFAULT']['management_grp_id']
        search_category = self.config["FILTERS"]["policy_defition_category"]

        response = self.policy_definition_list_by_management_group_category(managementGroupId)

        policy_definitions = json.dumps(response.json(), indent=4, ensure_ascii=False)
        with open("test_policy_definitions.json", "w") as json_results:
            json_results.write(policy_definitions)

        self.assertIsInstance(response.json(), dict)

        self.assertEqual(True, True)

    def policy_definition_list_by_management_group_category(self, managementGroupId):
        policy_definitions = PolicyDefinition()
        response = policy_definitions.policy_definitions_list_by_management_group(managementGroupId)
        results = response.json()
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
        return response


if __name__ == '__main__':
    unittest.main()
