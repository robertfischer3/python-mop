from configparser import ConfigParser

from azure.cosmos import cosmos_client, PartitionKey, exceptions as cosmos_except
from azure.mgmt.managementgroups import ManagementGroupsAPI
from dotenv import load_dotenv

from mop.azure.utils.create_configuration import change_dir, OPERATIONSPATH, CONFVARIABLES
from mop.azure.comprehension.operations.subscriptions import Subscriptions
from mop.framework.azure_connections import AzureConnections


class AggregateCosmosDb:
    def __init__(self, client_id, key, tenant_id, url, cosmos_key):
        load_dotenv()
        self.url = url
        self.__comos_key = cosmos_key
        self.cosmos_client = cosmos_client.CosmosClient(url, cosmos_key)

        self.credentials = AzureConnections().authenticate_device_code(CLIENT=client_id, KEY=key,
                                                                       TENANT_ID=tenant_id)

        with change_dir(OPERATIONSPATH):
            self.config = ConfigParser()
            self.config.read(CONFVARIABLES)

    def delete_database(self, id):
        self.cosmos_client.delete_database(id)

    def get_cosmos_container(self, database, container_name, partition, offer_throughput=400):
        partition_key = PartitionKey(path=partition, kind='Hash')
        container = database.create_container_if_not_exists(
            id=container_name,
            partition_key=partition_key,
            offer_throughput=offer_throughput
        )
        return container

    def get_cosmos_db(self, cosmos_db_name):
        databases = list(self.cosmos_client.list_databases())
        for database in databases:
            if cosmos_db_name in database['id']:
                return self.cosmos_client.get_database_client(cosmos_db_name)

        return self.cosmos_client.create_database(cosmos_db_name)


class AggregateCosmosDbSubscriptions(AggregateCosmosDb):

    def get_management_group_entities(self, management_grp, subscriptions_only = True):
        entity_list = list()
        management_client = ManagementGroupsAPI(self.credentials)
        mngrp_subscriptions = management_client.entities.list(group_name=management_grp)
        for entity in mngrp_subscriptions:
            if subscriptions_only:
                if "/subscriptions" in entity.type:
                    sub_entity = dict()
                    sub_entity['name'] = entity.name
                    sub_entity['display_name'] = entity.display_name
                    sub_entity['resource_id'] = entity.id
                    sub_entity['tenant_id'] = entity.tenant_id
                    entity_list.append(sub_entity)
            else:
                raise NotImplementedError

        return entity_list


    def publish_subscription_info(self, cosmos_db_name, partition, offer_throughput=400):

        database = self.get_cosmos_db(cosmos_db_name)
        container = self.get_cosmos_container(database, partition, offer_throughput)


        # try:
        #     database.create_container(id=id, partition_key=partition_key)
        #     print('Container with id \'{0}\' created'.format(id))
        #
        # except cosmos_except.CosmosResourceExistsError:
        #     pass



