import unittest
import os
from dotenv import load_dotenv
from mop.azure.utils.manage_api import TESTVARIABLES, change_dir, CONFVARIABLES
from configparser import ConfigParser
from mop.azure.resources.subscriptions import Subscriptions
from mop.azure.connections import Connections

class TestResourcesSubscriptions(unittest.TestCase):

    def setUp(self) -> None:
        load_dotenv()
        with change_dir('..'):
            print(os.getcwd())
            print(TESTVARIABLES)
            with change_dir('../../..'):

                config = ConfigParser()
                config.read(TESTVARIABLES)

    def test_listsubscriptions(self):

        credentials = Connections().get_authenticated_client()

        results = Subscriptions(credentials).subscription_list_displayname_id()
