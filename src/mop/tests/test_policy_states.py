import unittest
from configparser import ConfigParser
from dotenv import load_dotenv
from mop.azure.operations.policy_states import ScourPolicyStatesOperations

TESTVARIABLES = 'testvariables.ini'

class TestConfigParser(unittest.TestCase):

    def test_create_config_file_sections(self):
        config = ConfigParser()
        config['DEFAULT'] = {'subscription': '1c1ec02c-560c-4f3f-a8f1-4b29640fdfc6'}
        config['AZURESDK'] = {
            'PolicyStatesSummarizeForPolicyDefinition':'https://management.azure.com/subscriptions/{subscriptionId}/providers/Microsoft.Authorization/policyDefinitions/{policyDefinitionName}/providers/Microsoft.PolicyInsights/policyStates/latest/summarize?api-version=2019-10-01',
            'PolicyStatesSummarizeForSubscription':'https://management.azure.com/subscriptions/{subscriptionId}/providers/Microsoft.PolicyInsights/policyStates/latest/summarize?api-version=2019-10-01',
            'PolicyStatesSummarizeForSubscriptionFiltered':'https://management.azure.com/subscriptions/{subscriptionId}/providers/Microsoft.PolicyInsights/policyStates/latest/summarize?api-version=2019-10-01&$filter={filter}',
            '':'',
        }
        with open(TESTVARIABLES, 'w') as configfile:
            config.write(configfile)

    def test_read_testvariables_ini(self):
        config = ConfigParser()
        print(config.read(TESTVARIABLES))
        print(config['DEFAULT']['subscription'])


class TestOperationsPolicyStates(unittest.TestCase):

    def setUp(self) -> None:
        load_dotenv()

        self.config = ConfigParser()
        self.config.read(TESTVARIABLES)

    def test_policy_states_summarize_for_subscription(self):
        """
        Testing the policy_states_summarize_for_subscription methods on the class ScourPolicyStatesOperations
        :return:
        """
        subscription =  self.config['DEFAULT']['subscription']
        scour_policy = ScourPolicyStatesOperations()
        execute = scour_policy.policy_states_summarize_for_subscription(subscription)
        #Execute returns a method the can be executed anywhere more than once
        result = execute()
        self.assertIsNotNone(result)

        result2 = execute()
        self.assertIsNotNone(result2)

        values = result['value']
        self.assertIs(type(values), list)

    def test_policy_states_summarize_for_subscription(self):
        pass
