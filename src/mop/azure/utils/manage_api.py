from configparser import ConfigParser
from contextlib import contextmanager
import os
from mop.azure.utils.atomic_writes import atomic_write

CONFVARIABLES = 'app.config.ini'
OPERATIONSPATH = '../../../..'
TESTVARIABLES = 'test.app.config.ini'
TESTINGPATH='../../..'

@contextmanager
def change_dir(destination):
    try:
        cwd = os.getcwd()
        os.chdir(destination)
        yield
    finally:
        os.chdir(cwd)


def create_baseline_configuration(subscription_id, tentant_id, generate_test=True):
    """
        The method creates the api configuration file for Azure API calls.  As Microsoft changes
    :return:
    """

    config = ConfigParser()
    config['DEFAULT'] = {'subscription_id': os.environ['SUB'], 'management_grp_id':os.environ['MANGRP'], 'tenant_id': os.environ['TENANT']}
    config['LOGGING'] = {'level':'DEBUG'}
    config['AZURESDK'] = {
        'PolicyStatesSummarizeForPolicyDefinition': 'https://management.azure.com/subscriptions/{subscriptionId}/providers/Microsoft.Authorization/policyDefinitions/{policyDefinitionName}/providers/Microsoft.PolicyInsights/policyStates/latest/summarize?api-version=2019-10-01',
        'PolicyStatesSummarizeForSubscription': 'https://management.azure.com/subscriptions/{subscriptionId}/providers/Microsoft.PolicyInsights/policyStates/latest/summarize?api-version=2019-10-01',
        'PolicyStatesSummarizeForSubscriptionFiltered': 'https://management.azure.com/subscriptions/{subscriptionId}/providers/Microsoft.PolicyInsights/policyStates/latest/summarize?api-version=2019-10-01&$filter={filter}',
        'Subscriptions': 'https://management.azure.com/subscriptions?api-version=2019-06-01',
        'PolicyStatesFilterandmultiplegroups':'https://management.azure.com/subscriptions/{subscriptionId}/providers/Microsoft.PolicyInsights/policyStates/latest/queryResults?api-version=2018-04-04&$top=10&$orderby=NumNonCompliantResources desc&$filter=IsCompliant eq false&$apply=groupby((PolicyAssignmentId, PolicySetDefinitionId, PolicyDefinitionId, PolicyDefinitionReferenceId, ResourceId))/groupby((PolicyAssignmentId, PolicySetDefinitionId, PolicyDefinitionId, PolicyDefinitionReferenceId), aggregate($count as NumNonCompliantResources))',
        'PolicyStatesFilterandmultiplegroupsTrue':'https://management.azure.com/subscriptions/{subscriptionId}/providers/Microsoft.PolicyInsights/policyStates/latest/queryResults?api-version=2018-04-04&$top=10&$orderby=NumNonCompliantResources desc&$filter=IsCompliant eq true&$apply=groupby((PolicyAssignmentId, PolicySetDefinitionId, PolicyDefinitionId, PolicyDefinitionReferenceId, ResourceId))/groupby((PolicyAssignmentId, PolicySetDefinitionId, PolicyDefinitionId, PolicyDefinitionReferenceId), aggregate($count as NumNonCompliantResources))',
        'ListQueryResultsForManagementGroup':'https://management.azure.com/providers/Microsoft.Management/managementGroups/{managementGroupName}/providers/Microsoft.PolicyInsights/policyStates/{policyStatesResource}/queryResults?api-version=2018-04-04',
        'PolicyInsightsOperationsList':'PolicyInsightsOperationsList=https://management.azure.com/providers/Microsoft.PolicyInsights/operations?api-version=2018-04-04',
        'VirtualNetworksList':'https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Network/virtualNetworks?api-version=2019-09-01',
        'VirtualNetworksListAll':'https://management.azure.com/subscriptions/{subscriptionId}/providers/Microsoft.Network/virtualNetworks?api-version=2019-09-01',
        'VirtualNetworksListUsage': 'https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Network/virtualNetworks/{virtualNetworkName}/usages?api-version=2019-09-01',
    }

    with atomic_write(CONFVARIABLES, 'w') as configfile:
        config.write(configfile)

    if generate_test:
        with atomic_write(TESTVARIABLES, 'w') as testconfigfile:
            config.write(testconfigfile)
