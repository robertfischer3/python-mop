import urllib

import pluggy
from sqlalchemy import MetaData, Table, Column, Integer, String, Float
from sqlalchemy import create_engine
from mop.azure.analysis.analysis_db import AnalysisDb

dbhookimpl = pluggy.HookimplMarker("Analysis")
dbhookspec = pluggy.HookspecMarker("Analysis")


class DatbasePlugins(object):
    """A hook specification namespace."""

    @dbhookspec
    def create_database(self, server, database, user, password, driver):
        """Datbase creation hook"""

    @dbhookspec
    def get_db_engine(self, driver, server, database, password, user):
        """Get database engine hook"""

    @dbhookspec
    def delete_data(self, server, database, user, password, driver):
        """Datbase deletion hook"""


class SQLServerDatabase(object):
    """
        This class is an implementation of the dbhookspec
    """

    @dbhookimpl
    def get_db_engine(self, driver, server, database, password, user):
        """
         Creates SQL Datase engine
        :param database:
        :param driver:
        :param password:
        :param server:
        :param user:
        :return: database engine
        """
        self.driver = driver
        self.server = server
        self.database = database
        self.user = (user,)
        self.password = password
        connect_str = "DRIVER={driver};SERVER={server};DATABASE={database};UID=SA;PWD={password}".format(
            driver=self.driver,
            server=self.server,
            database=self.database,
            password=self.password,
        )
        params = urllib.parse.quote_plus(connect_str)
        engine = create_engine("mssql+pyodbc:///?odbc_connect=%s" % params)
        return engine

    @dbhookimpl
    def create_database(self, server, database, user, password, driver):
        """
            This function creates a SQL Server 2019 for Linux database table for handling results found in analysis
            As the framework becomes more modular, multiple database initiation modules need to be created
        :return:
        """
        engine = self.get_db_engine(database, driver, password, server, user)

        # The database here is not quite formed properly with proper keys and indexes.
        # TODO establish proper data model

        meta = MetaData()

        factcompliance = Table(
            "factcompliance",
            meta,
            Column("id", Integer, primary_key=True),
            Column("resource_id", String),
            Column("subscription_id", String(36)),
            Column("tenant_id", String(36)),
            Column("policy_definition_name", String(36)),
            Column("policy_assignment_id", String),
            Column("policy_definition_id", String),
            Column("compliant", Integer),
            Column("noncompliant", Integer),
            Column("total_resources_measured", Integer),
            Column("percent_compliant", Float)

        )


        policydefinitions = Table(
            "policydefinitions",
            meta,
            Column("id", Integer, primary_key=True),
            Column("policy_definition_name", String(36)),
            Column("policy_display_name"),
        )



        subscriptions = Table(
            "subscriptions",
            meta,
            Column("id", Integer, primary_key=True),
            Column("tenant_id", String(36)),
            Column("subscription_id", String(36)),
            Column("management_grp", String(36)),
            Column("subscription_display_name", String),

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
