from mop.framework.microsoft_graph_connections import request_authenticated_graph_session
from mop.framework.mopbase import MopBase


class DirectoryAudit(MopBase):

    def graph_directory_list_audits(self):
        api_endpoint = self.config['AZURESDK']['graph_directory_list_audits']
        graph_version = self.config['AZURESDK']['graph_version']

        api_endpoint = api_endpoint.format(graph_version=graph_version)
        # with statement automatically closes the connection
        with request_authenticated_graph_session() as req:
            # Returns response object. The response object contains the HTTP status code, and the response of the service
            audits = req.get(api_endpoint)
            return audits

    def graph_directory_get_audit(self, id):
        api_endpoint = self.config['AZURESDK']['graph_directory_list_audits']
        graph_version = self.config['AZURESDK']['graph_version']

        api_endpoint = api_endpoint.format(graph_version=graph_version, id=id)
        # with statement automatically closes the connection
        with request_authenticated_graph_session() as req:
            # Returns response object. The response object contains the HTTP status code, and the response of the service
            audits = req.get(api_endpoint)
            return audits

    def graph_directory_list_signins(self):
        api_endpoint = self.config['AZURESDK']['graph_directory_list_signins']
        graph_version = self.config['AZURESDK']['graph_version']

        api_endpoint = api_endpoint.format(graph_version=graph_version)
        # with statement automatically closes the connection
        with request_authenticated_graph_session() as req:
            # Returns response object. The response object contains the HTTP status code, and the response of the service
            signins = req.get(api_endpoint)
            return signins

    def graph_directory_get_signin(self, id):
        api_endpoint = self.config['AZURESDK']['graph_directory_get_signin']
        graph_version = self.config['AZURESDK']['graph_version']

        api_endpoint = api_endpoint.format(graph_version=graph_version, id=id)
        # with statement automatically closes the connection
        with request_authenticated_graph_session() as req:
            # Returns response object. The response object contains the HTTP status code, and the response of the service
            signin = req.get(api_endpoint)
            return signin
