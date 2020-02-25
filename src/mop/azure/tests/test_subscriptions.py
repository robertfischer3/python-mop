import json
import logging
import os
import unittest
import jmespath
from configparser import ConfigParser
from dotenv import load_dotenv
from mop.azure.connections import Connections
from mop.azure.comprehension.operations.subscriptions import Subscriptions
from mop.azure.utils.create_configuration import (
    change_dir,
    OPERATIONSPATH,
    TESTVARIABLES,
)


class TestResourcesSubscriptions(unittest.TestCase):
    def setUp(self) -> None:
        load_dotenv()
        with change_dir(OPERATIONSPATH):
            self.config = ConfigParser()
            self.config.read(TESTVARIABLES)

        logging_level = int(self.config['LOGGING']['level'])
        logging.basicConfig(level=logging_level)
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

    def test_jmespath_search(self):

        with open("response.json", "r") as myfile:
            json_doc = json.load(myfile)


        functional_owner = jmespath.search("value[?tagName == 'functional owner'].values[0].tagValue", json_doc)
        financial_owner = jmespath.search("value[?tagName == 'financial owner'].values[0].tagValue", json_doc)
        billing_contact = jmespath.search("value[?tagName == 'billing contact'].values[0].tagValue", json_doc)


        print(functional_owner, financial_owner, billing_contact)

    def test_get_tags(self):

        subscription_id = self.config['DEFAULT']['subscription_id']

        subscription_tags =  Subscriptions().get_tags_values(subscription_id, 'functional owner', 'financial owner', 'billing contact')
        self.assertEqual(len(subscription_tags) == 3, True)

    def test_subscription_list_displayname_id(self):
        """

        :return:
        """
        credentials = Connections().get_authenticated_client()
        results = Subscriptions().list_displayname_and_id()
        self.assertGreater(len(results), 0)

        for i in results:
            logging.debug(i)

    def test_list_subscriptions(self):
        """

        :return:
        """
        results = Subscriptions().list_subscriptions()
        print(results)

    def test_list_subscription(self):
        """

        :return:
        """
        subscription_id = self.config['DEFAULT']['subscription_id']
        results = Subscriptions().get(subscription_id)
        print(results)
