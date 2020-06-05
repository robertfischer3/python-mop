import logging
import os
import unittest
from configparser import ConfigParser

from dotenv import load_dotenv

from mop.azure.analysis.policy_compliance import PolicyCompliance
from mop.azure.comprehension.resource_management.policy_definitions import PolicyDefinition
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
        summarize.summarize_subscriptions(tenant_id)

    def test_summarize_query_results_for_policy_definitions(self):
        subscriptionId = self.config["DEFAULT"]["subscription_id"]
        management_grp = self.config["DEFAULT"]["management_grp_id"]

        summarize = PolicyCompliance()
        summarize.summarize_management_group_policy_definitions(management_grp)

        for policy_definition_name in policy_definition_name_list:
            summarize = PolicyCompliance()
            summarize.save_subscription_policies_by_category(category=category)
            summarize.summarize_fact_compliance_for_definition(category=category,
                                                               policy_definition_name=policy_definition_name)

        #summarize.summarize_query_results_for_policy_definitions()

    def test_compiled_sci(self):
        summarize = PolicyCompliance()
        summarize.compile_sci()

    def test_register_policy_definition(self):
        policy_definition_names = ['glbl-pr-sec-vmss-nomanageddisks-pol',
                                   'glbl-pr-sec-sqlserver-noaadadmin-pol',
                                   'glbl-pr-sec-vm-diskencrypt-pol',
                                   'glbl-pr-sec-storage-vnet-pol',
                                   'glbl-pr-sec-sqlserver-serverlevelthreatdetection-pol',
                                   'glbl-pr-sec-sqlserver-serverlevelauditsetting-pol',
                                   'glbl-pr-sec-sqldb-threatdetection-pol',
                                   'glbl-pr-sec-sqldb-encryption-pol',
                                   'glbl-pr-sec-sqldb-dblevelauditsetting-pol',
                                   'glbl-pr-sec-keyvault-novnetrules-pol',
                                   'glbl-pr-sec-DatalakeStore-serviceEndpoint-pol',
                                   'glbl-pr-sec-acr-contenttrust-pol']

        subscription_id = 'c537daa8-e7a7-4648-bbc0-f2b6386cca83'
        policy_compliance = PolicyCompliance()
        for policy_definition_name in policy_definition_names:
            policy_compliance.register_policy_definition(subscription_id=subscription_id,
                                                         policy_definition_name=policy_definition_name)

    def test_save_subscription_policies_by_category(self):
        category = self.config["FILTERS"]["policy_definition_category"]
        subscriptionId = self.config["DEFAULT"]["subscription_id"]

        policy_definition_name_list = ['glbl-pr-sec-acr-contenttrust-pol',
                                       'glbl-pr-sec-aks-nopodsecuritypolicies-pol',
                                       'glbl-pr-sec-storage-vnet-pol',
                                       'glbl-pr-sec-sqlserver-noaadadmin-pol',
                'glbl-pr-sec-sqlserver-serverlevelthreatdetection-pol',
                                       'glbl-pr-sec-sqlserver-serverlevelauditsetting-pol',
                                       'glbl-pr-sec-sqldb-threatdetection-pol',
                                       'glbl-pr-sec-sqldb-encryption-pol',
                                       'glbl-pr-sec-sqldb-dblevelauditsetting-pol',
                                       'glbl-pr-sec-sqlserver-noaadadmin-pol',
                                       'glbl-pr-sec-keyvault-novnetrules-pol',
                                       'glbl-pr-sec-aks-nopodsecuritypolicies-pol',
                                       'glbl-pr-sec-vm-diskencrypt-pol',
                                       'glbl-pr-sec-vmss-nomanageddisks-pol',
                                       'security-pol-adl-gen1diagnosticlogsanalytics',
                                       'glbl-pr-sec-vm-windowsantimalware-pol'
                                       ]

        for policy_definition_name in policy_definition_name_list:
            summarize = PolicyCompliance()
            # summarize.save_subscription_policies_by_category(category=category)
            summarize.summarize_fact_compliance_for_definition(category=category,
                                                               policy_definition_name=policy_definition_name)
