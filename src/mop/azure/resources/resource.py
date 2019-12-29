from configparser import ConfigParser
from dotenv import load_dotenv

from mop.azure.connections import request_authenticated_session, Connections
from mop.azure.utils.create_configuration import change_dir, OPERATIONSPATH, CONFVARIABLES


class Resource:
    def __init__(self):
        load_dotenv()
        self.credentials = Connections().get_authenticated_client()
        with change_dir(OPERATIONSPATH):
            self.config = ConfigParser()
            self.config.read(CONFVARIABLES)

    def list_resources(self, subscriptionId):
        """

        :return:
        """
        api_endpoint = self.config["AZURESDK"]["resourcelist"]
        api_endpoint = api_endpoint.format(subscriptionId=subscriptionId)
        with request_authenticated_session() as req:
            resource_group_function = req.post(api_endpoint).json

        return resource_group_function
