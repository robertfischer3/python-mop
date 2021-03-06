from configparser import ConfigParser
from dotenv import load_dotenv

from mop.azure.utils.create_configuration import (
    CONFVARIABLES,
    change_dir,
    OPERATIONSPATH,
)
from mop.framework.azure_connections import request_authenticated_azure_session


class VNet:
    def __init__(self):
        load_dotenv()
        with change_dir(OPERATIONSPATH):
            self.config = ConfigParser()
            self.config.read(CONFVARIABLES)

    def vnets_list(self, subscription):
        api_endpoint = self.config["AZURESDK"]["VirtualNetworksList"]
        with request_authenticated_azure_session() as req:
            list_vnets_function = req.post(api_endpoint).json

        return list_vnets_function

    def vnets_list_all(self, resourceId):
        api_endpoint = self.config["AZURESDK"]["VirtualNetworksListAll"]
        api_endpoint = api_endpoint.format(resourceId=resourceId)

        with request_authenticated_azure_session() as req:
            resource_policy_function = req.post(api_endpoint).json
        return resource_policy_function

    def vnet_list_usage(self, subscription, policyDefinitionName):
        api_endpoint = ["AZURESDK"]["VirtualNetworksListUsage"]
        api_endpoint = api_endpoint.format(
            subscriptionId=subscription, policyDefinitionName=policyDefinitionName
        )
        with request_authenticated_azure_session() as req:
            vnet_list_usage_fuction = req.post(api_endpoint).json

        return vnet_list_usage_fuction
