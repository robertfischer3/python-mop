from configparser import ConfigParser
from contextlib import contextmanager
from dotenv import load_dotenv
import os

CONFVARIABLES = 'app.config.ini'
TESTVARIABLES = 'test.app.config.ini'

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
    config['DEFAULT'] = {'subscription_id': subscription_id, 'tenant_id': tentant_id}
    config['AZURESDK'] = {
        'PolicyStatesSummarizeForPolicyDefinition': 'https://management.azure.com/subscriptions/{subscriptionId}/providers/Microsoft.Authorization/policyDefinitions/{policyDefinitionName}/providers/Microsoft.PolicyInsights/policyStates/latest/summarize?api-version=2019-10-01',
        'PolicyStatesSummarizeForSubscription': 'https://management.azure.com/subscriptions/{subscriptionId}/providers/Microsoft.PolicyInsights/policyStates/latest/summarize?api-version=2019-10-01',
        'PolicyStatesSummarizeForSubscriptionFiltered': 'https://management.azure.com/subscriptions/{subscriptionId}/providers/Microsoft.PolicyInsights/policyStates/latest/summarize?api-version=2019-10-01&$filter={filter}',
        'Subscriptions': 'https://management.azure.com/subscriptions?api-version=2019-06-01',
    }
    with change_dir('../..'):
        with open(CONFVARIABLES, 'w') as configfile:
            config.write(configfile)

        if generate_test:
            with open(TESTVARIABLES, 'w') as testconfigfile:
                config.write(testconfigfile)
