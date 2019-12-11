from configparser import ConfigParser
from dotenv import load_dotenv

CONFVARIABLES = 'app.config.ini'

def create_baseline_configuration():
    """
        The method creates the api configuration file for Azure API calls.  As Microsoft changes
    :return:
    """

    config = ConfigParser()
    config['DEFAULT'] = {'subscription': '1c1ec02c-560c-4f3f-a8f1-4b29640fdfc6'}
    config['AZURESDK'] = {
        'PolicyStatesSummarizeForPolicyDefinition': 'https://management.azure.com/subscriptions/{subscriptionId}/providers/Microsoft.Authorization/policyDefinitions/{policyDefinitionName}/providers/Microsoft.PolicyInsights/policyStates/latest/summarize?api-version=2019-10-01',
        'PolicyStatesSummarizeForSubscription': 'https://management.azure.com/subscriptions/{subscriptionId}/providers/Microsoft.PolicyInsights/policyStates/latest/summarize?api-version=2019-10-01',
        'PolicyStatesSummarizeForSubscriptionFiltered': 'https://management.azure.com/subscriptions/{subscriptionId}/providers/Microsoft.PolicyInsights/policyStates/latest/summarize?api-version=2019-10-01&$filter={filter}',
        '': '',
    }
    with open(CONFVARIABLES, 'w') as configfile:
        config.write(configfile)
