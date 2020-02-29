import datetime
import json
import os
import urllib
from configparser import ConfigParser

import pluggy
from dotenv import load_dotenv
from sqlalchemy import MetaData, Table, Column, Integer, String, Float, BigInteger, DateTime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import sqltypes

from mop.azure.analysis.analysis_db import AnalysisDb
from mop.azure.utils.create_configuration import change_dir, OPERATIONSPATH, CONFVARIABLES
from mop.db.basedb import BaseDb

dbhookimpl = pluggy.HookimplMarker("Analysis")
dbhookspec = pluggy.HookspecMarker("Analysis")


class DatbasePlugins(object):
    """A hook specification namespace."""

    @dbhookspec
    def create_database_tables(self):
        """Datbase creation hook"""

    @dbhookspec
    def delete_data(self, server, database, user, password, driver):
        """Datbase deletion hook"""


class SQLServerDatabase(BaseDb):
    """
        This class is an implementation of the dbhookspec
    """
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
        self.db_driver = sql_instance['db_driver']
        self.dialect = sql_instance['dialect']

        password = os.environ['DATABASEPWD']

        self.baseDb = BaseDb(server=self.server,
                             database=self.database,
                             user=self.username,
                             driver=self.db_driver,
                             dialect=self.dialect,
                             password=password)

        self.engine = self.baseDb.get_db_engine()
        self.Session = sessionmaker(bind=self.engine)

    @dbhookimpl
    def create_database_tables(self):
        """
            This function creates a SQL Server 2019 for Linux database table for handling results found in analysis
            As the framework becomes more modular, multiple database initiation modules need to be created
        :return:
        """
        engine = self.engine

        # The database here is not quite formed properly with proper keys and indexes.
        # TODO establish proper data model

        meta = MetaData()

        test_compiled_sci = Table(
            "test_compiled_sci",
            meta,
            Column("id", BigInteger, autoincrement=True, primary_key=True),
            Column("tenant_id", String(36)),
            Column("management_grp", sqltypes.NVARCHAR(300)),
            Column("subscription_id", String(36)),
            Column("subscription_display_name", sqltypes.NVARCHAR(64)),
            Column("business_owner_tag", sqltypes.NVARCHAR(256)),
            Column("technical_owner_tag", sqltypes.NVARCHAR(256)),
            Column("metadata_category", sqltypes.NVARCHAR(128)),
            Column("policy_definition_name", sqltypes.NVARCHAR(128)),
            Column("policy_display_name", sqltypes.NVARCHAR(128)),
            Column("policy_description", sqltypes.NVARCHAR(512)),
            Column("policy_definition_id", String(512)),
            Column("policy_compliant_resources", Integer),
            Column("policy_noncompliant_resources", Integer),
            Column("total_resources_measured", Integer),
            Column("percent_in_compliance", Float),
            Column("created", DateTime),
            Column("modified", DateTime),
            Column("batch_uuid", String(36)),

        )

        compiled_sci = Table(
            "compiled_sci",
            meta,
            Column("id", BigInteger, autoincrement=True, primary_key=True),
            Column("tenant_id", String(36)),
            Column("management_grp", sqltypes.NVARCHAR(300)),
            Column("subscription_id", String(36)),
            Column("subscription_display_name", sqltypes.NVARCHAR(64)),
            Column("business_owner_tag", sqltypes.NVARCHAR(256)),
            Column("technical_owner_tag", sqltypes.NVARCHAR(256)),
            Column("metadata_category", sqltypes.NVARCHAR(128)),
            Column("policy_definition_name", sqltypes.NVARCHAR(128)),
            Column("policy_display_name", sqltypes.NVARCHAR(128)),
            Column("policy_description", sqltypes.NVARCHAR(512)),
            Column("policy_definition_id", String(512)),
            Column("policy_compliant_resources", Integer),
            Column("policy_noncompliant_resources", Integer),
            Column("total_resources_measured", Integer),
            Column("percent_in_compliance", Float),
            Column("created", DateTime),
            Column("modified", DateTime),
            Column("batch_uuid", String(36)),

        )

        test_factcompliance = Table(
            "test_factcompliance",
            meta,
            Column("id", BigInteger, primary_key=True),
            Column("resource_id", String),
            Column("subscription_id", String(36)),
            Column("tenant_id", String(36)),
            Column("policy_definition_name", sqltypes.NVARCHAR(128)),
            Column("policy_assignment_id", String),
            Column("policy_definition_id", sqltypes.NVARCHAR(512)),
            Column("compliant", Integer),
            Column("noncompliant", Integer),
            Column("total_resources_measured", Integer),
            Column("percent_compliant", Float),
            Column("created", DateTime),
            Column("modified", DateTime),
            Column("batch_uuid", String(36)),

        )

        factcompliance = Table(
            "factcompliance",
            meta,
            Column("id", BigInteger, primary_key=True),
            Column("resource_id", String),
            Column("subscription_id", String(36)),
            Column("tenant_id", String(36)),
            Column("policy_definition_name", sqltypes.NVARCHAR(128)),
            Column("policy_assignment_id", String),
            Column("policy_definition_id", sqltypes.NVARCHAR(512)),
            Column("compliant", Integer),
            Column("noncompliant", Integer),
            Column("total_resources_measured", Integer),
            Column("percent_compliant", Float),
            Column("created", DateTime),
            Column("modified", DateTime),
            Column("batch_uuid", String(36)),

        )

        test_policydefinitions = Table(
            "test_policydefinitions",
            meta,
            Column("id", Integer, primary_key=True),
            Column("policy_definition_name", sqltypes.NVARCHAR(128)),
            Column("policy_display_name", sqltypes.NVARCHAR(128)),
            Column("policy_description", sqltypes.NVARCHAR(500)),
            Column("metadata_category", sqltypes.NVARCHAR(128)),
            Column("policy_type", sqltypes.NVARCHAR(128)),
            Column("subscriptionid", String(36)),
            Column("created", DateTime),
            Column("modified", DateTime),
            Column("batch_uuid", String(36)),
        )

        policydefinitions = Table(
            "policydefinitions",
            meta,
            Column("id", Integer, primary_key=True),
            Column("policy_definition_name", sqltypes.NVARCHAR(128)),
            Column("policy_display_name", sqltypes.NVARCHAR(128)),
            Column("policy_description", sqltypes.NVARCHAR(500)),
            Column("metadata_category", sqltypes.NVARCHAR(128)),
            Column("policy_type", sqltypes.NVARCHAR(128)),
            Column("subscriptionid", String(36)),
            Column("created", DateTime),
            Column("modified", DateTime),
            Column("batch_uuid", String(36)),
        )


        test_subscriptions = Table(
            "test_subscriptions",
            meta,
            Column("id", BigInteger, primary_key=True),
            Column("subscription_id", String(36)),
            Column("subscription_display_name", sqltypes.NVARCHAR(64)),
            Column("tenant_id", String(36)),
            Column("management_grp", String(36)),
            #The current subscription display name is 64 in most Azure documentation currently
            Column("functional_owner", sqltypes.NVARCHAR(256)),
            Column("billing_contact", sqltypes.NVARCHAR(256)),
            Column("financial_owner", sqltypes.NVARCHAR(256)),
            Column("TIMESTAMP", DateTime, default=datetime.datetime.utcnow),
            Column("modified", DateTime, onupdate=datetime.datetime.now),
            Column("batch_uuid", String(36)),
        )

        subscriptions = Table(
            "subscriptions",
            meta,
            Column("id", BigInteger, primary_key=True),
            Column("subscription_id", String(36)),
            Column("subscription_display_name", sqltypes.NVARCHAR(64)),
            Column("tenant_id", String(36)),
            Column("management_grp", String(36)),
            # The current subscription display name is 64 in most Azure documentation currently
            Column("functional_owner", sqltypes.NVARCHAR(256)),
            Column("billing_contact", sqltypes.NVARCHAR(256)),
            Column("financial_owner", sqltypes.NVARCHAR(256)),
            Column("TIMESTAMP", DateTime, default=datetime.datetime.utcnow),
            Column("modified", DateTime, onupdate=datetime.datetime.now),
            Column("batch_uuid", String(36)),

        )
        meta.create_all(engine)

        return meta.tables

    @dbhookimpl
    def delete_database(self, server, database, user, password, driver):
        """
            This function creates a SQL Server 2019 for Linux database table for handling results found in analysis
            As the framework becomes more modular, multiple database initiation modules need to be created
        :return:
        """
        engine = self.get_db_engine(database, driver, password, server, user)

        m = MetaData()
        m.reflect(engine)

        m.drop_all(engine)

        return 0
