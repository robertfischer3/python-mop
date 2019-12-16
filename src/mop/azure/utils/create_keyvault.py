"""
Azure Key Vaults are the better way to store credentials than other alternatives.  This utility creates
an Key Vault that can be utilized for managing cloud and database credentials

The code is based on example code provided by Laurent Mazuel, Ian McCowan and the original is found here:
https://github.com/Azure-Samples/key-vault-python-manage/blob/master/example.py
"""
import os
import logging
from msrestazure.azure_active_directory import ServicePrincipalCredentials
from azure.keyvault.key_vault_client import KeyVaultClient
from azure.mgmt.resource.resources.resource_management_client import (
    ResourceManagementClient,
)


def create_key_vault(credentials, subscription_id):

    kv_client = KeyVaultClient(credentials, subscription_id)
    resource_client = ResourceManagementClient(credentials, subscription_id)

    # You MIGHT need to add KeyVault as a valid provider for these credentials
    # If so, this operation has to be done only once for each credentials
    resource_client.providers.register("Microsoft.KeyVault")

    # Create Resource group
    ("\nCreate Resource Group")
    resource_group_params = {"location": WEST_US}
    print_item(
        resource_client.resource_groups.create_or_update(
            GROUP_NAME, resource_group_params
        )
    )

    # Create a vault
    print("\nCreate a vault")
    vault = kv_client.vaults.create_or_update(
        GROUP_NAME,
        KV_NAME,
        {
            "location": WEST_US,
            "properties": {
                "sku": {"name": "standard"},
                "tenant_id": os.environ["AZURE_TENANT_ID"],
                "access_policies": [
                    {
                        "tenant_id": os.environ["AZURE_TENANT_ID"],
                        "object_id": OBJECT_ID,
                        "permissions": {"keys": ["all"], "secrets": ["all"]},
                    }
                ],
            },
        },
    )
    print_item(vault)

    # List the Key vaults
    print("\nList KeyVault")
    for vault in kv_client.vaults.list():
        print_item(vault)
