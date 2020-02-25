from configparser import ConfigParser

from dotenv import load_dotenv
from mop.azure.utils.create_configuration import change_dir, OPERATIONSPATH, CONFVARIABLES


class PyPolicyRunner():
    def __init__(self):
        load_dotenv()
        with change_dir(OPERATIONSPATH):
            self.config = ConfigParser()
            self.config.read(CONFVARIABLES)

    def run(self, tenant_id, subscripiton_id, client_id, client_secret, customer_id, shared_key):
        pass


