import unittest
import pluggy
from dotenv import load_dotenv
from sqlalchemy.sql import text
from sqlalchemy import create_engine
import pyodbc
import secrets
import urllib
import os

from mop.azure.utils.create_sqldb import SQLServerDatabase, DatbasePlugins


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        load_dotenv()

        #Never place passwords in code.  Your just asking for trouble otherwise
        self.password = os.environ['DATABASEPWD']

    def test_create_database(self):
        #Testing the pluggy architecture and database creation code

        # The driver often needs to be obtained from the database publisher
        driver = '{ODBC Driver 17 for SQL Server}'
        # Server is the IP address or DNS of the database server
        server = '172.17.0.1'
        # Can be any database name, as long as you are consistent
        database = 'TestDB'

        # Do not use SA
        user = 'SA'
        # Do not store the password in this file
        password = self.password

        pm = pluggy.PluginManager("Analysis")
        pm.add_hookspecs(DatbasePlugins)
        pm.register(SQLServerDatabase())

        tables = pm.hook.create_database(server=server,
                                          database=database,
                                          user=user,
                                          password=password,
                                          driver=driver)

        self.assertIsNotNone(tables)

    def test_delete_database(self):
        # Testing the pluggy architecture and database creation code

        # The driver often needs to be obtained from the database publisher
        driver = '{ODBC Driver 17 for SQL Server}'
        # Server is the IP address or DNS of the database server
        server = '172.17.0.1'
        # Can be any database name, as long as you are consistent
        database = 'TestDB'

        # Do not use SA
        user = 'SA'
        # Do not store the password in this file
        password = self.password

        pm = pluggy.PluginManager("Analysis")
        pm.add_hookspecs(DatbasePlugins)
        pm.register(SQLServerDatabase())

        result = pm.hook.delete_database(server=server,
                                         database=database,
                                         user=user,
                                         password=password,
                                         driver=driver)

        self.assertEqual(result, [0])

    def test_something(self):
        #Testing pyodbc
        # Some other example server values are
        # server = 'localhost\sqlexpress' # for a named instance
        # server = 'myserver,port' # to specify an alternate port
        server = 'tcp:172.17.0.1'
        database = 'TestDB'
        username = 'SA'
        password = self.password
        cnxn = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
        cursor = cnxn.cursor()

        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
