import os
from configparser import ConfigParser
import random
from tenacity import retry, wait_random, stop_after_attempt
from azure.mgmt.policyinsights.models import QueryFailureException
from azure.mgmt.policyinsights.models import QueryOptions
from azure.mgmt.policyinsights.policy_insights_client import PolicyInsightsClient
from dotenv import load_dotenv

from mop.azure.connections import request_authenticated_session
from mop.azure.utils.create_configuration import (
    CONFVARIABLES,
    change_dir,
    OPERATIONSPATH,
)


class PolicyStates:
    def __init__(self):
        load_dotenv()
        with change_dir(OPERATIONSPATH):
            self.config = ConfigParser()
            self.config.read(CONFVARIABLES)

    def policystates_genericfunc(self, api_endpoint, *args):
        """
            This function can theoretically call any Azure SDK API the service pricipal has access to
        :param api_config_key:
        :param args:
        :return:
        """
        # The policystates_genericfunc has no way of learning the named string format parameters
        # a simple replace makes the URL a workable generic call to the API
        # example: api_config_key.replace('{subscriptionId}', '{}')

        api_endpoint = api_endpoint.format(*args)

        with request_authenticated_session() as req:
            return req.post(api_endpoint).json

    def policy_states_summarize_for_policy_definition(self, subscriptionId, policyDefinitionName):
        """
        Summarizes policy states for the subscription level policy definition.
        https://docs.microsoft.com/en-us/rest/api/policy-insights/policystates/summarizeforpolicydefinition#code-try-0
        :param subscriptionId:
        :param policyDefinitionName:
        :return:
        """
        api_endpoint = self.config["AZURESDK"]["policy_states_summarize_for_policy_definition"]
        api_endpoint = api_endpoint.format(subscriptionId=subscriptionId, policyDefinitionName=policyDefinitionName)

        with request_authenticated_session() as req:
            policy_states_summarize_for_policy_definition = req.post(api_endpoint)

        return policy_states_summarize_for_policy_definition

    def policy_states_summarize_for_resourcegroup(self, subscriptionId):
        """

        :param subscriptionId:
        :return:
        """
        api_endpoint = self.config["AZURESDK"]["policy_states_summarize_for_resource_group"]
        api_endpoint = api_endpoint.format(subscriptionId=subscriptionId)

        with request_authenticated_session() as req:
            summarized_resource_group_function = req.post(api_endpoint).json

        return summarized_resource_group_function

    def policy_states_list_query_results_for_policy_definitions(self, subscription_id, policy_definition_name,
                                                                authenticated_session=None,
                                                                policy_states_resource='latest'):
        try:

            api_endpoint = self.config["AZURESDK"]["policy_states_list_query_results_for_policy_definitions"]
            api_endpoint = api_endpoint.format(subscriptionId=subscription_id,
                                               policyDefinitionName=policy_definition_name,
                                               policyStatesResource=policy_states_resource)

            query_results_for_policy_definitions_function = None

            if authenticated_session:
                query_results_for_policy_definitions_function = authenticated_session.post(api_endpoint).json
            else:
                with request_authenticated_session() as req:
                    query_results_for_policy_definitions_function = req.post(api_endpoint).json

        except UnboundLocalError:
            pass
        finally:
            return query_results_for_policy_definitions_function

    def policy_states_summarize_for_resource(self, resourceId):
        """

        :param resourceId:
        :return: function
        """

        api_endpoint = self.config["AZURESDK"]["policystatessummarizeforresource"]
        api_endpoint = api_endpoint.format(resourceId=resourceId)

        with request_authenticated_session() as req:
            resource_policy_function = req.post(api_endpoint).json
        return resource_policy_function

    def policy_states_summarize_for_subscription_query(self):
        """

        :param subscription:
        :return:
        """
        api_endpoint = self.config["AZURESDK"]["policystatessummarizeforsubscriptionquery"]
        with request_authenticated_session() as req:
            policy_states_summary_subscription = req.post(api_endpoint).json

        return policy_states_summary_subscription

    def policy_states_list_query_results_for_management_group(self, management_grp, policyStatesResource='latest'):

        api_endpoint = self.config["AZURESDK"]["policy_states_list_query_results_for_management_group"]
        api_endpoint = api_endpoint.format(managementGroupName=management_grp,
                                           policyStatesResource=policyStatesResource)
        with request_authenticated_session() as req:
            policy_states_summary_subscription = req.post(api_endpoint).json

        return policy_states_summary_subscription

    @retry(wait=wait_random(min=1, max=2), stop=stop_after_attempt(4))
    def policy_states_summarize_for_subscription(self, subscription):
        """

        :return:
        :param subscription:
        :return:
        """
        api_endpoint = self.config["AZURESDK"]["policy_states_summarize_for_subscription"]
        api_endpoint = api_endpoint.format(subscriptionId=subscription)

        with request_authenticated_session() as req:
            policy_states_summary_subscription_response = req.post(api_endpoint)

        return policy_states_summary_subscription_response

    def policy_states_summarize_for_subscription_compliant(
        self, subscriptionId, is_compliant="true"
    ):

        filter_condition = "IsCompliant eq {}".format(is_compliant)

        api_endpoint = self.config["AZURESDK"][
            "PolicyStatesSummarizeForSubscriptionFiltered"
        ]
        api_endpoint = api_endpoint.format(
            subscriptionId=subscriptionId, filter=filter_condition
        )

        with request_authenticated_session() as req:
            policy_states_summary_subscription = req.post(api_endpoint).json

        return policy_states_summary_subscription

    def policy_states_filter_and_multiple_groups(self, subscriptionId):

        api_endpoint = self.config["AZURESDK"]["policy_states_filter_and_multiple_groups"]
        api_endpoint = api_endpoint.format(subscriptionId=subscriptionId)

        with request_authenticated_session() as req:
            r_policy_states_filter_and_multiple_groups = req.post(api_endpoint).json()

        return r_policy_states_filter_and_multiple_groups

    def policy_states_filter_and_multiple_groups_compliant(self, subscriptionId):
        """

        :param subscriptionId:
        :return: function
        """
        api_endpoint = self.config["AZURESDK"]["policy_states_filter_and_multiple_groups"]
        api_endpoint = api_endpoint.format(subscriptionId=subscriptionId)

        with request_authenticated_session() as req:
            r_policy_states_filter_and_multiple_groups = req.post(api_endpoint).json

        return r_policy_states_filter_and_multiple_groups

    def summarize_for_subscription(self, creds, subscription_id):
        """

        :param creds:
        :param subscription_id:
        :return:
        """
        policy_client = PolicyInsightsClient(credentials=creds, base_url=None)
        summarized_results = policy_client.policy_states.summarize_for_subscription(
            subscription_id
        )

        return summarized_results

    def list_query_results_for_subscription_wrapper(
        self, credentials, subscription_id, policy_assignment_name
    ):
        """

        :param credentials:
        :param subscription_id:
        :param policy_assignment_name:
        :return:
        """
        query = QueryOptions(filter="IsCompliant eq false")
        policy_client = PolicyInsightsClient(credentials=credentials, base_url=None)

        try:

            summary_results = policy_client.policy_states.list_query_results_for_subscription(
                "latest",
                subscription_id=subscription_id,
                policy_definition_name=policy_assignment_name,
                custom_headers=None,
                raw=False,
            )
        except QueryFailureException:
            summary_results = None

        return summary_results
