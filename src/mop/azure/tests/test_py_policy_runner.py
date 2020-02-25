import logging
import os
import unittest
from configparser import ConfigParser

from dotenv import load_dotenv

from mop.azure.comprehension.resource_management import py_policy_runner
from mop.azure.utils.create_configuration import (
    TESTVARIABLES,
    change_dir,
    OPERATIONSPATH,
)

class test_py_policy_runner(unittest.TestCase):
    def setUp(self) -> None:
        load_dotenv()
        logging.basicConfig(level=logging.WARN)
        logging.debug("Current working directory {}".format(os.getcwd()))
        with change_dir(OPERATIONSPATH):
            logging.debug("Current change_dir working directory {}".format(os.getcwd()))
            self.config = ConfigParser()
            self.config.read(TESTVARIABLES)

    def test_run(self):
        tenant_id = self.config['DEFAULT']['tenant_id']
        subscriptionId = self.config["DEFAULT"]["subscription_id"]
        client = os.environ["CLIENT"]
        pwd = os.environ["KEY"]

        runner = py_policy_runner.PyPolicyRunner()

        runner.run(tenant_id=tenant_id, subscripiton_id=subscriptionId, client_id=client, client_secret=pwd, customer_id="test", shared_key="test")

if __name__ == '__main__':
    unittest.main()
