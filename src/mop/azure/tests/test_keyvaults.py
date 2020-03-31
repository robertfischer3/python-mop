import unittest
from configparser import ConfigParser

from mop.azure.comprehension.keyvault.keyvault import KeyVault
from mop.azure.comprehension.keyvault.vaults import Vaults
from dotenv import load_dotenv

from mop.azure.utils.create_configuration import change_dir, OPERATIONSPATH, TESTVARIABLES


class TestKeyVaults(unittest.TestCase):
    def setUp(self) -> None:
        load_dotenv()
        with change_dir(OPERATIONSPATH):
            self.config = ConfigParser()
            self.config.read(TESTVARIABLES)

    def test_vaults_list(self):
        subscriptionId = self.config["DEFAULT"]["subscription_id"]

        vaults = Vaults()
        response = vaults.list(subscriptionId)
        self.assertEqual(response.status_code, 200)

    def test_vaults_list_by_subscription(self):
        subscriptionId = self.config["DEFAULT"]["subscription_id"]

        vaults = Vaults()
        response = vaults.list_by_subscription(subscriptionId)
        self.assertEqual(response.status_code, 200)

    def test_get_by_id(self):
        subscriptionId = self.config["DEFAULT"]["subscription_id"]

        vaults = Vaults()
        response_vaults = vaults.list_by_subscription(subscriptionId)
        self.assertEqual(response_vaults.status_code, 200)
        id = None
        vaults_json = response_vaults.json()
        if 'value' in vaults_json:
            for vault in vaults_json['value']:
                if 'name' in vault and vault['name'] == 'azure-devops-keyvault-29':
                    id = vault['id']
                    break
        response_vault = vaults.get_by_id(id=id)
        self.assertEqual(response_vault.status_code, 200)

        vault_json = response_vault.json()
        vaultUri = vault_json['properties']['vaultUri']

        key_vault = KeyVault()
        keys = key_vault.get_keys(vaultUri)

        print(keys)


if __name__ == '__main__':
    unittest.main()
