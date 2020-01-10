import urllib
from configparser import ConfigParser

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from mop.azure.utils.create_configuration import OPERATIONSPATH, change_dir, CONFVARIABLES, TESTVARIABLES


class BaseDb:
    def __init__(self, driver, database, dialect, password, server, user, configuration_file="CONFVARIABLES"):

        with change_dir(OPERATIONSPATH):
            self.config = ConfigParser()
            if "CONFVARIABLES" in configuration_file:
                self.config.read(CONFVARIABLES)
            else:
                self.config.read(TESTVARIABLES)

        self.driver = driver
        self.dialect = dialect
        self.server = server
        self.database = database
        self.user = user
        self.password = password

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


