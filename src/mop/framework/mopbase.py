import logging
import os
from configparser import ConfigParser
from dotenv import load_dotenv

from mop.framework.azure_connections import AzureConnections
from mop.azure.utils.create_configuration import change_dir, OPERATIONSPATH, CONFVARIABLES, TESTVARIABLES


class MopBase():
    def __init__(self):
        load_dotenv()
        self.credentials = AzureConnections().get_authenticated_client()

        # Not the default path is debug. This exists in order to fail safe.  Production must be explicit.
        if 'mop_debug' is os.environ and os.environ['mop_debug'].lower() in 'false':
            config_file = CONFVARIABLES
        else:
            config_file = TESTVARIABLES

        with change_dir(OPERATIONSPATH):
            self.config = ConfigParser()
            self.config.read(config_file)

        logging_level = int(self.config['LOGGING']['level'])
        logging.basicConfig(level=logging_level)
