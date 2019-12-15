import unittest
import pluggy
from dotenv import load_dotenv
from sqlalchemy.sql import text
from sqlalchemy import create_engine
import pyodbc
import secrets
import urllib
import os

from mop.azure.utils.create_sqldb import SQLServerDatabase


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        load_dotenv()
        self.password = os.environ['DATABASEPWD']

    def test_create_database(self):
        sql = SQLServerDatabase()
        sql.create_basic_analysis_database()

    def test_something(self):

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
