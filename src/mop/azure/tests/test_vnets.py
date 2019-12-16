import logging
import unittest
from configparser import ConfigParser
import os
from mop.azure.resources.vnets import VNet

from dotenv import load_dotenv

from mop.azure.utils.create_configuration import change_dir, OPERATIONSPATH, TESTVARIABLES, CONFVARIABLES


class TestVNetInformation(unittest.TestCase):
    def setUp(self) -> None:
        load_dotenv()
        logging.basicConfig(level=logging.DEBUG)
        logging.debug("Current working directory {}".format(os.getcwd()))
        with change_dir(OPERATIONSPATH):
            logging.debug(
                "Current change_dir working directory {}".format(os.getcwd())
            )
            self.config = ConfigParser()
            self.config.read(CONFVARIABLES)

    def test_VNetAPIs(self):
        vnet = VNet()
        subscription = self.config['DEFAULT']['subscription_id']

        execute = vnet.vnets_list(subscription)
        results = execute()

        self.assertIsNotNone(results)
