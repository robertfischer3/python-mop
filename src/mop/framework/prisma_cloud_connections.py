import inspect
import json
import logging
import os
from contextlib import contextmanager

import requests
from dotenv import load_dotenv

from mop.framework.dotenvkms import DotEnvKMS
from mop.framework.mopbase import MopBase


@contextmanager
def request_authenticated_prisma_session():
    """
    Context manager for Prisma Cloud API calls
    :return: requests.session
    """
    session = None
    try:

        token = PrismaCloudAuthentication().authenticate()
        session = requests.session()
        headers = {
            'accept': "*/*",
            'x-redlock-auth': "{token}".format(token=token)
        }
        session.headers.update(
            headers
        )
        yield session
    except:
        func = inspect.currentframe().f_back.f_code
        logging.critical(
            "Error creating authenticated session in {} contained in {}".format(
                func.co_name, func.co_filename,
            )
        )

    finally:
        if session:
            session.close()


class PrismaCloudAuthentication(MopBase):

    def authenticate(self):
        """
        Application id and secret authentication that returns an access token
        WARNING: once acquired, the bearer token can be used anywhere. Ensure least privileges are
        enforced with application account
        :return:
        """
        api_endpoint = self.config['PRISMACLOUD']['api2_eu_login']
        dot_env_kms = DotEnvKMS().credentials

        payload = {'username': dot_env_kms['prisma_username'], 'password': dot_env_kms['prisma_password'],
                   'customerName': dot_env_kms['prisma_customerName']}
        headers = {
            'accept': "application/json; charset=UTF-8",
            'content-type': "application/json; charset=UTF-8"
        }

        data = json.dumps(payload)
        response = requests.request("POST", api_endpoint, data=data, headers=headers)
        if response.status_code in range(200, 299):
            token_json = response.json()
            token = token_json['token']
            return token
