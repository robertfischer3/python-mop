from mop.framework.azure_connections import request_authenticated_azure_session
from mop.framework.mopbase import MopBase


class Users(MopBase):

    def list_users(self):
        api_endpoint = self.config['AZURESDK']['graph_list_users']
        graph_version = self.config['AZURESDK']['graph_version']

        api_endpoint = api_endpoint.format(graph_version=graph_version)
        # with statement automatically closes the connection
        with request_authenticated_azure_session() as req:
            # Returns response object. The response object contains the HTTP status code, and the response of the service
            users = req.get(api_endpoint)
            return users

    def get_user(self, id):
        api_endpoint = self.config['AZURESDK']['graph_get_user']
        graph_version = self.config['AZURESDK']['graph_version']

        api_endpoint = api_endpoint.format(graph_version=graph_version, id=id)
        # with statement automatically closes the connection
        with request_authenticated_azure_session() as req:
            # Returns response object. The response object contains the HTTP status code, and the response of the service
            audits = req.get(api_endpoint)
            return audits
