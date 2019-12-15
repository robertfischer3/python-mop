import unittest
import os
from dotenv import load_dotenv
from mop.azure.utils.create_configuration import change_dir, CONFVARIABLES, OPERATIONSPATH
from configparser import ConfigParser
from mop.azure.resources.subscriptions import Subscriptions
from mop.azure.connections import Connections
import logging

class TestResourcesSubscriptions(unittest.TestCase):

    def setUp(self) -> None:
        load_dotenv()
        with change_dir('..'):
            with change_dir(OPERATIONSPATH):

                config = ConfigParser()
                config.read(OPERATIONSPATH)
        logging.basicConfig(level=logging.DEBUG)

    def test_listsubscriptions(self):

        credentials = Connections().get_authenticated_client()
        results = Subscriptions(credentials).subscription_list_displayname_id()
        self.assertGreater(len(results), 0)

        for i in results:
            logging.debug(i)
