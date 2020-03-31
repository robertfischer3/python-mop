from mop.framework.azure_connections import request_authenticated_azure_session
from mop.framework.mopbase import MopBase


class Vaults(MopBase):
    def list(self, subscriptionId, api_version=None):
        api_endpoint = self.config['AZURESDK']['vaults_list']
        if api_version is None:
            api_version = self.config['AZURESDK']['apiversion']

        api_endpoint = api_endpoint.format(subscriptionId=subscriptionId, apiversion=api_version)
        # with statement automatically closes the connection
        with request_authenticated_azure_session() as req:
            # Returns response object. The response object contains the HTTP status code, and the response of the service
            vaults = req.get(api_endpoint)
            return vaults

    def list_by_subscription(self, subscriptionId, api_version=None):
        api_endpoint = self.config['AZURESDK']['vaults_list_by_subscription']
        if api_version is None:
            api_version = self.config['AZURESDK']['apiversion']

        api_endpoint = api_endpoint.format(subscriptionId=subscriptionId, apiversion=api_version)
        # with statement automatically closes the connection
        with request_authenticated_azure_session() as req:
            # Returns response object. The response object contains the HTTP status code, and the response of the service
            vaults = req.get(api_endpoint)
            return vaults

    def get_by_id(self, id, api_version=None):
        api_endpoint = self.config['AZURESDK']['vaults_get_by_id']
        management_root = self.config['AZURESDK']['management_root']
        if api_version is None:
            api_version = self.config['AZURESDK']['apiversion']

        api_endpoint = api_endpoint.format(management_root=management_root, id=id, apiversion=api_version)
        # with statement automatically closes the connection
        with request_authenticated_azure_session() as req:
            # Returns response object. The response object contains the HTTP status code, and the response of the service
            vault = req.get(api_endpoint)
            return vault
