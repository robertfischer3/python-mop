import json
import unittest
from configparser import ConfigParser

import jmespath
from dotenv import load_dotenv

from mop.azure.comprehension.resource_management.policy_assignments import PolicyAssignments
from mop.azure.comprehension.resource_management.policy_set_definition import PolicySetDefinition
from mop.azure.utils.create_configuration import change_dir, OPERATIONSPATH, TESTVARIABLES


class TestCasePolicyAssigments(unittest.TestCase):
    def setUp(self) -> None:
        load_dotenv()
        with change_dir(OPERATIONSPATH):
            self.config = ConfigParser()
            self.config.read(TESTVARIABLES)

    def test_policy_assignments_list(self):
        subscription_id = self.config['DEFAULT']['subscription_id']
        response = PolicyAssignments().policy_assignments_list(subscription_id)
        policy_assignments = json.dumps(response.json(), indent=4, ensure_ascii=False)
        with open("test_assignments.json", "w") as json_results:
            json_results.write(policy_assignments)

        self.assertIsInstance(response.json(), dict)

    def test_policy_set_definition(self):
        subscription_id = self.config['DEFAULT']['subscription_id']
        policy_definition_category = self.config['FILTERS']['policy_definition_category']

        policySetDefinitionName = "{}SubscriptionPolicies".format(policy_definition_category).replace(' ', '')

        policy_set_properties_body = {
            "properties": {
                "displayName": "{} Minimum Requirements".format(policy_definition_category),
                "description": "{} Minimum Requirements for an Azure subscription".format(policy_definition_category),
                "metadata": {
                    "category": policy_definition_category
                }
            },
            "policyDefinitionGroups": [],
            "policyDefinitions": []
        }

        policy_definition_groups = [{
            "name": "AuditPolicy",
            "displayName": "Audit Policies",
            "description": "{} Audit Policy".format(policy_definition_category)
        }, ]

        response = PolicyAssignments().policy_assignments_list(subscription_id)
        if response.status_code >= 200 and response.status_code <= 299:
            policy_assignments = response.json()

            if 'value' in policy_assignments:

                policy_definitions = policy_assignments['value']
                policy_set_definition = PolicySetDefinition()
                policy_set_definitions_in_category = []
                for policy_definition in policy_definitions:
                    category = jmespath.search('properties.metadata.category', policy_definition)
                    if category and policy_definition_category in category:
                        policy_set_definitions_in_category.append(policy_definition)

                policy_set_definition.create_or_update(subscription_id,
                                                       policySetDefinitionName=policySetDefinitionName,
                                                       policyDefinitionsList=policy_set_definitions_in_category,
                                                       policy_set_properties_body=policy_set_properties_body,
                                                       policyDefinitionReferenceId='Minimum_Requirement')


if __name__ == '__main__':
    unittest.main()
