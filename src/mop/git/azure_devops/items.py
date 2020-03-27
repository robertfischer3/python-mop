from mop.azure.connections import request_authenticated_session
from mop.git.azure_devops.devops_base import AzureDevOpsBase


class AzureDevOpsItems(AzureDevOpsBase):

    def get(self, organization, project, repositoryId, scopePath, versionDescriptor_version):
        api_endpoint = self.config["GIT"]['azure_devops_items_list']
        recursionLevel = 'Full'
        includeLinks = 'true'
        api_endpoint = api_endpoint.format(organization=organization,
                                           project=project,
                                           repositoryId=repositoryId,
                                           scopePath=scopePath,
                                           recursionLevel=recursionLevel,
                                           includeLinks=includeLinks,
                                           versionDescriptor_version=versionDescriptor_version)

        with request_authenticated_session() as req:
            items = req.get(api_endpoint, auth=('', self.personal_access_token))

        return items

    def memory_download_file(self, URL):
        with request_authenticated_session() as req:
            file = req.get(URL, auth=('', self.personal_access_token))
