from azure.mgmt.resource.policy import PolicyClient
from azure.mgmt.policyinsights import PolicyInsightsClient

from dotenv import load_dotenv

from mop.framework.azure_connections import request_authenticated_azure_session


class PolicyInsights:
    def __init__(self, credentials):
        load_dotenv()
        self.credentials = credentials
        self.subscriptions = None
        self.policy_insights = None

    def policyinsights_genericfunc(self, api_endpoint, *args):
        """
            This function can theoretically call any Azure SDK API the service pricipal has access to
        :param api_config_key:
        :param args:
        :return:
        """
        # The policyinsights_generic_req has no way of learning the named string format parameters
        # a simple replace makes the URL a workable generic call to the API
        # example: api_config_key.replace('{subscriptionId}', '{}')

        api_endpoint = api_endpoint.format(*args)

        with request_authenticated_azure_session() as req:
            return req.post(api_endpoint).json()

    def policy_insights_client_query(
        self, subscription_id_param, policy_states="latest"
    ):
        """
        Grabs the policy states for a give subscription
        :param policy_states:
        :param creds:
        :param subscription_id_param:
        :return:
        """
        policy_insights_client = PolicyInsightsClient(credentials=self.credentials)
        states = policy_insights_client.policy_states

        query_results = states.list_query_results_for_subscription(
            subscription_id=subscription_id_param, policy_states_resource=policy_states
        )

        return query_results.value


    def policy_insights_management_grp_query(
        self, management_group_name, policy_states="latest", query_options=None
    ):
        """
        Retrieve policy insights for a particular management group. Returns policy insights with policy states
        :param policy_states:
        :param creds:
        :param management_group_name:
        :return:
        """
        policy_insights_client = PolicyInsightsClient(credentials=self.credentials)
        states = policy_insights_client.policy_states

        query_results = states.list_query_results_for_management_group(
            policy_states_resource=policy_states,
            management_group_name=management_group_name,
            query_options=query_options,
            custom_headers=None,
            raw=False,
        )
        return query_results.value

    def subscription_policy_list(self, subscription_id_param) -> list:
        """
        Returns a list of policy definitions for a given subscription
        :param subscription_id_param:
        :return:
        """
        policy_client = PolicyClient(
            credentials=self.credentials,
            subscription_id=subscription_id_param,
            base_url=None,
        )
        policy_definitions = policy_client.policy_definitions.list(
            custom_headers=None, raw=False
        )
        policy_defs_limited = [
            [
                policy.metadata.get("category"),
                policy.policy_type,
                policy.display_name,
                policy.name,
                policy.description,
            ]
            for policy in policy_definitions
        ]

        return policy_defs_limited

    @staticmethod
    def mapped_columns_policy_insights(raw_policy_insights_management_grp_query):
        """

        :param raw_policy_insights_management_grp_query:
        :return:list
        """
        policy_insights = raw_policy_insights_management_grp_query
        if not policy_insights:
            return None

        mapped_policy_insights = [
            [
                policy_insight.is_compliant,
                policy_insight.resource_id,
                policy_insight.management_group_ids,
                policy_insight.policy_assignment_id,
                policy_insight.policy_assignment_name,
                policy_insight.policy_assignment_owner,
                policy_insight.policy_assignment_parameters,
                policy_insight.policy_assignment_scope,
                policy_insight.policy_definition_action,
                policy_insight.policy_definition_category,
                policy_insight.policy_definition_id,
                policy_insight.policy_definition_name,
                policy_insight.policy_definition_reference_id,
                policy_insight.policy_set_definition_category,
                policy_insight.policy_set_definition_id,
                policy_insight.policy_set_definition_name,
                policy_insight.policy_set_definition_owner,
                policy_insight.policy_set_definition_parameters,
                policy_insight.resource_group,
                policy_insight.resource_location,
                policy_insight.resource_tags,
                policy_insight.resource_type,
                policy_insight.serialize,
                policy_insight.subscription_id,
                policy_insight.timestamp,
            ]
            for policy_insight in policy_insights
        ]

        return mapped_policy_insights

    @staticmethod
    def get_row_names():
        """
        Returns the columns we are interested in evaluating
        :return:
        """
        fieldnames = [
            "is_compliant",
            "resource_id",
            "management_group_ids",
            "policy_assignment_id",
            "policy_assignment_name",
            "policy_assignment_owner",
            "policy_assignment_parameters",
            "policy_assignment_scope",
            "policy_definition_action",
            "policy_definition_category",
            "policy_definition_id",
            "policy_definition_name",
            "policy_definition_reference_id",
            "policy_set_definition_category",
            "policy_set_definition_id",
            "policy_set_definition_name",
            "policy_set_definition_owner",
            "policy_set_definition_parameters",
            "resource_group",
            "resource_location",
            "resource_tags",
            "resource_type",
            "serialize",
            "subscription_id",
            "timestamp",
        ]

        return fieldnames
