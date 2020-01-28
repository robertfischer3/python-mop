from configparser import ConfigParser

from dotenv import load_dotenv

from mop.azure.connections import Connections
from mop.azure.comprehension.operations.subscriptions import Subscriptions
from mop.azure.utils.create_configuration import OPERATIONSPATH, change_dir, CONFVARIABLES
from mop.azure.comprehension.resource_management.resource import Resource

class SCI():
    def __init__(self):
        load_dotenv()
        self.credentials = Connections().get_authenticated_client()
        with change_dir(OPERATIONSPATH):
            self.config = ConfigParser()
            self.config.read(CONFVARIABLES)


        self.subscriptions = Subscriptions().subscription_list_displayname_id()
        self.resource_cls = Resource()

    def get_resources(self):

        for i in self.subscriptions:
            resources = self.resource_cls.list_resources(i[1])
            print(resources())


if __name__ == "__main__":
    sci = SCI()
    sci.get_resources()
