from configparser import ConfigParser
from contextlib import contextmanager
import os

from dotenv import load_dotenv

from mop.azure.utils.atomic_writes import atomic_write

CONFVARIABLES = "app.config.ini"
OPERATIONSPATH = "../../../.."
TESTVARIABLES = "test.app.config.ini"
TESTINGPATH = "../../../.."


@contextmanager
def change_dir(destination):
    try:
        cwd = os.getcwd()
        os.chdir(destination)
        yield
    finally:
        os.chdir(cwd)

def create_baseline_configuration(generate_test=True):
    """
        The method creates the api configuration file for Azure API calls.  As Microsoft changes
    :return:
    """
    load_dotenv()
    config = ConfigParser()

    config["DEFAULT"] = {
        "subscription_id": os.environ["SUB"],
        "management_grp_id": os.environ["MANGRP"],
        "tenant_id": os.environ["TENANT"],
        "organization": os.environ["ORGANIZATION"],
        'plugin_root_path': 'src/mop/azure/plugins/',
    }
    """
    The configuration file supports multiple database instances
    """
    config["SQLSERVER"] = {"instance01":{
        'server':'tcp:172.17.0.1',
        'database':'TestDB2',
        'username': 'robert',
        'db_driver':'{ODBC Driver 17 for SQL Server}',
        'dialect':'mssql'
    }
    }
    config["FILTERS"] = {
        "policy_definition_category": "Security",
        "policy_definition_name_01": ""
    }
    config["LOGGING"] = {"level": "20"}
    config["AZURESDK"] = {
        'apiversion': '2019-09-01',
        'graph_version': 'v1.0',
        'get_policy_definition_by_name': 'https://management.azure.com/providers/Microsoft.Authorization/policyDefinitions/{policyDefinitionName}?api-version=2019-09-01',
        'listqueryresultsformanagementgroup': 'https://management.azure.com/providers/Microsoft.Management/managementGroups/{managementGroupName}/providers/Microsoft.PolicyInsights/policyStates/{policyStatesResource}/queryResults?api-version=2018-04-04',
        'management_root': 'https://management.azure.com',
        'policy_assignments_create': 'https://management.azure.com/subscriptions/{subscriptionId}/providers/Microsoft.Authorization/policyAssignments/{policyAssignmentName}?api-version=2019-09-01',
        'policy_assignments_list': 'https://management.azure.com/subscriptions/{subscriptionId}/providers/Microsoft.Authorization/policyAssignments?api-version=2019-09-01',
        'policy_definitions_create_or_update': 'https://management.azure.com/subscriptions/{subscriptionId}/providers/Microsoft.Authorization/policyDefinitions/{policyDefinitionName}?api-version=2019-09-01',
        'policy_definitions_create_or_update_at_management_group': 'https://management.azure.com/providers/Microsoft.Management/managementgroups/{managementGroupId}/providers/Microsoft.Authorization/policyDefinitions/{policyDefinitionName}?api-version=2019-09-01',
        'policy_definitions_get': 'https://management.azure.com/subscriptions/{subscriptionId}/providers/Microsoft.Authorization/policyDefinitions/{policyDefinitionName}?api-version=2019-09-01',
        'policy_definitions_get_at_management_group': 'https://management.azure.com/providers/Microsoft.Management/managementgroups/{managementGroupId}/providers/Microsoft.Authorization/policyDefinitions/{policyDefinitionName}?api-version=2019-09-01',
        'policy_definitions_list': 'https://management.azure.com/subscriptions/{subscriptionId}/providers/Microsoft.Authorization/policyDefinitions?api-version=2019-09-01',
        'policy_definitions_list_by_management_group': 'https://management.azure.com/providers/Microsoft.Management/managementgroups/{managementGroupId}/providers/Microsoft.Authorization/policyDefinitions?api-version=2019-09-01',
        'policy_defintions_by_subscription': 'https://management.azure.com/subscriptions/{subscriptionId}/providers/Microsoft.Authorization/policyDefinitions?api-version=2019-09-01',
        'policy_insights_operations_list': 'https://management.azure.com/providers/Microsoft.PolicyInsights/operations?api-version=2018-04-04',
        'policy_set_definitions_create_or_update': 'https://management.azure.com/subscriptions/{subscriptionId}/providers/Microsoft.Authorization/policySetDefinitions/{policySetDefinitionName}?api-version=2019-09-01',
        'policy_set_definitions_list': 'https://management.azure.com/subscriptions/{subscriptionId}/providers/Microsoft.Authorization/policySetDefinitions?api-version=2019-09-01',
        'policy_states_filter_and_multiple_groups': 'https://management.azure.com/subscriptions/{subscriptionId}/providers/Microsoft.PolicyInsights/policyStates/latest/queryResults?api-version=2018-04-04&$top=10&$orderby=NumNonCompliantResources desc&$filter=IsCompliant eq false&$apply=groupby((PolicyAssignmentId, PolicySetDefinitionId, PolicyDefinitionId, PolicyDefinitionReferenceId, ResourceId))/groupby((PolicyAssignmentId, PolicySetDefinitionId, PolicyDefinitionId, PolicyDefinitionReferenceId), aggregate($count as NumNonCompliantResources))',
        'policy_states_filter_and_multiple_groups_true': 'https://management.azure.com/subscriptions/{subscriptionId}/providers/Microsoft.PolicyInsights/policyStates/latest/queryResults?api-version=2018-04-04&$top=10&$orderby=NumNonCompliantResources desc&$filter=IsCompliant eq true&$apply=groupby((PolicyAssignmentId, PolicySetDefinitionId, PolicyDefinitionId, PolicyDefinitionReferenceId, ResourceId))/groupby((PolicyAssignmentId, PolicySetDefinitionId, PolicyDefinitionId, PolicyDefinitionReferenceId), aggregate($count as NumNonCompliantResources))',
        'policy_states_list_query_results_for_policy_definitions': 'https://management.azure.com/subscriptions/{subscriptionId}/providers/Microsoft.Authorization/policyDefinitions/{policyDefinitionName}/providers/Microsoft.PolicyInsights/policyStates/{policyStatesResource}/queryResults?api-version=2019-10-01',
        'policy_states_summarize_for_policy_definition': 'https://management.azure.com/subscriptions/{subscriptionId}/providers/Microsoft.Authorization/policyDefinitions/{policyDefinitionName}/providers/Microsoft.PolicyInsights/policyStates/latest/summarize?api-version=2019-10-01',
        'policy_states_summarize_for_resource_group': 'https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.PolicyInsights/policyStates/latest/summarize?api-version=2019-10-01',
        'policy_states_summarize_for_subscription': 'https://management.azure.com/subscriptions/{subscriptionId}/providers/Microsoft.PolicyInsights/policyStates/latest/summarize?api-version=2019-10-01',
        'policy_states_summarize_for_subscription_filtered': 'https://management.azure.com/subscriptions/{subscriptionId}/providers/Microsoft.PolicyInsights/policyStates/latest/summarize?api-version=2019-10-01&$filter={filter}',
        'policy_states_summarize_for_subscription_level_policy_assignment': 'https://management.azure.com/subscriptions/{subscriptionId}/providers/Microsoft.Authorization/policyAssignments/{policyAssignmentName}/providers/Microsoft.PolicyInsights/policyStates/latest/summarize?api-version=2019-10-01',
        'policystateslistqueryresultsformanagementgroup': 'https://management.azure.com/providers/Microsoft.Management/managementGroups/{managementGroupName}/providers/Microsoft.PolicyInsights/policyStates/{policyStatesResource}/queryResults?api-version=2019-10-01',
        'resourcegroupslist': 'https://management.azure.com/subscriptions/{subscriptionId}/resourcegroups?api-version=2019-08-01',
        'resourcelist': 'https://management.azure.com/subscriptions/{subscriptionId}/resources?api-version=2019-08-01',
        'subscriptions': 'https://management.azure.com/subscriptions?api-version=2019-06-01',
        'tags_list': 'https://management.azure.com/subscriptions/{subscriptionId}/tagNames?api-version=2019-10-01',
        'virtual_networks_list': 'https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Network/virtualNetworks?api-version=2019-09-01',
        'virtual_networks_list_all': 'https://management.azure.com/subscriptions/{subscriptionId}/providers/Microsoft.Network/virtualNetworks?api-version=2019-09-01',
        'virtual_networks_list_usage': 'https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Network/virtualNetworks/{virtualNetworkName}/usages?api-version=2019-09-01',
        'azure_devops_repositories_list': 'https://dev.azure.com/{organization}/{project}/_apis/git/repositories?api-version=5.1',
        'vaults_list': "https://management.azure.com/subscriptions/{subscriptionId}/resources?$filter=resourceType eq 'Microsoft.KeyVault/vaults'&api-version={apiversion}",
        'vaults_list_by_subscription': 'https://management.azure.com/subscriptions/{subscriptionId}/providers/Microsoft.KeyVault/vaults?api-version={apiversion}',
        'vaults_get_by_id': '{management_root}{id}?api-version={apiversion}',
        'keyvault_get': '{vaultBaseUrl}/keys/{key-name}/{key-version}?api-version=7.0',
        'keyvault_get_keys': '{vaultBaseUrl}/keys?api-version = 7.0',
        'graph_directory_list_audits': "https://graph.microsoft.com/{graph_version}/auditLogs/directoryAudits",
        'graph_directory_get_audit': 'https://graph.microsoft.com/{graph_version}/auditLogs/directoryAudits/{id}',
        'graph_directory_list_signins': 'https://graph.microsoft.com/{graph_version}/auditLogs/signIns',
        'graph_directory_get_signin': 'https://graph.microsoft.com/{graph_version}/auditLogs/signIns/{id}',
        'graph_list_users': 'https://graph.microsoft.com/{graph_version}/users',
        'graph_get_user': 'https://graph.microsoft.com/{graph_version}/users/{id}',
        'graph_get_user_upn': 'https://graph.microsoft.com/{graph_version}/users/{userPricipalName}'
    }
    config["PRISMACLOUD"] = {
        'api2_eu_login': 'https://api2.eu.prismacloud.io/login',
        'api2_eu': 'https://api2.eu.prismacloud.io',
        'policy': '{cloud_api}/policy',
        'compliance': '{cloud_api}/compliance',
        'filter_policy_suggest': '{cloud_api}/filter/policy/suggest'
    }

    config["PLUGINS"] = {
        'plugin_python_policies': 'pypolicy/glbl_pr_sec*.py',
        'plugin_database': 'test_db_plugin'
    }
    config["GIT"] = {
        'azure_project_01': 'testproject',
        'azure_repository_id_01': 'b3e721c7-0a2a-4712-b37a-2df3ce32f4cf',
        'azure_repository_name_01': 'testrepo',
        'azure_scope_path_01': '/cloud/azure/policy/security',
        'azure_devops_organization_url': '',
        'azure_devops_repositories_list': 'https://dev.azure.com/{organization}/{project}/_apis/git/repositories?api-version=5.1',
        'azure_devops_repository_get': 'https://dev.azure.com/{organization}/{project}/_apis/git/repositories/{repositoryId}?api-version=5.1',
        'azure_devops_refs_list': 'https://dev.azure.com/{organization}/{project}/_apis/git/repositories/{repositoryId}/refs?filter=heads/&filterContains={filterValue}&api-version=5.1',
        'azure_devops_items_list': 'https://dev.azure.com/{organization}/{project}/_apis/git/repositories/{repositoryId}/items?scopePath={scopePath}&recursionLevel={recursionLevel}&includeLinks={includeLinks}&versionDescriptor.version={versionDescriptor_version}&api-version=5.1'

    }
    with atomic_write(CONFVARIABLES, "w") as configfile:
        config.write(configfile)

    if generate_test:
        with atomic_write(TESTVARIABLES, "w") as testconfigfile:
            config.write(testconfigfile)

def main():
    create_baseline_configuration()

if __name__ == "__main__":
    main()
