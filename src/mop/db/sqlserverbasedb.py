from mop.db.basedb import BaseDb


class SQLServerBaseDb(BaseDb):
    def __init__(self, instance_name="instance01"):
        db_driver = self.config['SQLSERVER'][instance_name]['db_driver']
        dialect = self.config['SQLSERVER'][instance_name]['dialect']
        server = self.config['SQLSERVER'][instance_name]['server']
        database = self.config['SQLSERVER'][instance_name]['database']
        username = self.config['SQLSERVER'][instance_name]['username']

        password = os.environ['DATABASEPWD']

        super(driver=db_driver, server=server, database=database, dialect=dialect, user=username, password=password)
