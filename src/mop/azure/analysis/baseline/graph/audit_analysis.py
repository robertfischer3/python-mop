import json
import os
from configparser import ConfigParser

from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker

from mop.azure.comprehension.graph.audit import DirectoryAudit
from mop.azure.utils.create_configuration import change_dir, OPERATIONSPATH, CONFVARIABLES
from mop.db.basedb import BaseDb


class AuditAnalysis(BaseDb):
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
        self.driver = sql_instance['db_driver']
        self.dialect = sql_instance['dialect']
        self.password = password = os.environ['DATABASEPWD']
        self.get_db_engine()

        self.Session = sessionmaker(bind=self.engine)

    def find_user_records(self):
        directory_audit = DirectoryAudit()
        audits = directory_audit.graph_directory_list_audits()

        print(audits)
