import urllib
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

class BaseDB:
    def __init__(self, driver, database, dialect, password, server, user):

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
        return engine

    def get_db_model(self, engine):

        Base = automap_base()

        # engine, suppose it has two tables 'factcompliance' and 'address' set up
        engine = self.get_db_engine()

        # reflect the tables
        Base.prepare(engine, reflect=True)

        # mapped classes are now created with names by default
        # matching that of the table name.
        factcompliance = Base.classes.factcompliance
        noncompliant = Base.classes.noncompliant

        session = Session(engine)


