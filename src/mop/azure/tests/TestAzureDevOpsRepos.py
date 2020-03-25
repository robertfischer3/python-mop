import json
import unittest
import os
from configparser import ConfigParser

import jmespath
from dotenv import load_dotenv

from mop.azure.utils.create_configuration import change_dir, OPERATIONSPATH, CONFVARIABLES
from mop.git.azure_devops.repos import AzureDevOpsRepos
from mop.git.azure_devops.refs import AzureDevOpsRefs
from mop.git.azure_devops.items import AzureDevOpsItems


class TestAzureDevOpsRepos(unittest.TestCase):
    def setUp(self) -> None:
        load_dotenv()
        with change_dir(OPERATIONSPATH):
            self.config = ConfigParser()
            self.config.read(CONFVARIABLES)

    def test_list(self):
        personal_access_token = os.environ['PAT']
        organization = os.environ['ORGANIZATION']
        project = self.config['GIT']['azure_project_01']
        repos_name = self.config['GIT']['azure_repository_name_01']

        devops = AzureDevOpsRepos(personal_access_token)
        respositories = devops.list(organization, project)
        if respositories.status_code >= 200 and respositories.status_code <= 299:
            repos = respositories.json()
            result = jmespath.search("value[?name == '{}']".format(repos_name), repos)
            if len(result) == 1:
                repos_id = result[0]['id']
                print(repos_id, repos_name)
                self.assertEqual(True, True)
        else:
            self.assertEqual(True, False)

    def test_list_refs(self):
        personal_access_token = os.environ['PAT']
        organization = os.environ['ORGANIZATION']
        project = self.config['GIT']['azure_project_01']
        repos_name = self.config['GIT']['azure_repository_name_01']

        devops = AzureDevOpsRepos(personal_access_token)
        respositories = devops.list(organization, project)
        if respositories.status_code >= 200 and respositories.status_code <= 299:
            repos = respositories.json()
            result = jmespath.search("value[?name == '{}']".format(repos_name), repos)
            if len(result) == 1:
                repos_id = result[0]['id']

                branches = AzureDevOpsRefs(personal_access_token)
                ref_list_response = branches.list(organization, project, repositoryId=repos_id, filterValue="Develop")
                if ref_list_response.status_code in range(200, 299):
                    print(ref_list_response.json())
                    self.assertEqual(True, True)
                else:
                    self.assertEqual(True, False)

    def test_list_items(self):
        personal_access_token = os.environ['PAT']
        organization = os.environ['ORGANIZATION']
        project = self.config['GIT']['azure_project_01']
        repos_name = self.config['GIT']['azure_repository_name_01']

        repos_id = self.config['GIT']['azure_repository_id_01']
        scopePath = self.config['GIT']['azure_scope_path_01']
        versionDescriptor_version = 'develop'

        devops_items = AzureDevOpsItems(personal_access_token)
        items_response = devops_items.get(organization, project, repos_id, scopePath, versionDescriptor_version)
        if items_response.status_code in range(200, 299):
            items = items_response.json()
            print(json.dumps(items, indent=4, ensure_ascii=False))
            self.assertEqual(True, True)
        else:
            self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
