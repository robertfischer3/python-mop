import os
import unittest
import uuid
from configparser import ConfigParser

import pandas as pd
import pluggy
import pyodbc
from dotenv import load_dotenv

from mop.azure.analysis.compile_compliance import subscription_policy_compliance
from mop.azure.comprehension.resources.subscriptions import Subscriptions
from mop.azure.utils.create_configuration import change_dir, OPERATIONSPATH, TESTVARIABLES
from mop.azure.utils.create_sqldb import SQLServerDatabase, DatbasePlugins
from mop.db.basedb import BaseDb


class TestUtilDb(unittest.TestCase):
    def setUp(self) -> None:
        load_dotenv()
        with change_dir(OPERATIONSPATH):
            self.config = ConfigParser()
            self.config.read(TESTVARIABLES)
        # The driver often needs to be obtained from the database publisher
        self.driver = "{ODBC Driver 17 for SQL Server}"
        # Server is the IP address or DNS of the database server
        self.server = "172.17.0.1"
        # Can be any database name, as long as you are consistent
        self.database = "TestDB3"
        # Never place passwords in code.  Your just asking for trouble otherwise
        self.password = os.environ["DATABASEPWD"]
        # Do not use SA in production
        self.user = "SA"

    def test_create_database(self):
        sql_db = SQLServerDatabase()
        tables = sql_db.create_database_tables(driver=self.driver,
                                               server=self.server,
                                               database=self.database,
                                               user=self.user,
                                               password=self.password, )

        self.assertIsNotNone(tables)

    def test_create_database_pluggy(self):
        # Testing the pluggy architecture and database creation code

        pm = pluggy.PluginManager("Analysis")
        pm.add_hookspecs(DatbasePlugins)
        pm.register(SQLServerDatabase())

        tables = pm.hook.create_database_tables(
            server=self.server,
            database=self.database,
            user=self.user,
            password=self.password,
            driver=self.driver,
        )

        self.assertIsNotNone(tables)

    def test_get_database_engine_pluggy(self):
        pm = pluggy.PluginManager("Analysis")
        pm.add_hookspecs(DatbasePlugins)
        pm.register(SQLServerDatabase())
        engine = pm.hook.get_db_engine(
            driver=self.driver,
            server=self.server,
            database=self.database,
            user=self.user,
            password=self.password,
        )
        self.assertIsNotNone(engine)

    def test_pandas_dataframe_to_sql_pluggy(self):

        pm = pluggy.PluginManager("Analysis")
        pm.add_hookspecs(DatbasePlugins)
        pm.register(SQLServerDatabase())
        engine_list = pm.hook.get_db_engine(
            driver=self.driver,
            server=self.server,
            database=self.database,
            user=self.user,
            password=self.password,
        )
        engine = engine_list[0]
        # Create dataframe
        data = pd.DataFrame({
            'book_id': [uuid.uuid1(), uuid.uuid1(), uuid.uuid1()],
            'title': ['Python Programming for Freaks', 'Learn Something', 'Data Science for the Masses'],
            'price': [32, 22, 29]
        })

        data.to_sql('book_details', con=engine, if_exists='append', chunksize=1000)

    def test_pandas_dataframe_subscriptions_to_sql_pluggy(self):
        pm = pluggy.PluginManager("Analysis")
        pm.add_hookspecs(DatbasePlugins)
        pm.register(SQLServerDatabase())
        engine_list = pm.hook.get_db_engine(
            driver=self.driver,
            server=self.server,
            database=self.database,
            user=self.user,
            password=self.password,
        )
        engine = engine_list[0]
        management_grp = os.environ["MANGRP"]

        subscriptions = Subscriptions().list_management_grp_subcriptions(management_grp=management_grp)
        subscriptions.reset_index(inplace=True)
        subscriptions.to_sql('subscriptions', index=False, con=engine, if_exists='append', chunksize=1000)

    def test_pandas_dataframe_policy_states_summarize_for_subscription_pluggy(self):

        pm = pluggy.PluginManager("Analysis")
        pm.add_hookspecs(DatbasePlugins)
        pm.register(SQLServerDatabase())
        engine_list = pm.hook.get_db_engine(
            driver=self.driver,
            server=self.server,
            database=self.database,
            user=self.user,
            password=self.password,
        )

        subscriptionId = self.config["DEFAULT"]["subscription_id"]
        df = subscription_policy_compliance(subscriptionId)

        self.assertTrue(len(df.index) > 0)

        engine = engine_list[0]

        df.to_sql('test_policy_compliance_ratios', index=False, con=engine, if_exists='append', chunksize=1000)

    def test_delete_database(self):
        # Testing the pluggy architecture and database creation code

        pm = pluggy.PluginManager("Analysis")
        pm.add_hookspecs(DatbasePlugins)
        pm.register(SQLServerDatabase())

        result = pm.hook.delete_database(
            server=self.server,
            database=self.database,
            user=self.user,
            password=self.password,
            driver=self.driver,
        )

        self.assertEqual(result, [0])

    def test_base_class_sqlserver_pluggy(self):
        """
         Testing base class for coverage only.  Class will be developed later
        :return:
        """
        server = "tcp:172.17.0.1"
        database = "TestDB2"
        username = "SA"
        password = self.password
        db_driver = "{ODBC Driver 17 for SQL Server}"

        baseDb = BaseDb(
            server=server,
            database=database,
            user=username,
            password=password,
            driver=db_driver,
            dialect="mssql",
        )
        self.assertIsNotNone(baseDb)

        engine = baseDb.get_db_engine()
        self.assertIsNotNone(engine)

        factcompliance, noncompliance, subscriptions = baseDb.get_db_model(engine=engine)

        if subscriptions:

            for subscription in subscriptions:
                print(subscription.subscription_id)

    def test_something(self):
        # Testing pyodbc
        # Some other example server values are
        # server = 'localhost\sqlexpress' # for a named instance
        # server = 'myserver,port' # to specify an alternate port
        server = "tcp:172.17.0.1"
        database = "TestDB2"
        username = "SA"
        password = self.password
        cnxn = pyodbc.connect(
            "DRIVER={ODBC Driver 17 for SQL Server};SERVER="
            + server
            + ";DATABASE="
            + database
            + ";UID="
            + username
            + ";PWD="
            + password
        )
        cursor = cnxn.cursor()

        self.assertIsNotNone(cursor)


if __name__ == "__main__":
    unittest.main()
