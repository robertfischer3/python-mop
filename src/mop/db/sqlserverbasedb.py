import os
import urllib

from mop.db.basedb import BaseDb
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine


class SQLServerBaseDb(BaseDb):
    def __init__(self, instance_name="instance01"):
        db_driver = self.config['SQLSERVER'][instance_name]['db_driver']
        dialect = self.config['SQLSERVER'][instance_name]['dialect']
        server = self.config['SQLSERVER'][instance_name]['server']
        database = self.config['SQLSERVER'][instance_name]['database']
        username = self.config['SQLSERVER'][instance_name]['username']

        password = os.environ['DATABASEPWD']

        super(driver=db_driver, server=server, database=database, dialect=dialect, user=username, password=password)

    def get_db_engine(self):
        """
                 Creates SQL Datase engine
                :param database:
                :param driver:
                :param password:
                :param server:
                :param user:
                :return: database engine
                """
        connect_str = "DRIVER={driver};SERVER={server};DATABASE={database};UID=SA;PWD={password}".format(
            driver=self.driver,
            server=self.server,
            database=self.database,
            password=self.password,
        )
        params = urllib.parse.quote_plus(connect_str)
        engine_str = "{dialect}+pyodbc:///?odbc_connect=%s".format(dialect=self.dialect)
        engine = create_engine(engine_str % params)
        self.engine = engine

        return self.engine

    def get_db_model(self, engine):
        """

        :param engine:
        :return:
        """

        Base = automap_base()
        Base.prepare(engine, reflect=True)

        return Base
