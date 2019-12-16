import os
import unittest

import pluggy
import pyodbc
from dotenv import load_dotenv

from mop.azure.utils.create_sqldb import SQLServerDatabase, DatbasePlugins
from mop.db.basedb import BaseDB


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        load_dotenv()

        # Never place passwords in code.  Your just asking for trouble otherwise
        self.password = os.environ["DATABASEPWD"]

    def test_create_database(self):
        # Testing the pluggy architecture and database creation code

        # The driver often needs to be obtained from the database publisher
        driver = "{ODBC Driver 17 for SQL Server}"
        # Server is the IP address or DNS of the database server
        server = "172.17.0.1"
        # Can be any database name, as long as you are consistent
        database = "TestDB2"

        # Do not use SA
        user = "SA"
        # Do not store the password in this file
        password = self.password

        pm = pluggy.PluginManager("Analysis")
        pm.add_hookspecs(DatbasePlugins)
        pm.register(SQLServerDatabase())

        tables = pm.hook.create_database(
            server=server,
            database=database,
            user=user,
            password=password,
            driver=driver,
        )

        self.assertIsNotNone(tables)

    def test_delete_database(self):
        # Testing the pluggy architecture and database creation code

        # The driver often needs to be obtained from the database publisher
        driver = "{ODBC Driver 17 for SQL Server}"
        # Server is the IP address or DNS of the database server
        server = "172.17.0.1"
        # Can be any database name, as long as you are consistent
        database = "TestDB2"

        # Do not use SA
        user = "SA"
        # Do not store the password in this file
        password = self.password

        pm = pluggy.PluginManager("Analysis")
        pm.add_hookspecs(DatbasePlugins)
        pm.register(SQLServerDatabase())

        result = pm.hook.delete_database(
            server=server,
            database=database,
            user=user,
            password=password,
            driver=driver,
        )

        self.assertEqual(result, [0])

    def test_base_class_sqlserver(self):
        """
         Testing base class for coverage only.  Class will be developed later
        :return:
        """
        server = "tcp:172.17.0.1"
        database = "TestDB"
        username = "SA"
        password = self.password
        db_driver = "{ODBC Driver 17 for SQL Server}"

        baseDb = BaseDB(
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

        baseDb.get_db_model(engine=engine)

    def test_something(self):
        # Testing pyodbc
        # Some other example server values are
        # server = 'localhost\sqlexpress' # for a named instance
        # server = 'myserver,port' # to specify an alternate port
        server = "tcp:172.17.0.1"
        database = "TestDB"
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
