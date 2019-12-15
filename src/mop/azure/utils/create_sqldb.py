import urllib

import pluggy
from sqlalchemy import MetaData, Table, Column, Integer, String
from sqlalchemy import create_engine

dbhookimpl = pluggy.HookimplMarker("Analysis")
dbhookspec = pluggy.HookspecMarker("Analysis")


class DatbasePlugins(object):
    """A hook specification namespace."""

    @dbhookspec
    def create_database(self, server, database, user, password, driver):
        """Datbase creation hook"""

    @dbhookspec
    def delete_data(self, server, database, user, password, driver):
        """Datbase deletion hook"""

class SQLServerDatabase(object):
    """
        This class is an implementation of the dbhookspec
    """

    @dbhookimpl
    def create_database(self, server, database, user, password, driver):
        """
            This function creates a SQL Server 2019 for Linux database table for handling results found in analysis
            As the framework becomes more modular, multiple database initiation modules need to be created
        :return:
        """
        self.driver = driver
        self.server = server
        self.database = database
        self.user = user,
        self.password = password

        connect_str = \
            'DRIVER={driver};SERVER={server};DATABASE={database};UID=SA;PWD={password}' \
                .format(driver=self.driver, server=self.server, database=self.database, password=self.password)

        params = urllib.parse.quote_plus(connect_str)
        engine = create_engine("mssql+pyodbc:///?odbc_connect=%s" % params)

        # The database here is not quite formed properly with proper keys and indexes.
        #TODO establish proper data model

        m = MetaData()
        t = Table('noncompliant', m,
                  Column('id', Integer, primary_key=True),
                  Column('resource_id', String),
                  Column('management_group_ids', String),
                  Column('policy_assignment_id', String),
                  Column('policy_assignment_name', String),
                  Column('policy_assignment_owner', String),
                  Column('policy_assignment_parameters', String),
                  Column('policy_assignment_scope', String),
                  Column('policy_definition_action', String),
                  Column('policy_definition_category', String),
                  Column('policy_definition_id', String),
                  Column('policy_definition_name', String),
                  Column('policy_definition_reference_id', String),
                  Column('policy_set_definition_category', String),
                  Column('policy_set_definition_id', String),
                  Column('policy_set_definition_name', String),
                  Column('policy_set_definition_owner', String),
                  Column('policy_set_definition_parameters', String),
                  Column('resource_group', String),
                  Column('resource_location', String),
                  Column('resource_tags', String),
                  Column('resource_type', String),
                  Column('serialize', String),
                  Column('subscription_id', String),
                  Column('tenant_id', String),
                  Column('subscription_display_name', String),
                  Column('management_grp', String),
                  Column('timestamp', String))

        t2 = Table('factcompliance', m,
                   Column('id', Integer, primary_key=True),
                   Column('resource_id', String),
                   Column('subscription_id', String),
                   Column('tenant_id', String),
                   Column('policy_assignment_id', String),
                   Column('policy_definition_id', String),
                   Column('compliant', Integer),
                   Column('non-compliant', Integer))

        m.create_all(engine)

        return 0

    @dbhookimpl
    def delete_database(self, server, database, user, password, driver):
        """
            This function creates a SQL Server 2019 for Linux database table for handling results found in analysis
            As the framework becomes more modular, multiple database initiation modules need to be created
        :return:
        """
        self.driver = driver
        self.server = server
        self.database = database
        self.user = user,
        self.password = password

        connect_str = \
            'DRIVER={driver};SERVER={server};DATABASE={database};UID=SA;PWD={password}' \
                .format(driver=self.driver, server=self.server, database=self.database, password=self.password)

        params = urllib.parse.quote_plus(connect_str)
        engine = create_engine("mssql+pyodbc:///?odbc_connect=%s" % params)
