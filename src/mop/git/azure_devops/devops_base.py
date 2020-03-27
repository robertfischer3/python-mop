from configparser import ConfigParser
from dotenv import load_dotenv

from mop.azure.utils.create_configuration import (
    change_dir,
    CONFVARIABLES,
    OPERATIONSPATH,
)


class AzureDevOpsBase():
    def __init__(self, personal_access_token):
        load_dotenv()
        with change_dir(OPERATIONSPATH):
            self.config = ConfigParser()
            self.config.read(CONFVARIABLES)

        self.personal_access_token = personal_access_token
