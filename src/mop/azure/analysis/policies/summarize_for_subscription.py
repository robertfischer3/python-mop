import datetime
import json
import os
import uuid
from configparser import ConfigParser

import jmespath
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker
from azure.cosmos import CosmosClient, PartitionKey, exceptions

from mop.azure.comprehension.operations.policy_states import PolicyStates
from mop.azure.comprehension.operations.policy_insights2 import PolicyInsights2

from mop.azure.utils.create_configuration import CONFVARIABLES, change_dir, OPERATIONSPATH
from mop.db.basedb import BaseDb


class SummarizeForSubscription(BaseDb):

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

        self.password = os.environ['DATABASEPWD']

        self.get_db_engine()
        self.Session = sessionmaker(bind=self.engine)


    def Summarize_For_Subscription(self):
        policy_states = PolicyStates()
        batch_uuid = uuid.uuid4()
        created = datetime.datetime.utcnow()

        # create a configured "Session" class

        # create a Session
        # Execute returns a method the can be executed anywhere more than once
        models = self.get_db_model(self.engine)
        subscriptions_model = models.classes.subscriptions

        session = self.Session()
        subscriptions = session.query(subscriptions_model).all()
        policy_insights = PolicyInsights2()

        for subscription in subscriptions:
            policy_insight_response = policy_insights.policy_states_summarize_for_subscription(subscriptionId=subscription.subscription_id)
            if policy_insight_response.status_code in range(200, 299):
                policy_states_summarize_for_subscription = policy_insight_response.json()
                print(subscription.subscription_id)


        #TODO finish
