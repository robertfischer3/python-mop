import unittest
import json
from configparser import ConfigParser

from dotenv import load_dotenv

from mop.azure.comprehension.resource_management.policy_assignments import PolicyAssignments
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


if __name__ == '__main__':
    unittest.main()
