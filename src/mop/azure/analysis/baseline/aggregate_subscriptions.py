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

    def compile_tags(self):
        '''
        Storing subscription tags in a database table
        '''
        # create a configured "Session" class
        # create a Session

        batch_uuid = uuid.uuid4()
        created = datetime.datetime.utcnow()

        session = self.Session()
        # Execute returns a method the can be executed anywhere more than once
        models = self.get_db_model(self.engine)

        subscription_facade = Subscriptions()

        subscription_cls = models.classes.subscriptions
        subscription_tags2 = models.classes.subscription_tags2
        subscriptions = session.query(subscription_cls).all()

        subscription_tag_list = list()
        for subscription in subscriptions:

            tag_dictionary = subscription_facade.get_tags_dictionary(subscription.subscription_id)
            if tag_dictionary:
                for tag_name in tag_dictionary:
                    print(tag_name, tag_dictionary[tag_name])
                    for tag_value in tag_dictionary[tag_name]:
                        tag = subscription_tags2(
                            subscription_id=subscription.subscription_id,
                            tag_name=tag_name,
                            tag_value=tag_value,
                            created=created,
                            batch_uuid=batch_uuid
                        )
                    subscription_tag_list.append(tag)

        session.bulk_save_objects(subscription_tag_list)
        session.commit()

    def identify_subscription_owners(self):
        # create a Session
        session = self.Session()
        # Execute returns a method the can be executed anywhere more than once
        models = self.get_db_model(self.engine)

        subscription_facade = Subscriptions()

        subscription_cls = models.classes.subscriptions
        subscription_tags2_cls = models.classes.subscription_tags2
        subscriptions = session.query(subscription_cls).all()

        technical_owner_dict = self.get_filtered_tags(session, subscription_tags2_cls, 'tech%')
        financial_owner_dict = self.get_filtered_tags(session, subscription_tags2_cls, 'financial%')
        functional_owner_dict = self.get_filtered_tags(session, subscription_tags2_cls, 'function%')
        market_dict = self.get_filtered_tags(session, subscription_tags2_cls, 'market')

        for subscription in subscriptions:
            if subscription.subscription_id in functional_owner_dict:
                subscription.functional_owner = functional_owner_dict[subscription.subscription_id]

            if subscription.subscription_id in financial_owner_dict:
                subscription.financial_owner = financial_owner_dict[subscription.subscription_id]

            if subscription.subscription_id in technical_owner_dict:
                subscription.billing_contact = technical_owner_dict[subscription.subscription_id]

            if subscription.subscription_id in market_dict:
                subscription.market = market_dict[subscription.subscription_id]

        session.bulk_save_objects(subscriptions, update_changed_only=True)
        session.commit()

    def get_filtered_tags(self, session, subscription_tags2_cls, like_filter):
        filtered_tags = session.query(subscription_tags2_cls).filter(subscription_tags2_cls.tag_name.ilike(like_filter))

        if filtered_tags:
            filtered_tags_dict = {}

            for subscription in filtered_tags:
                if subscription.subscription_id not in filtered_tags_dict:
                    filtered_tags_dict[subscription.subscription_id] = subscription.tag_value[:511]
                else:
                    filtered_tags_dict[subscription.subscription_id] = (filtered_tags_dict[
                                                                            subscription.subscription_id] + ';' + subscription.tag_value)[
                                                                       :511]
        return filtered_tags_dict

    def get_functional_owner_tags(self, session, subscription_tags2_cls):
        functional_tags = session.query(subscription_tags2_cls).filter(
            subscription_tags2_cls.tag_name.ilike('function%'))

        if functional_tags:
            functional_owner_dict = {}

            for subscription in functional_tags:
                if subscription.subscription_id not in functional_owner_dict:
                    functional_owner_dict[subscription.subscription_id] = subscription.tag_value[:511]
                else:
                    functional_owner_dict[subscription.subscription_id] = (functional_owner_dict[
                                                                               subscription.subscription_id] + ';' + subscription.tag_value)[
                                                                          :511]
        return functional_owner_dict

    def get_financial_owner_tags(self, session, subscription_tags2_cls):
        financial_tags = session.query(subscription_tags2_cls).filter(
            subscription_tags2_cls.tag_name.ilike('financial%'))

        if financial_tags:
            financial_owner_dict = {}

            for subscription in financial_tags:
                if subscription.subscription_id not in financial_owner_dict:
                    financial_owner_dict[subscription.subscription_id] = subscription.tag_value[:511]
                else:
                    financial_owner_dict[subscription.subscription_id] = (financial_owner_dict[
                                                                              subscription.subscription_id] + ';' + subscription.tag_value)[
                                                                         :511]
        return financial_owner_dict

    def get_technical_owner_tags(self, session, subscription_tags2_cls):
        technical_tags = session.query(subscription_tags2_cls).filter(subscription_tags2_cls.tag_name.ilike('tech%'))
        if technical_tags:
            technical_owner_dict = {}

            for subscription in technical_tags:
                if subscription.subscription_id not in technical_owner_dict:
                    technical_owner_dict[subscription.subscription_id] = subscription.tag_value[:511]
                else:
                    technical_owner_dict[subscription.subscription_id] = (technical_owner_dict[
                                                                              subscription.subscription_id] + ';' + subscription.tag_value)[
                                                                         :511]
        return technical_owner_dict
