from configparser import ConfigParser

from tenacity import retry, wait_random, stop_after_attempt
from dotenv import load_dotenv

from mop.azure.utils.create_configuration import change_dir, OPERATIONSPATH, CONFVARIABLES
from mop.framework.azure_connections import request_authenticated_azure_session, AzureConnections

class PolicyInsights2:
    def __init__(self, credentials=None):
        load_dotenv()
        with change_dir(OPERATIONSPATH):
            self.config = ConfigParser()
            self.config.read(CONFVARIABLES)

        self.credentials = AzureConnections().get_authenticated_client()

    @retry(wait=wait_random(min=1, max=3), stop=stop_after_attempt(4))
    def policy_states_summarize_for_subscription(self, subscriptionId):
        """
        This method calls the policy compliance using the policy insights and query policy state
        :rtype: response
        :param subscriptionId:
        :return:
        """
        api_endpoint = self.config["AZURESDK"]['policy_states_summarize_for_subscription']
        api_endpoint = api_endpoint.format(subscriptionId=subscriptionId)

        with request_authenticated_azure_session() as req:
            policy_states_summary = req.post(api_endpoint)

        return policy_states_summary

    @retry(wait=wait_random(min=1, max=3), stop=stop_after_attempt(4))
    def policy_states_summarize_for_policy_definition(self, subscription_id, policy_definition_name):
        api_endpoint = self.config["AZURESDK"]['policy_states_summarize_for_policy_definition']
        api_endpoint = api_endpoint.format(subscriptionId=subscription_id, policyDefinitionName=policy_definition_name)

        with request_authenticated_azure_session() as req:
            policy_states_summary = req.post(api_endpoint)

        return policy_states_summary
