import unittest
from configparser import ConfigParser
from dotenv import load_dotenv
from mop.azure.operations.policy_states import ScourPolicyStatesOperations
from mop.azure.utils.manage_api import TESTVARIABLES


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
