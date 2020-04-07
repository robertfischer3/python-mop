import importlib
import re
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
        plugin_path = self.config['PLUGINS']['path01']

        for plugin in plugins:
            if re.match('plugin_', plugin, re.IGNORECASE):
                self.plugins[plugin] = self.config['PLUGINS'][plugin]
        return
