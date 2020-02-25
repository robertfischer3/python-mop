import json
import unittest
import uuid
from configparser import ConfigParser

from dotenv import load_dotenv

from mop.azure.analysis.baseline.aggregate_subscriptions import AggregateSubscriptions
from mop.azure.comprehension.resource_management.policy_definitions import PolicyDefinition
from mop.azure.utils.create_configuration import OPERATIONSPATH, change_dir, TESTVARIABLES
from mop.azure.utils.atomic_writes import atomic_write

class TestPolicyDefinitionsCase(unittest.TestCase):

    def setUp(self) -> None:
        load_dotenv()
        with change_dir(OPERATIONSPATH):
            self.config = ConfigParser()
            self.config.read(TESTVARIABLES)

    def test_create_subscription_policy_definition(self):

        subscriptionId = "82746ea2-9f97-4313-b21a-e9bde3a0a241"
        policy_definitions = PolicyDefinition()

        results = policy_definitions.create_subscription_policy_definition(subscriptionId)
        self.assertEqual(201, results.status_code)

    def test_create_subscriptions_policy_definition(self):
        """

        :return:
        """
        batch_uuid = uuid.uuid4()
        subscriptions = AggregateSubscriptions()
        result = subscriptions.list_subscriptions()
        policy_definitions = PolicyDefinition()
        for subscription in result:
            print(subscription.subscription_id)
            response = policy_definitions.create_subscription_policy_definition(subscription.subscription_id)
            if response is not None:
                response_dict = response.json()

                response_dict["subscription_id"] = subscription.subscription_id
                response_dict["subscription_display_name"] = subscription.subscription_display_name
                response_dict["status_code"] = response.status_code

                policy_assignment_record = json.dumps(response_dict, indent=4, ensure_ascii=False)
                with open("policy_definition_records{}.json".format(batch_uuid), "a+") as json_results:
                    json_results.write(policy_assignment_record)


    def test_create_subscription_policy_assignment(self):

        batch_uuid = uuid.uuid4()

        subscriptions = AggregateSubscriptions()
        result = subscriptions.list_subscriptions()
        policy_definitions = PolicyDefinition()
        for subscription in result:
            print(subscription.subscription_id)
            response = policy_definitions.create_subscription_policy_assignment(subscription.subscription_id)



    def test_policy_definition_via_policyDefinitionId(self):

        policy_definitions = PolicyDefinition()

        models = self.get_db_model(self.engine)
        FactCompliance = models.classes.factcompliance
        DimPolicies = models.classes.policydefinitions

        session = self.Session()
        results = session.query(FactCompliance).all()
        pf = session.query(DimPolicies).all()

        policies_found = list()
        policy_definition_name = 'glbl-pr-sec-storage-auditvnet-pol'
        policyDefinitionId = "/subscriptions/c537daa8-e7a7-4648-bbc0-f2b6386cca83/providers/Microsoft.Authorization/policyDefinitions/glbl-pr-sec-storage-auditvnet-pol"
        response = policy_definitions.policy_definition_via_policyDefinitionId(policyDefinitionId)
        json_response = response.json()

        policy_definition = json_response

        if policy:
            displayName = policy_definition['properties']['displayName']
            if 'description' in policy_definition['properties']:
                description = policy_definition['properties']['description']
            else:
                description = policy_definition['properties']['displayName']
            policyType = policy_definition['properties']['policyType']
            if 'category' in policy_definition['properties']['metadata']:
                category = policy_definition['properties']['metadata']['category']
            else:
                category = ''
            print(displayName)

        policy = DimPolicies(policy_definition_name=row.policy_definition_name,
                             policy_description=description,
                             policy_display_name=displayName,
                             policy_type=policyType,
                             metadata_category=category)


    def test_get_policy_definition(self):

        subscriptions = AggregateSubscriptions()
        result = subscriptions.list_subscriptions()
        for subscription in result:
            print(subscription.subscription_id)
            policy_definitions = PolicyDefinition()
            pol_def_name = policy_definitions.get_policy_definitions(subscription_id=subscription.subscription_id,
                                                                     policy_definition_name="glbl-pr-sec-storage-auditencryption-pol")
            print(pol_def_name)

    def test_policy_definitions_by_subscription(self):
        """

        :return:
        """

        subscriptionId = self.config['DEFAULT']['subscription_id']
        category = "Nestle Security"

        policy_definitions = PolicyDefinition()
        policy_definition_list = policy_definitions.list_subscription_policy_definition_by_category(subscriptionId=subscriptionId,
                                                                           category=category)
        for policy in policy_definition_list:
            if 'category' in policy['properties']['metadata']:
                if policy['properties']['metadata']['category'] in category:
                    self.assertTrue(True)
                else:
                    self.assertTrue(False)
            else:
                self.assertTrue(False)

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
