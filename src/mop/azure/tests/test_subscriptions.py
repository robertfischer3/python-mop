import logging
import os
import unittest
from configparser import ConfigParser
from dotenv import load_dotenv
from jmespath import search
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

        with change_dir(OPERATIONSPATH):
            logging.debug(
                "Current change_dir working directory {}".format(os.getcwd())
            )
            self.config = ConfigParser()
            self.config.read(TESTVARIABLES)

    def test_list_subscriptions_api(self):
        execute = Subscriptions().list_subscriptions()
        results = execute()
        print(type(results))

    def test_subscription_list_displayname_id(self):
        """

        :return:
        """
        credentials = Connections().get_authenticated_client()
        results = Subscriptions().subscription_list_displayname_id()
        self.assertGreater(len(results), 0)

        for i in results:
            logging.debug(i)

    def test_list_subscriptions(self):
        """

        :return:
        """
        results = Subscriptions().list_subscriptions()
        print(results)

    def test_list_subscriptions(self):
        """

        :return:
        """
        subscription_id = self.config['DEFAULT']['subscription_id']
        results = Subscriptions().get_subscription(subscription_id)
        print(results)
