import logging
import os
import inspect
from contextlib import contextmanager

import requests
import adal

from dotenv import load_dotenv


@contextmanager
def request_authenticated_graph_session():
    """
    Context manager for Graph API calls
    :return: requests.session
    """
    session = None
    try:

        token_response = GraphAPIAuthentication().authenticate()
        session = requests.session()
        session.headers.update(
            {"Authorization": "Bearer " + token_response["accessToken"]}
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


class GraphAPIAuthentication:
    """
    Graph SDK authentication token for REST API
    """

    def __init__(
        self,
        authority_host_uri="https://login.microsoftonline.com",
        resource_uri=" https://graph.microsoft.com",
    ):
        load_dotenv()
        self.authority_host_uri = authority_host_uri
        self.resource_uri = resource_uri

        self.client = os.environ["CLIENT"]
        self.secret = os.environ["KEY"]
        self.tenant_id = os.environ["TENANT"]

    def authenticate(self):
        """
        Application id and secret authentication that returns an access token
        WARNING: once acquired, the bearer token can be used anywhere Security Principal has access. This means once
        acquired it might be possible to circumvent Multi-Factor authentication
        :return:
        """
        authority_url = "https://login.microsoftonline.com/" + self.tenant_id
        context = adal.AuthenticationContext(authority_url)
        token = context.acquire_token_with_client_credentials(
            self.resource_uri, self.client, self.secret
        )
        logging.info("Token aquired by client id")

        return token
