import unittest
import os
from tempfile import TemporaryDirectory
from configparser import ConfigParser

from dotenv import load_dotenv

from mop.azure.utils.create_configuration import (
    change_dir,
    create_baseline_configuration,
    TESTVARIABLES,
    TESTINGPATH,
)
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
        subscription_id = os.environ["SUB"]
        tenant_id = os.environ["TENANT"]
        with change_dir(TESTINGPATH):
            create_baseline_configuration()
            self.assertEqual(os.path.isfile("app.config.ini"), True)


class TestConfigParser(unittest.TestCase):
    def setUp(self) -> None:
        load_dotenv()
        self.subscription = os.environ["SUB"]

    def test_create_config_file_sections(self):
        tmpTESTVARIABLES = "tmp_" + TESTVARIABLES
        config = ConfigParser()
        # An active subscription is generally needed for this application
        # However, subscription ids should be guarded.  Hence, we use an .env value

        config["DEFAULT"] = {"subscription": self.subscription}
        config["AZURESDK"] = {
            "PolicyStatesSummarizeForPolicyDefinition": "https://management.azure.com/subscriptions/{subscriptionId}/providers/Microsoft.Authorization/policyDefinitions/{policyDefinitionName}/providers/Microsoft.PolicyInsights/policyStates/latest/summarize?api-version=2019-10-01",
            "PolicyStatesSummarizeForSubscription": "https://management.azure.com/subscriptions/{subscriptionId}/providers/Microsoft.PolicyInsights/policyStates/latest/summarize?api-version=2019-10-01",
            "PolicyStatesSummarizeForSubscriptionFiltered": "https://management.azure.com/subscriptions/{subscriptionId}/providers/Microsoft.PolicyInsights/policyStates/latest/summarize?api-version=2019-10-01&$filter={filter}",
        }
        with change_dir(TESTINGPATH):
            with atomic_write(tmpTESTVARIABLES, "w") as configfile:
                config.write(configfile)

            self.assertEqual(os.path.isfile(tmpTESTVARIABLES), True)
            # This is a temporary local test file because the working directory for the test has not been altered
            if os.path.isfile(tmpTESTVARIABLES):
                os.remove(tmpTESTVARIABLES)

    def test_read_testvariables_ini(self):
        config = ConfigParser()

        print(config.read(TESTVARIABLES))
        print(config["DEFAULT"]["subscription"])


if __name__ == "__main__":
    unittest.main()
