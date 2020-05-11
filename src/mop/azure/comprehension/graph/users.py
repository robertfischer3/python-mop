from mop.framework.microsoft_graph_connections import request_authenticated_graph_session
from mop.framework.mopbase import MopBase


class Users(MopBase):

    def list_users(self, select_columns_list):
        api_endpoint = self.config['AZURESDK']['graph_list_users']
        graph_version = self.config['AZURESDK']['graph_version']

        if len(select_columns_list):
            columns = ','.join(map(str, select_columns_list))
            select_statement = '?$select={}'.format(columns)
            api_endpoint = api_endpoint.format(graph_version=graph_version)
            api_endpoint = api_endpoint + select_statement
        else:
            api_endpoint = api_endpoint.format(graph_version=graph_version)
        # with statement automatically closes the connection
        with request_authenticated_graph_session() as req:
            # Returns response object. The response object contains the HTTP status code, and the response of the service
            users = req.get(api_endpoint)
            return users

    def get_user(self, id):
        api_endpoint = self.config['AZURESDK']['graph_get_user']
        graph_version = self.config['AZURESDK']['graph_version']

        api_endpoint = api_endpoint.format(graph_version=graph_version, id=id)
        # with statement automatically closes the connection
        with request_authenticated_graph_session() as req:
            # Returns response object. The response object contains the HTTP status code, and the response of the service
            audits = req.get(api_endpoint)
            return audits
