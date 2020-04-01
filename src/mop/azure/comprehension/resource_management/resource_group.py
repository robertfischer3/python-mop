from configparser import ConfigParser

from dotenv import load_dotenv

from mop.framework.azure_connections import request_authenticated_azure_session, AzureConnections
from mop.azure.utils.create_configuration import change_dir, OPERATIONSPATH, CONFVARIABLES


class ResourceGroup:
    def __init__(self):
        load_dotenv()
        self.credentials = AzureConnections().get_authenticated_client()
        with change_dir(OPERATIONSPATH):
            self.config = ConfigParser()
            self.config.read(CONFVARIABLES)

    def list_resourcegroup(self, subscriptionId):
        """

        :return:
        """
        api_endpoint = self.config["AZURESDK"]["resourcegroupslist"]
        api_endpoint = api_endpoint.format(subscriptionId=subscriptionId)
        with request_authenticated_azure_session() as req:
            resource_group_function = req.post(api_endpoint).json

        return resource_group_function

