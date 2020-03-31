from configparser import ConfigParser
from dotenv import load_dotenv

from mop.framework.azure_connections import AzureConnections, request_authenticated_azure_session
from mop.azure.utils.create_configuration import (
    change_dir,
    CONFVARIABLES,
    OPERATIONSPATH,
)


class PolicyAssignments():
    def __init__(self, credentials=None):
        load_dotenv()
        with change_dir(OPERATIONSPATH):
            self.config = ConfigParser()
            self.config.read(CONFVARIABLES)

        self.credentials = AzureConnections().get_authenticated_client()

    def policy_assignments_list(self, subscriptionId):
        """

        :param subscriptionId:
        :return: Policy definitions by subscription request
        """
        api_endpoint = self.config["AZURESDK"]["policy_assignments_list"]
        api_endpoint = api_endpoint.format(subscriptionId=subscriptionId)

        with request_authenticated_azure_session() as req:
            policy_assignments_request = req.get(api_endpoint)

        return policy_assignments_request
