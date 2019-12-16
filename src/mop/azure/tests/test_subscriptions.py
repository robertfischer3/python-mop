import logging
import os
import unittest
from configparser import ConfigParser
from dotenv import load_dotenv

from mop.azure.connections import Connections
from mop.azure.resources.subscriptions import Subscriptions
from mop.azure.utils.create_configuration import (
    change_dir,
    OPERATIONSPATH,
    TESTVARIABLES,
)


class TestResourcesSubscriptions(unittest.TestCase):
    def setUp(self) -> None:
        load_dotenv()
        logging.basicConfig(level=logging.DEBUG)
        logging.debug("Current working directory {}".format(os.getcwd()))
        with change_dir(".."):
            with change_dir(OPERATIONSPATH):
                logging.debug(
                    "Current change_dir working directory {}".format(os.getcwd())
                )
                config = ConfigParser()
                config.read(TESTVARIABLES)

    def test_listsubscriptions(self):
        """

        :return:
        """
        credentials = Connections().get_authenticated_client()
        results = Subscriptions(credentials).subscription_list_displayname_id()
        self.assertGreater(len(results), 0)

        for i in results:
            logging.debug(i)
