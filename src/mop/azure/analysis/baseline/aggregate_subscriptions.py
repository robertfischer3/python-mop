import json
import os
import uuid
from configparser import ConfigParser

from dotenv import load_dotenv
from sqlalchemy import text
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
