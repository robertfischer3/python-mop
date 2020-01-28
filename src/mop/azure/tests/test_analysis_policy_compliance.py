import logging
import unittest
from configparser import ConfigParser
import os
from dotenv import load_dotenv

from mop.azure.analysis.policy_compliance import PolicyCompliance
from mop.azure.utils.create_configuration import (
    TESTVARIABLES,
    change_dir,
    OPERATIONSPATH,
)


class TestAnalysisCompileCompliance(unittest.TestCase):
    def setUp(self) -> None:
        load_dotenv()
        logging.basicConfig(level=logging.WARN)
        logging.debug("Current working directory {}".format(os.getcwd()))
        with change_dir(OPERATIONSPATH):
            logging.debug("Current change_dir working directory {}".format(os.getcwd()))
            self.config = ConfigParser()
            self.config.read(TESTVARIABLES)

    def test_summarize_subscriptions(self):

        management_grp = self.config["DEFAULT"]["management_grp_id"]
        tenant_id = self.config['DEFAULT']['tenant_id']

        summarize = PolicyCompliance()
        summarize.summarize_subscriptions(management_grp)


    def test_summarize_query_results_for_policy_definitions(self):

        subscriptionId = self.config["DEFAULT"]["subscription_id"]

        summarize = PolicyCompliance()
        summarize.reduce_policy_definition_list(subscription_list=[subscriptionId], metadata_category='Nestle Security',
                                                                      include=['Custom'], )
        summarize.summarize_query_results_for_policy_definitions()
