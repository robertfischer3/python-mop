import os
from configparser import ConfigParser
from unittest import TestCase
import azure.cosmos.cosmos_client as cosmos_client
from azure.cosmos import DatabaseProxy
from azure.cosmos.container import ContainerProxy
from dotenv import load_dotenv

from mop.azure.analysis.baseline.aggregate_cosmos_subscriptions import AggregateCosmosDbSubscriptions
from mop.azure.utils.create_configuration import OPERATIONSPATH, change_dir, TESTVARIABLES


class TestAggregateCosmosDbSubscriptions(TestCase):
    def setUp(self) -> None:
        load_dotenv()
        with change_dir(OPERATIONSPATH):
            self.config = ConfigParser()
            self.config.read(TESTVARIABLES)

    def test_AggregateCosmosDbSubscriptions_constructor(self):
        client_id = os.environ["CLIENT"]
        key = os.environ["KEY"]
        tenant_id = os.environ["TENANT"]
        cosmos_db_key = os.environ["COSMODB_KEY"]
        cosmosdb_url = self.config['COSMOSDB']['uri_01']

        aggregate_cosmosdb_subscriptions = AggregateCosmosDbSubscriptions(client_id=client_id, key=key,
                                                                          tenant_id=tenant_id, url=cosmosdb_url,
                                                                          cosmos_key=cosmos_db_key)
        self.assertIsNotNone(aggregate_cosmosdb_subscriptions)

    def test_get_aggregate_entities(self):
        client_id = os.environ["CLIENT"]
        key = os.environ["KEY"]
        tenant_id = os.environ["TENANT"]
        cosmos_db_key = os.environ["COSMODB_KEY"]
        cosmosdb_url = self.config['COSMOSDB']['uri_01']

        aggregate_cosmosdb_subscriptions = AggregateCosmosDbSubscriptions(client_id=client_id, key=key,
                                                                          tenant_id=tenant_id, url=cosmosdb_url,
                                                                          cosmos_key=cosmos_db_key)
        subscriptions = aggregate_cosmosdb_subscriptions.get_management_group_entities(management_grp=tenant_id, subscriptions_only=True)
        self.assertGreaterEqual(len(subscriptions), 0)

    def test_cosmos_db_connection(self):
        cosmos_db_key = os.environ["COSMODB_KEY"]
        cosmosdb_url = self.config['COSMOSDB']['uri_01']

        client = cosmos_client.CosmosClient(cosmosdb_url, cosmos_db_key)
        databases = list(client.list_databases())

        if not databases:
            return

        for database in databases:
            print(database['id'])

        db = client.create_database_if_not_exists('booger2')
        self.assertIs(type(db), DatabaseProxy)

        client.delete_database(db)

    def test_cosmos_db_client(self):

        client_id = os.environ["CLIENT"]
        key = os.environ["KEY"]
        tenant_id = os.environ["TENANT"]
        cosmos_db_key = os.environ["COSMODB_KEY"]
        cosmosdb_url = self.config['COSMOSDB']['uri_01']

        aggregate_cosmosdb_subscriptions = AggregateCosmosDbSubscriptions(client_id=client_id, key=key,
                                                                          tenant_id=tenant_id, url=cosmosdb_url,
                                                                          cosmos_key=cosmos_db_key)
        try:
            database = aggregate_cosmosdb_subscriptions.get_cosmos_db("baddb03")
            self.assertIsNotNone(database)
            self.assertIsInstance(database, DatabaseProxy)
        finally:
            aggregate_cosmosdb_subscriptions.delete_database("baddb03")


    def test_cosmos_container(self):

        client_id = os.environ["CLIENT"]
        key = os.environ["KEY"]
        tenant_id = os.environ["TENANT"]
        cosmos_db_key = os.environ["COSMODB_KEY"]
        cosmosdb_url = self.config['COSMOSDB']['uri_01']

        aggregate_cosmosdb_subscriptions = AggregateCosmosDbSubscriptions(client_id=client_id, key=key,
                                                                          tenant_id=tenant_id, url=cosmosdb_url,
                                                                          cosmos_key=cosmos_db_key)
        try:
            database = aggregate_cosmosdb_subscriptions.get_cosmos_db("baddb04")
            container = aggregate_cosmosdb_subscriptions.get_cosmos_container(database=database, container_name= "test04", partition='/subscription')

            self.assertIsInstance(container, ContainerProxy)
        finally:
            aggregate_cosmosdb_subscriptions.delete_database("baddb04")

    def test_publish_entity_info(self):
        client_id = os.environ["CLIENT"]
        key = os.environ["KEY"]
        tenant_id = os.environ["TENANT"]
        cosmos_db_key = os.environ["COSMODB_KEY"]
        cosmosdb_url = self.config['COSMOSDB']['uri_01']

        aggregate_cosmosdb_subscriptions = AggregateCosmosDbSubscriptions(client_id=client_id, key=key,
                                                                          tenant_id=tenant_id, url=cosmosdb_url,
                                                                          cosmos_key=cosmos_db_key)
        subscriptions = aggregate_cosmosdb_subscriptions.get_management_group_entities(management_grp=tenant_id,
                                                                                       subscriptions_only=True)

        database = aggregate_cosmosdb_subscriptions.get_cosmos_db('policy_analysis')
        container = aggregate_cosmosdb_subscriptions.get_cosmos_container(database=database, container_name='subscriptions', partition='/name' )

        self.assertIsNotNone(database)
        self.assertIsInstance(database, DatabaseProxy)
        self.assertIsNotNone(container)
        self.assertIsInstance(container, ContainerProxy)
        for subscription in subscriptions:
            container.upsert_item(subscription)

