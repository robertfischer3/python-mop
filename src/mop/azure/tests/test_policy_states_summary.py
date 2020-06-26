import unittest
import logging
import os
from configparser import ConfigParser

from dotenv import load_dotenv
from mop.azure.analysis.policies.summarize_for_subscription import SummarizeForSubscription
from mop.azure.analysis.policies.summary_for_policy_definition import SummaryForPolicyDefinition
from mop.azure.utils.create_configuration import change_dir, OPERATIONSPATH, TESTVARIABLES


class TestPolicyStatesSummary(unittest.TestCase):
    def setUp(self) -> None:
        load_dotenv()
        with change_dir(OPERATIONSPATH):
            self.config = ConfigParser()
            self.config.read(TESTVARIABLES)

    def test_summarize_for_subscription(self):
        summary = SummarizeForSubscription()
        summary.Summarize_For_Subscription()
        self.assertEqual(True, True)

    def test_summarize_policy_defintions_for_all_management_grp(self):
        management_grp_id = self.config["DEFAULT"]["management_grp_id"]
        metadata_category = self.config["FILTERS"]["policy_definition_category"]
        summary = SummaryForPolicyDefinition()
        summary.summarize_policy_defintions_for_all_management_grp(management_grp_id, 'security-pol-vm-diskencrypt',
                                                                   metadata_category)


if __name__ == '__main__':
    unittest.main()
