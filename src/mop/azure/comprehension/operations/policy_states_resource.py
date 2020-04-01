from configparser import ConfigParser

from dotenv import load_dotenv

from mop.framework.azure_connections import request_authenticated_azure_session
from mop.azure.utils.create_configuration import (
    change_dir,
    OPERATIONSPATH,
    CONFVARIABLES,
)


class PolicyStatesResource:
    def __init__(self):
        load_dotenv()
        with change_dir(OPERATIONSPATH):
            self.config = ConfigParser()
            self.config.read(CONFVARIABLES)

    def policy_states_summarize_for_resource(self, resourceId):
        """
            Calls Policy State Summarize for Resource in the Azure Framework
        :param resourceId:
        :return: a function
        """
        api_endpoint = self.config["AZURESDK"]["policystatessummarizeforresource"]
        api_endpoint = api_endpoint.format(resourceId=resourceId)

        with request_authenticated_azure_session() as req:
            resource_policy_function = req.post(api_endpoint).json
        return resource_policy_function
