import json
import unittest
import uuid
from configparser import ConfigParser

from dotenv import load_dotenv

from mop.azure.analysis.baseline.aggregate_subscriptions import AggregateSubscriptions
from mop.azure.comprehension.resource_management.policy_definitions import PolicyDefinition
from mop.azure.utils.create_configuration import OPERATIONSPATH, change_dir, TESTVARIABLES


class TestPolicyDefinitionsCase(unittest.TestCase):

    def setUp(self) -> None:
        load_dotenv()
        with change_dir(OPERATIONSPATH):
            self.config = ConfigParser()
            self.config.read(TESTVARIABLES)

    def test_create_subscription_policy_definition(self):
        '''
        Create a test to create policy definitions in a single Azure subscription
        :return:
        '''
        subscriptionId = self.config['DEFAULT']['subscription_id']
        policy_definitions = PolicyDefinition()

        results = policy_definitions.create_subscription_policy_definition(subscriptionId)

        for key in results.keys():
            print(key)
            if results[key].status_code != 201:
                results[key]
            self.assertEqual(201, results[key].status_code)

    def test_create_subscriptions_policy_definition(self):
        """
        Create a test to create policy definitions in a across multiple Azure subscriptions
        :return:
        """
        batch_uuid = uuid.uuid4()
        subscriptions = AggregateSubscriptions()
        result = subscriptions.list_subscriptions()
        policy_definitions = PolicyDefinition()
        for subscription in result:
            print(subscription.subscription_id)
            responses = policy_definitions.create_subscription_policy_definition(subscription.subscription_id)
            if responses is not None:
                for policy_definition_name in responses.keys():
                    response_dict = responses[policy_definition_name].json()

                    response_dict["subscription_id"] = subscription.subscription_id
                    response_dict["subscription_display_name"] = subscription.subscription_display_name
                    response_dict["status_code"] = responses[policy_definition_name].status_code

                    policy_assignment_record = json.dumps(response_dict, indent=4, ensure_ascii=False)
                    with open("policy_definition_records{}.json".format(batch_uuid), "a+") as json_results:
                        json_results.write(policy_assignment_record)

    def test_create_management_group_definition(self):
        management_grp_id = self.config['DEFAULT']['management_grp_id']
        management_grp_policy_definition = PolicyDefinition()

        policy_definition_files = management_grp_policy_definition.get_json_policy_definitions()

        results = {}

        for policy_definition_file in policy_definition_files:
            with open(policy_definition_file['policy_definition_path']) as definition:
                try:
                    policy_definition_body = json.load(definition)
                except:
                    print("Creation failed for ", policy_definition_file['policy_defintion_name'])
                    continue

                if 'name' in policy_definition_body:
                    policyDefinitionName = policy_definition_body['name']

                    if policyDefinitionName:
                        policy_definition_body = json.dumps(policy_definition_body)
                        response = management_grp_policy_definition.create_management_group_definition(
                            management_grp_id,
                            policyDefinitionName=policyDefinitionName,
                            policy_definition_body=policy_definition_body)
                        print(policyDefinitionName, response.status_code)
                        results[policyDefinitionName] = response.status_code
                else:
                    self.assertTrue(False, msg="Policy Definition Name not found {}".format(policy_definition_file))

        for key in results.keys():
            if results[key] not in range(200, 299):
                print('Policy creation error {}'.format(key))

    def test_create_management_group_assignment_at_subscription_level(self):

        management_grp_id = self.config['DEFAULT']['management_grp_id']

        policy_definition = PolicyDefinition()
        policy_definition_files = policy_definition.get_json_policy_definitions()

        batch_uuid = uuid.uuid4()

        aggregate_subscriptions = AggregateSubscriptions()
        subscriptions = aggregate_subscriptions.list_subscriptions()
        #subscriptions.reverse()

        for subscription in subscriptions:
            for policy_definition_file in policy_definition_files:
                with open(policy_definition_file['policy_definition_path']) as definition:
                    try:
                        policy_definition_body = json.load(definition)
                        result = self.create_policy_assignment_with_management_group_policy(
                            management_grp_id=management_grp_id,
                            policy_definition_body=policy_definition_body,
                            subcription_id=subscription.subscription_id)
                        if not result:
                            print("{}: Assignment not created, {}".format(subscription.subscription_id,
                                                                          policy_definition_file[
                                                                              'policy_definition_path']))
                    except json.decoder.JSONDecodeError as jason_error:
                        print(jason_error.msg)

    def create_policy_assignment_with_management_group_policy(self, management_grp_id, policy_definition_body,
                                                              subcription_id):
        policy_definition = PolicyDefinition()
        if 'name' in policy_definition_body:
            policyDefinitionName = policy_definition_body['name']
        else:
            self.assertTrue(False, msg="Policy Definition Name not found")

        if policyDefinitionName:
            policy_assignment_response = policy_definition.create_management_group_policy_assignment_at_subscription_level(
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

            # self.assertTrue(False, "Policy cannot be assigned, parameters not specified")

    def test_create_single_subscription_policy_assignment(self):
        '''
        Create a single assignment across in single subscriptions
        :return:
        '''
        subscriptionId = self.config['DEFAULT']['subscription_id']

        policy_definitions = PolicyDefinition()
        definitions = policy_definitions.get_json_policy_definitions()

        policy_assignments, responses = policy_definitions.create_subscription_policy_assignment(subscriptionId,
                                                                                                 definitions)
        for response in responses:
            self.assertEqual(response.status_code, 200)

    def test_create_subscription_policy_assignment(self):

        batch_uuid = uuid.uuid4()

        subscriptions = AggregateSubscriptions()
        result = subscriptions.list_subscriptions()
        policy_definitions = PolicyDefinition()
        definitions = policy_definitions.get_json_policy_definitions()

        for subscription in result:
            print(subscription.subscription_id)
            response = policy_definitions.create_subscription_policy_assignment(subscription.subscription_id,
                                                                                definitions)

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
        category = self.config['FILTERS']['policy_definition_category']

        policy_definitions = PolicyDefinition()
        policy_definition_list = policy_definitions.list_subscription_policy_definition_by_category(
            subscriptionId=subscriptionId,
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
        search_category = self.config["FILTERS"]["policy_definition_category"]
        policy_definitons = PolicyDefinition()

        response = policy_definitons.list_by_management_group_category(managementGroupId, search_category)

        policy_definitions = json.dumps(response.json(), indent=4, ensure_ascii=False)
        with open("test_policy_definitions.json", "w") as json_results:
            json_results.write(policy_definitions)

        self.assertIsInstance(response.json(), dict)


if __name__ == '__main__':
    unittest.main()
