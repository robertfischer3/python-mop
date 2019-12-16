import logging
import unittest
from configparser import ConfigParser
import os
from dotenv import load_dotenv

from mop.azure.analysis.compile_compliance import summarize_subscriptions
from mop.azure.utils.create_configuration import (
    TESTVARIABLES,
    change_dir,
    OPERATIONSPATH,
)


class TestAnalysisCompileCompliance(unittest.TestCase):
    def setUp(self) -> None:
        load_dotenv()
        logging.basicConfig(level=logging.DEBUG)
        logging.debug("Current working directory {}".format(os.getcwd()))
        with change_dir(OPERATIONSPATH):
            logging.debug("Current change_dir working directory {}".format(os.getcwd()))
            self.config = ConfigParser()
            self.config.read(TESTVARIABLES)

    def test_summarize_subscriptions(self):
        subscription_id = self.config["DEFAULT"]["subscription_id"]
        df = summarize_subscriptions(subscription_id)
        print(df)
