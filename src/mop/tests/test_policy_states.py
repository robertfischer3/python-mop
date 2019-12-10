import unittest
from configparser import ConfigParser
from dotenv import load_dotenv
from mop.azure.operations.policy_states import ScourPolicyStatesOperations

class TestConfigParser(unittest.TestCase):

    def test_config_file_sections(self):
        config = ConfigParser()

        self.assertIsNotNone(config.read("testvariables.ini"))
        default = config.default_section
        self.assertGreater(len(default), 0)

class TestOperationsPolicyStates(unittest.TestCase):

    def setUp(self) -> None:
        load_dotenv()

    def test(self):
        scour_policy = ScourPolicyStatesOperations()
        result = scour_policy.policy_states_summarize_for_subscription()
        print(result)


