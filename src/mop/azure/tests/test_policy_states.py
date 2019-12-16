import os
import unittest
from configparser import ConfigParser

import pandas as pd
from dotenv import load_dotenv
import json

from mop.azure.analysis.policy_analysis import EvaluatePolicies
from mop.azure.connections import Connections
from mop.azure.operations.policy_states import ScourPolicyStatesOperations
from mop.azure.utils.create_configuration import (
    TESTVARIABLES,
    change_dir,
    OPERATIONSPATH,
)


class TestOperationsPolicyStates(unittest.TestCase):
    def setUp(self) -> None:
        load_dotenv()
        with change_dir(OPERATIONSPATH):
            self.config = ConfigParser()
            self.config.read(TESTVARIABLES)

    def test_policy_states_summarize_for_subscription(self):
        """
        Testing the policy_states_summarize_for_subscription methods on the class ScourPolicyStatesOperations
        :return:
        """
        subscription = self.config["DEFAULT"]["subscription"]
        scour_policy = ScourPolicyStatesOperations()
        execute = scour_policy.policy_states_summarize_for_subscription(subscription)
        # Execute returns a method the can be executed anywhere more than once
        result = execute()
        self.assertIsNotNone(result)

        result2 = execute()
        self.assertIsNotNone(result2)

        values = result["value"]
        self.assertIs(type(values), list)

    def test_policy_states_summarize_for_subscription(self):
        """
        Testing the policy_states_summarize_for_subscription methods on the class ScourPolicyStatesOperations
        :return:
        """
        subscription = self.config["DEFAULT"]["subscription_id"]
        scour_policy = ScourPolicyStatesOperations()
        execute = scour_policy.policy_states_summarize_for_subscription(subscription)
        # Execute returns a method the can be executed anywhere more than once
        result = execute()

        summarize_results = result["value"]
        for summary in summarize_results:
            policyAssignments = summary["policyAssignments"]
            for policy_assignment in policyAssignments:
                policyAssignmentId = policy_assignment["policyAssignmentId"]
                policySetDefinitionId = policy_assignment["policySetDefinitionId"]

                self.assertIsNotNone(policyAssignmentId)
                self.assertIsNotNone(policySetDefinitionId)

                complianceState = policy_assignment["results"]["resourceDetails"][0]
                com_state = complianceState["complianceState"]
                com_state_cnt = complianceState["count"]

                self.assertIsNotNone(com_state)
                self.assertEqual(type(com_state_cnt), type(1))

                non_complianceState = policy_assignment["results"]["resourceDetails"][1]
                non_comp_state = non_complianceState["complianceState"]
                non_comp_state_cnt = non_complianceState["count"]

                self.assertIsNotNone(non_comp_state)
                self.assertEqual(type(non_comp_state_cnt), type(1))

                break

    def test_generic_function(self):
        """
            Demonstration the composability of the framework. Returns a method can be called at any time
        :return:
        """
        subscriptionId = os.environ["SUB"]
        polic_states = ScourPolicyStatesOperations()
        api_config_key = "https://management.azure.com/subscriptions/{subscriptionId}/providers/Microsoft.PolicyInsights/policyStates/latest/summarize?api-version=2019-10-01"
        # The policystates_genericfunc has no way of learning the named string format parameters
        # a simple replace makes the URL a workable generic call to the API
        api_config_key = api_config_key.replace("{subscriptionId}", "{}")

        execute = polic_states.policystates_genericfunc(api_config_key, subscriptionId,)
        result = execute()

        self.assertIsNotNone(result)

    def test_aggregation(self):

        subscription = os.environ["SUB"]
        management_grp = os.environ["MANGRP"]

        credentials = Connections().get_authenticated_client()
        eval_policies = EvaluatePolicies(credentials)
        df = eval_policies.process_management_grp_subscriptions(management_grp)

    def test_correlate_management_grp_data(self):

        parquet_file = "TestingCorrelation.parquet"
        xlsx_file = "TestingCorrelation.xlsx"
        with change_dir(OPERATIONSPATH):
            if os.path.isfile(parquet_file):
                os.remove(parquet_file)

        subscription = os.environ["SUB"]
        management_grp = os.environ["MANGRP"]

        credentials = Connections().get_authenticated_client()
        df = EvaluatePolicies(credentials).correlate_management_grp_data(
            management_grp=management_grp, subscription=subscription
        )



