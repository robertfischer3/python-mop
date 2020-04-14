import importlib
import re
import os

from mop.azure.utils.create_configuration import change_dir, OPERATIONSPATH
from mop.framework.mopbase import MopBase

class Execution(MopBase):

    def __init__(self):
        super().__init__()
        self.plugins = {}

    def load_plugins(self):
        plugins = self.config['PLUGINS']
        for plugin in plugins:
            if re.match('plugin_', plugin, re.IGNORECASE):
                self.plugins[plugin] = self.config['PLUGINS'][plugin]

    def run(self, plugin_name):
        plugins = self.config['PLUGINS']
        root_path = self.config["DEFAULT"]["plugin_root_path"]

        with change_dir(OPERATIONSPATH):
            path = '{}/{}'.format(os.getcwd(), root_path)

        for plugin in plugins:
            if re.match('plugin_', plugin, re.IGNORECASE):
                self.plugins[plugin] = self.config['PLUGINS'][plugin]

        return path
