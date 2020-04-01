from configparser import ConfigParser

from dotenv import load_dotenv

from mop.framework.azure_connections import request_authenticated_azure_session
from mop.azure.utils.create_configuration import (
    change_dir,
    CONFVARIABLES,
    OPERATIONSPATH,
)


class AzureDevOpsRefs():

    def __init__(self, personal_access_token):
        load_dotenv()
        with change_dir(OPERATIONSPATH):
            self.config = ConfigParser()
            self.config.read(CONFVARIABLES)

        self.personal_access_token = personal_access_token

    def list(self, organization, project, repositoryId, filterValue):
        api_endpoint = self.config["GIT"]['azure_devops_refs_list']
        api_endpoint = api_endpoint.format(organization=organization,
                                           project=project, repositoryId=repositoryId, filterValue=filterValue)

        with request_authenticated_azure_session() as req:
            refs_list = req.get(api_endpoint, auth=('', self.personal_access_token))

        return refs_list
