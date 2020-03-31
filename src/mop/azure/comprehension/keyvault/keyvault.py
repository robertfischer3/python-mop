from mop.framework.azure_connections import request_authenticated_azure_session
from mop.framework.mopbase import MopBase


class KeyVault(MopBase):
    def get_keys(self, vaultBaseUrl):
        api_endpoint = self.config['AZURESDK']['keyvault_get_keys']
        api_endpoint = api_endpoint.format(vaultBaseUrl=vaultBaseUrl)
        # with statement automatically closes the connection
        with request_authenticated_azure_session() as req:
            # Returns response object. The response object contains the HTTP status code, and the response of the service
            keys = req.get(api_endpoint)
            return keys
