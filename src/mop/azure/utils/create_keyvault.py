import os

from msrestazure.azure_active_directory import ServicePrincipalCredentials
import os
import json
from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.keyvault import KeyVaultManagementClient
from azure.mgmt.resource.resources import ResourceManagementClient

# The object ID of the User or Application for access policies. Find this number in the portal
def create_keyvault(KV_NAME, GROUP_NAME, OBJECT_ID, location):
    subscription_id = os.environ['SUB']

    credentials = ServicePrincipalCredentials(
        client_id=os.environ['CLIENT'],
        secret=os.environ['KEY'],
        tenant=os.environ['TENANT']
    )
    kv_client = KeyVaultManagementClient(credentials, subscription_id)
    resource_client = ResourceManagementClient(credentials, subscription_id)

    # You MIGHT need to add KeyVault as a valid provider for these credentials
    # If so, this operation has to be done only once for each credentials
    resource_client.providers.register('Microsoft.KeyVault')

    # Create Resource group

    resource_group_params = {'location': location}
    resource_client.resource_groups.create_or_update(
        GROUP_NAME, resource_group_params)

    # Create a vault

    vault = kv_client.vaults.create_or_update(
        GROUP_NAME,
        KV_NAME,
        {
            'location': location,
            'properties': {
                'sku': {
                    'name': 'standard'
                },
                'tenant_id': os.environ['TENANT'],
                'access_policies': [{
                    'tenant_id': os.environ['TENANT'],
                    'object_id': OBJECT_ID,
                    'permissions': {
                        'keys': ['all'],
                        'secrets': ['all']
                    }
                }]
            }
        }
    )
