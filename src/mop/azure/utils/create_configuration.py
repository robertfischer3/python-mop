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
    }
    """
    The configuration file supports multiple database instances
    """
    config["SQLSERVER"] = {"instance01":{
        'server':'tcp:172.17.0.1',
        'database':'TestDB2',
        'username': 'SA',
        'db_driver':'{ODBC Driver 17 for SQL Server}',
        'dialect':'mssql'
    }
    }
    config["FILTERS"] = {
        "policy_defition_category": "Security",
        "policy_definition_name_01": ""
    }
    config["LOGGING"] = {"level": "20"}
    config["AZURESDK"] = {
        "management_root":"https://management.azure.com",
        "apiversion":"2019-09-01",
        "PolicyStatesSummarizeForSubscription": "https://management.azure.com/subscriptions/{subscriptionId}/providers/Microsoft.PolicyInsights/policyStates/latest/summarize?api-version=2019-10-01",
        "PolicyStatesSummarizeForSubscriptionFiltered": "https://management.azure.com/subscriptions/{subscriptionId}/providers/Microsoft.PolicyInsights/policyStates/latest/summarize?api-version=2019-10-01&$filter={filter}",
        "Subscriptions": "https://management.azure.com/subscriptions?api-version=2019-06-01",
        "PolicyStatesFilterandmultiplegroups": "https://management.azure.com/subscriptions/{subscriptionId}/providers/Microsoft.PolicyInsights/policyStates/latest/queryResults?api-version=2018-04-04&$top=10&$orderby=NumNonCompliantResources desc&$filter=IsCompliant eq false&$apply=groupby((PolicyAssignmentId, PolicySetDefinitionId, PolicyDefinitionId, PolicyDefinitionReferenceId, ResourceId))/groupby((PolicyAssignmentId, PolicySetDefinitionId, PolicyDefinitionId, PolicyDefinitionReferenceId), aggregate($count as NumNonCompliantResources))",
        "PolicyStatesFilterandmultiplegroupsTrue": "https://management.azure.com/subscriptions/{subscriptionId}/providers/Microsoft.PolicyInsights/policyStates/latest/queryResults?api-version=2018-04-04&$top=10&$orderby=NumNonCompliantResources desc&$filter=IsCompliant eq true&$apply=groupby((PolicyAssignmentId, PolicySetDefinitionId, PolicyDefinitionId, PolicyDefinitionReferenceId, ResourceId))/groupby((PolicyAssignmentId, PolicySetDefinitionId, PolicyDefinitionId, PolicyDefinitionReferenceId), aggregate($count as NumNonCompliantResources))",
        "ListQueryResultsForManagementGroup": "https://management.azure.com/providers/Microsoft.Management/managementGroups/{managementGroupName}/providers/Microsoft.PolicyInsights/policyStates/{policyStatesResource}/queryResults?api-version=2018-04-04",
        "PolicyInsightsOperationsList": "PolicyInsightsOperationsList=https://management.azure.com/providers/Microsoft.PolicyInsights/operations?api-version=2018-04-04",
        "VirtualNetworksList": "https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Network/virtualNetworks?api-version=2019-09-01",
        "VirtualNetworksListAll": "https://management.azure.com/subscriptions/{subscriptionId}/providers/Microsoft.Network/virtualNetworks?api-version=2019-09-01",
        "VirtualNetworksListUsage": "https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Network/virtualNetworks/{virtualNetworkName}/usages?api-version=2019-09-01",
        "PolicyStatesSummarizeForSubscriptionQuery":"https://management.azure.com/subscriptions/82746ea2-9f97-4313-b21a-e9bde3a0a241/providers/Microsoft.PolicyInsights/policyStates/latest/queryResults?api-version=2019-10-01&$from=2019-12-17 20:12:48Z&$to=2019-12-18 20:12:48Z and PolicyAssignmentId eq '/providers/microsoft.management/managementgroups/12a3af23-a769-4654-847f-958f3d479f4a/providers/microsoft.authorization/policyassignments/95b344047fdf442fa4172383' and PolicyDefinitionId eq '/providers/microsoft.authorization/policydefinitions/c8343d2f-fdc9-4a97-b76f-fc71d1163bfc' and PolicyDefinitionReferenceId eq 'sqlserveradvanceddatasecurityemailadminsmonitoring",
        "PolicyStatesSummarizeForResourceGroup":"https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.PolicyInsights/policyStates/latest/summarize?api-version=2019-10-01",
        "resourcegroupslist":"https://management.azure.com/subscriptions/{subscriptionId}/resourcegroups?api-version=2019-08-01",
        "resourcelist":"https://management.azure.com/subscriptions/{subscriptionId}/resources?api-version=2019-08-01",
        "policy_defintions_by_subscription":"https://management.azure.com/subscriptions/{subscriptionId}/providers/Microsoft.Authorization/policyDefinitions?api-version=2019-09-01",
        "policystateslistqueryresultsformanagementgroup": 'https://management.azure.com/providers/Microsoft.Management/managementGroups/{managementGroupName}/providers/Microsoft.PolicyInsights/policyStates/{policyStatesResource}/queryResults?api-version=2019-10-01',
        "policy_states_list_query_results_for_policy_definitions":"https://management.azure.com/subscriptions/{subscriptionId}/providers/Microsoft.Authorization/policyDefinitions/{policyDefinitionName}/providers/Microsoft.PolicyInsights/policyStates/{policyStatesResource}/queryResults?api-version=2019-10-01",
        "policy_definitions_list_by_management_group":"https://management.azure.com/providers/Microsoft.Management/managementgroups/{managementGroupId}/providers/Microsoft.Authorization/policyDefinitions?api-version=2019-09-01",
        "policy_definitions_get":"https://management.azure.com/subscriptions/{subscriptionId}/providers/Microsoft.Authorization/policyDefinitions/{policyDefinitionName}?api-version=2019-09-01",
        "get_policy_definition_by_name":"https://management.azure.com/providers/Microsoft.Authorization/policyDefinitions/{policyDefinitionName}?api-version=2019-09-01",
        "policy_assignments_list":"https://management.azure.com/subscriptions/{subscriptionId}/providers/Microsoft.Authorization/policyAssignments?api-version=2019-09-01",
        "policy_definitions_list":"https://management.azure.com/subscriptions/{subscriptionId}/providers/Microsoft.Authorization/policyDefinitions?api-version=2019-09-01",
        "policy_definitions_create_or_update":"https://management.azure.com/subscriptions/{subscriptionId}/providers/Microsoft.Authorization/policyDefinitions/{policyDefinitionName}?api-version=2019-09-01",
        "policy_assignments_create":"https://management.azure.com/subscriptions/{subscriptionId}/providers/Microsoft.Authorization/policyAssignments/{policyAssignmentName}?api-version=2019-09-01",
        "policy_states_summarize_for_policy_definition":"https://management.azure.com/subscriptions/{subscriptionId}/providers/Microsoft.Authorization/policyDefinitions/{policyDefinitionName}/providers/Microsoft.PolicyInsights/policyStates/latest/summarize?api-version=2019-10-01",
        "tags_list":"https://management.azure.com/subscriptions/{subscriptionId}/tagNames?api-version=2019-10-01"
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
