import json
import unittest

import pytest
import requests
import logging
import os
from configparser import ConfigParser
from dotenv import load_dotenv

from mop.prismacloud.compliancestandard import Compliance
from mop.prismacloud.policy import Policy
from mop.azure.utils.create_configuration import (
    change_dir,
    OPERATIONSPATH,
    TESTVARIABLES,
)
from mop.framework.prisma_cloud_connections import PrismaCloudAuthentication


class TestPrismaCloud(unittest.TestCase):
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

    @pytest.mark.skip(reason="Login credentials are not tested by default")
    def test_login(self):
        authentication_provider = PrismaCloudAuthentication()
        token = authentication_provider.authenticate()
        print(token)
        self.assertIsNotNone(token)

    def test_policy_list(self):
        cloud_api = self.config['PRISMACLOUD']['api2_eu']

        policy = Policy()
        policy_response = policy.list(cloud_api=cloud_api)
        self.assertTrue(policy_response.status_code in range(200, 299))

        policies = json.dumps(policy_response.json(), indent=4, ensure_ascii=False)

        print(policies)

    def test_compliance_list(self):
        cloud_api = self.config['PRISMACLOUD']['api2_eu']

        compliance = Compliance()
        compliance_standards_response = compliance.list(cloud_api)
        compliance_standards = json.dumps(compliance_standards_response.json(), indent=4, ensure_ascii=False)
        print(compliance_standards)

    def test_filter_policy_suggest(self):
        cloud_api = self.config['PRISMACLOUD']['api2_eu']

        policy = Policy()
        policies_response = policy.filter_policy_suggest(cloud_api=cloud_api)
        filter_policy_suggest = json.dumps(policies_response.json(), indent=4, ensure_ascii=False)
        print(filter_policy_suggest)


if __name__ == '__main__':
    unittest.main()
