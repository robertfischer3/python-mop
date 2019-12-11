import unittest
import os
from tempfile import TemporaryDirectory
from configparser import ConfigParser

from dotenv import load_dotenv

from mop.azure.utils.manage_api import change_dir, create_baseline_configuration, TESTVARIABLES
from mop.azure.utils.atomic_writes import atomic_write

class TestCaseUtils(unittest.TestCase):
    """
    Test the Utils package functionality
    """

    def setUp(self) -> None:
        load_dotenv()

    def test_atomic_writes(self):
        """Ensure file exists after being written successfully for orignal implementation"""

        with TemporaryDirectory() as tmp:
            fp = os.path.join(tmp, "testme.txt")

            # perform an atomic write
            with atomic_write(fp, "w") as f:
                assert not os.path.exists(fp)
                tmpfile = f.name
                f.write("roger that")

            # ensure tmp file has been deleted
            assert not os.path.exists(tmpfile)
            # ensure file to write to exists
            assert os.path.exists(fp)

            # ensure content of destination file is what we expect
            with open(fp) as f:
                self.assertEqual(f.read(), "roger that")


    def test_directory_context_manager(self):
        subscription_id = os.environ['SUB']
        tenant_id = os.environ['TENANT']
        with change_dir('../../..'):
            create_baseline_configuration(tentant_id=tenant_id, subscription_id=subscription_id)
            self.assertEqual(os.path.isfile('app.config.ini'), True)


class TestConfigParser(unittest.TestCase):

    def test_create_config_file_sections(self):
        config = ConfigParser()
        config['DEFAULT'] = {'subscription': '1c1ec02c-560c-4f3f-a8f1-4b29640fdfc6'}
        config['AZURESDK'] = {
            'PolicyStatesSummarizeForPolicyDefinition':'https://management.azure.com/subscriptions/{subscriptionId}/providers/Microsoft.Authorization/policyDefinitions/{policyDefinitionName}/providers/Microsoft.PolicyInsights/policyStates/latest/summarize?api-version=2019-10-01',
            'PolicyStatesSummarizeForSubscription':'https://management.azure.com/subscriptions/{subscriptionId}/providers/Microsoft.PolicyInsights/policyStates/latest/summarize?api-version=2019-10-01',
            'PolicyStatesSummarizeForSubscriptionFiltered':'https://management.azure.com/subscriptions/{subscriptionId}/providers/Microsoft.PolicyInsights/policyStates/latest/summarize?api-version=2019-10-01&$filter={filter}',
        }
        with open(TESTVARIABLES, 'w') as configfile:
            config.write(configfile)

    def test_read_testvariables_ini(self):
        config = ConfigParser()

        print(config.read(TESTVARIABLES))
        print(config['DEFAULT']['subscription'])

if __name__ == '__main__':
    unittest.main()
