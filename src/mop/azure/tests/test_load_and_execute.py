import logging
import os
import unittest
from configparser import ConfigParser
from mop.azure.utils.create_configuration import change_dir, OPERATIONSPATH, TESTVARIABLES
from dotenv import load_dotenv

from mop.azure.plugins.execution import Execution

from mop.azure.plugins.pypolicy.glbl_pr_sec_databricks_vnetfilter_scr import \
    main as glbl_pr_sec_databricks_vnetfilter_scr
from mop.azure.plugins.pypolicy.glbl_pr_sec_cdb_aadauth_scr import main as glbl_pr_sec_cdb_aadauth_scr
from mop.azure.plugins.pypolicy.glbl_pr_sec_netapp_backupaudit_scr import main as glbl_pr_sec_netapp_backupaudit_scr
from mop.azure.plugins.pypolicy.glbl_pr_sec_storage_aadauth_scr import main as glbl_pr_sec_storage_aadauth_scr



class TestLoadAndExecute(unittest.TestCase):
    def setUp(self) -> None:
        load_dotenv()
        logging.basicConfig(level=logging.WARN)
        logging.debug("Current working directory {}".format(os.getcwd()))
        with change_dir(OPERATIONSPATH):
            logging.debug("Current change_dir working directory {}".format(os.getcwd()))
            self.config = ConfigParser()
            self.config.read(TESTVARIABLES)

    def test_something(self):
        execute = Execution()
        path = execute.run('plugin_python_policies')

        subscription_id = self.config['DEFAULT']['subscription_id']
        tenant_id = self.config['DEFAULT']['tenant_id']
        client_id = os.environ['CLIENT']
        client_secret = os.environ['Key']
        customer_id = ''
        shared_key = ''

        glbl_pr_sec_databricks_vnetfilter_scr(tenant_id=tenant_id, )


if __name__ == '__main__':
    unittest.main()
