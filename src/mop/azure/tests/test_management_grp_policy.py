from unittest import TestCase
from mop.azure.comprehension.resources.policy_definitions import get_management_grp_policies

class TestManagement_grp_policy(TestCase):
    def test_management_grp_policy_list(self):
        get_management_grp_policies()
        self.fail()
