from dotenv import load_dotenv
from msrestazure.azure_active_directory import AADTokenCredentials, ServicePrincipalCredentials
import logging
import configparser
import os
import adal
from adal import AuthenticationContext


class Connections:
    """
    Azure connection provides various means to aquire access to an Azure Tenant.  So named since AWS, and Google Cloud
    Platform is planned
    """
    def __index__(self):
        """
        Loads .env file.  CLIENT, KEY, and TENTANTID are required keys for credentials to authenticate with
        :return:
        """
        load_dotenv()

    def authenticate_device_code(self, CLIENT, KEY, TENANT_ID):
        """
        Authenticate the end-user using device auth.  This is one of the easiest authentication method, but the
        requirement of a secret key only makes it unsuitable for sensitive information
        """
        credentials = ServicePrincipalCredentials(
            client_id=CLIENT,
            secret=KEY,
            tenant=TENANT_ID
        )

        return credentials

    def get_authenticated_client(self):
        """
        Returns an authenticated client
        :rtype: object
        """
        client = os.environ['CLIENT']
        pwd = os.environ['KEY']
        tenant_id = os.environ['TENANT']

        credentials = self.authenticate_device_code(CLIENT=client, KEY=pwd, TENANT_ID=tenant_id)
        return credentials


class AzureSDKAuthentication:
    '''
    Azure SDK authentication token for REST API
    '''

    def __init__(self,
                 authority_host_uri='https://login.microsoftonline.com',
                 resource_uri='https://management.azure.com/'):
        load_dotenv()
        self.authority_host_uri = authority_host_uri
        self.resource_uri = resource_uri

        self.client = os.environ['CLIENT']
        self.secret = os.environ['KEY']
        self.tenant_id = os.environ['TENANT']

    def authenticate_client_key(self):
        """
        Authenticate using service principal w/ key.
        """
        authority_host_uri = self.authority_host_uri
        tenant = self.tenant_id
        authority_uri = authority_host_uri + '/' + tenant
        resource_uri = self.resource_uri
        client_id = self.client
        client_secret = self.secret

        context = adal.AuthenticationContext(authority_uri, api_version=None)
        mgmt_token = context.acquire_token_with_client_credentials(resource_uri, client_id, client_secret)

        logging.info("Token aquired by client id {}".format(client_id))
        # credentials = AADTokenCredentials(mgmt_token, client_id)
        return mgmt_token

    def authenticate_device_code(self):
        """
        Authenticate the end-user using device auth.
        """
        authority_host_uri = 'https://login.microsoftonline.com'
        tenant = self.tenant_id
        authority_uri = authority_host_uri + '/' + tenant
        resource_uri = 'https://management.core.windows.net/'
        # This client id is a Microsoft Client ID in common use
        # https://docs.microsoft.com/en-us/samples/azure-samples/data-lake-analytics-python-auth-options/authenticating-your-python-application-against-azure-active-directory/
        client_id = '04b07795-8ddb-461a-bbee-02f9e1bf7b46'

        context = adal.AuthenticationContext(authority_uri, api_version=None)
        code = context.acquire_user_code(resource_uri, client_id)

        mgmt_token = context.acquire_token_with_device_code(resource_uri, code, client_id)
        credentials = AADTokenCredentials(mgmt_token, client_id)
        if credentials:
            logging.info("Token aquired by client id {}".format(client_id))

        return credentials

    def authenticate(self):
        '''
        Application id and secret authentication that returns an access token
        WARNING: once acquired, the bearer token can be used anywhere Security Principal has access. This means once
        acquired it might be possible to circumvent Multi-Factor authentication
        :return:
        '''
        authority_url = "https://login.microsoftonline.com/" + self.tenant_id
        context = adal.AuthenticationContext(authority_url)
        token = context.acquire_token_with_client_credentials(self.resource_uri, self.client, self.secret)
        logging.info("Token aquired by client id {}".format(self.client))

        return token
