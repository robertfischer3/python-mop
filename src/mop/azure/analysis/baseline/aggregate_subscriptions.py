import datetime
import json
import os
import uuid
from configparser import ConfigParser
import pandas as pd

from dotenv import load_dotenv
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker

from mop.azure.comprehension.operations.subscriptions import Subscriptions
from mop.azure.utils.create_configuration import change_dir, OPERATIONSPATH, CONFVARIABLES
from mop.db.basedb import BaseDb


class AggregateSubscriptions(BaseDb):

    def __init__(self, db_server_instance="instance01"):
        load_dotenv()
        with change_dir(OPERATIONSPATH):
            self.config = ConfigParser()
            self.config.read(CONFVARIABLES)

        sql_instance = self.config['SQLSERVER'][db_server_instance]
        sql_instance = json.loads(sql_instance.replace("\'", "\""))
        self.server = sql_instance['server']
        self.database = sql_instance['database']
        self.username = sql_instance['username']
        self.driver = sql_instance['db_driver']
        self.dialect = sql_instance['dialect']
        self.password = password = os.environ['DATABASEPWD']
        self.get_db_engine()

        self.Session = sessionmaker(bind=self.engine)

    def get_managment_grp_subscriptions(self, management_grp):
        subscriptions = Subscriptions()
        return subscriptions.dataframe_management_grp_subcriptions(management_grp)

    def create_subscriptions(self, subscriptions_dataframe):
        subscriptions_dataframe['batch_uuid'] = uuid.uuid4()
        subscriptions_dataframe['created'] = datetime.datetime.utcnow()
        subscriptions_dataframe['modified'] = datetime.datetime.utcnow()
        subscriptions_dataframe.to_sql('subscriptions', self.engine, if_exists='append')

    def list_subscriptions(self):
        """
        Returns all subscriptions in the database
        :return:
        """
        models = self.get_db_model(self.engine)
        subscriptions = models.classes.subscriptions
        session = self.Session()
        return session.query(subscriptions).all()

    def list_tags(self):
        # create a configured "Session" class

        # create a Session
        session = self.Session()
        # Execute returns a method the can be executed anywhere more than once
        models = self.get_db_model(self.engine)

        subscription_facade = Subscriptions()

        subscription_cls = models.classes.subscriptions
        subscriptions = session.query(subscription_cls).all()

        subscription_tag_list = list()
        for subscription in subscriptions:

            tag_dictionary = subscription_facade.get_tags_dictionary(subscription.subscription_id)
            if tag_dictionary:
                for tag_name in tag_dictionary:
                    print(tag_name, tag_dictionary[tag_name])
                    for tag_value in tag_dictionary[tag_name]:
                        subscription_tag_list.append([subscription.subscription_id, tag_name, tag_value])

        return subscription_tag_list

    def save_tags(self, subscription_tag_list):
        """

        :param subscription_tag_list:
        :return:
        """
        batch_uuid = uuid.uuid4()
        created = datetime.datetime.utcnow()

        df = pd.DataFrame(subscription_tag_list, columns=['subscription_id', 'tag_name', 'tag_value'])
        df['batch_uuid'] = batch_uuid
        df['created'] = created
        df.reset_index(inplace=True)
        df.to_sql('subscription_tags', index=False, con=self.engine, if_exists='append', chunksize=1000)

    def list_tag_name_cloud(self):
        # create a Session
        session = self.Session()
        # Execute returns a method the can be executed anywhere more than once
        models = self.get_db_model(self.engine)

        subscription_facade = Subscriptions()

        subscription_cls = models.classes.subscriptions
        subscriptions = session.query(subscription_cls).all()
        tag_name_cloud = {}
        for subscription in subscriptions:
            tag_dictionary = subscription_facade.get_tags_dictionary(subscription.subscription_id)
