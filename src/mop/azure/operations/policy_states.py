import os
from configparser import ConfigParser

import requests
from azure.mgmt.policyinsights.policy_insights_client import PolicyInsightsClient
from dotenv import load_dotenv
from azure.mgmt.policyinsights.models import QueryOptions
from mop.azure.connections import AzureSDKAuthentication, request_authenticated_session
from azure.mgmt.policyinsights.models import QueryFailureException

from mop.azure.utils.manage_api import CONFVARIABLES, change_dir, OPERATIONSPATH


class ScourPolicyStatesOperations:

    def __init__(self):
        load_dotenv()
        with change_dir(OPERATIONSPATH):
            self.config = ConfigParser()
            self.config.read(CONFVARIABLES)

    def list_operations(self, subscription):
        api_endpoint = os.environ['PolicyDefinitionsListBuiltin']
        with request_authenticated_session as req:
            print(req.headers)
            definitions = req.post(api_endpoint).json()

        return definitions

    def policy_states_summarize_for_resource(self, resourceId):
        api_endpoint = self.config['AZURESDK']['policystatessummarizeforresource']
        api_endpoint = api_endpoint.format(resourceId=resourceId)

        with request_authenticated_session() as req:
            resource_policy_function = req.post(api_endpoint).json()
        return resource_policy_function

    def policy_states_summarize_for_policy_definition(self, subscription, policyDefinitionName):
        api_endpoint = os.environ['PolicyStatesSummarizeForPolicyDefinition']
        api_endpoint = api_endpoint.format(subscriptionId=subscription,
                                           policyDefinitionName=policyDefinitionName)
        with request_authenticated_session() as req:
            policy_def_builtin = req.post(api_endpoint).json()

        return policy_def_builtin

    def policy_states_summarize_for_subscription(self, subscription):
        '''

        :param subscription:
        :return:
        '''
        api_endpoint = self.config['AZURESDK']['policystatessummarizeforsubscription']
        api_endpoint = api_endpoint.format(subscriptionId=subscription)
        with request_authenticated_session() as req:
            policy_states_summary_subscription = req.post(api_endpoint).json

        return policy_states_summary_subscription


    def policy_states_summarize_for_subscription_compliant(self, subscriptionId, is_compliant='true'):
        '''

        :param subscription: str
        :param is_compliant: bool
        :return:
        '''

        filter_condition = "IsCompliant eq {}".format(is_compliant)

        api_endpoint = self.config['DEFAULT']['PolicyStatesSummarizeForSubscriptionFiltered']
        api_endpoint = api_endpoint.format(subscriptionId=subscriptionId, filter=filter_condition)

        with request_authenticated_session() as req:
            policy_states_summary_subscription = req.post(api_endpoint).json()

        return policy_states_summary_subscription

    def policy_states_filter_and_multiple_groups(self, subscriptionId):
        api_endpoint = os.environ['PolicyStatesFilterandmultiplegroups']
        api_endpoint = api_endpoint.format(subscriptionId=subscriptionId)

        with request_authenticated_session() as req:
            r_policy_states_filter_and_multiple_groups = req.post(api_endpoint).json()

        return r_policy_states_filter_and_multiple_groups

    def policy_states_filter_and_multiple_groups_compliant(self, subscriptionId):
        api_endpoint = os.environ['PolicyStatesFilterandmultiplegroups']
        api_endpoint = api_endpoint.format(subscriptionId=subscriptionId)

        with ReguestSession() as req:
            r_policy_states_filter_and_multiple_groups = req.post(api_endpoint).json()

        return r_policy_states_filter_and_multiple_groups

    def summarize_for_subscript(self, creds, subscription_id):
        #
        policy_client = PolicyInsightsClient(credentials=creds, base_url=None)
        summarized_results = policy_client.policy_states.summarize_for_subscription(subscription_id)

        return summarized_results

    def list_query_results_for_subscription_wrapper(self, credentials,
                                                                    subscription_id,
                                                                    policy_assignment_name):
        query = QueryOptions(filter='IsCompliant eq false')
        policy_client = PolicyInsightsClient(credentials=credentials, base_url=None)

        try:

            summary_results = policy_client.policy_states.list_query_results_for_subscription('latest',
                                                                                                subscription_id=subscription_id,
                                                                                                policy_definition_name=policy_assignment_name,
                                                                                                custom_headers=None,
                                                                                                raw=False)
        except QueryFailureException:
            summary_results = None

        return summary_results

    def summarize_for_policy_set_definition(self, credentials, subscription_id, policy_set_definition_name):
        policy_client = PolicyInsightsClient(credentials=credentials, base_url=None)
        #summarized_results = policy_client.policy_states.(subscription_id=subscription_id,
        #                                                                       policy_set_definition_name=policy_set_definition_name)