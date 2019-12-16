import urllib

import sqlalchemy as db
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class BaseDB:
    def __init__(self, database, dialect, engine, password, server, user):
        self.dialect = dialect
        self.server = server
        self.database = database
        self.user = user
        self.password = password
        self.engine = engine

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
        # TODO Replace the msql with a more generalizable plugin capable format
        engine = create_engine("mssql+pyodbc:///?odbc_connect=%s" % params)
        return engine


class NonCompliantResources(Base):
    """
        Non-compliance resources model
    """
    __tablename__ = 'noncompliantresources'

    id = db.Column("id", db.Integer, primary_key=True)
    resource_id = db.Column("resource_id", db.String)
    management_group_ids = db.Column("management_group_ids", db.String)
    policy_assignment_id = db.Column("policy_assignment_id", db.String)
    policy_assignment_name = db.Column("policy_assignment_name", db.String)
    policy_assignment_owner = db.Column("policy_assignment_owner", db.String)
    policy_assignment_parameters = db.Column("policy_assignment_parameters", db.String)
    policy_assignment_scope = db.Column("policy_assignment_scope", db.String)
    policy_definition_action = db.Column("policy_definition_action", db.String)
    policy_definition_category = db.Column("policy_definition_category", db.String)
    policy_definition_id = db.Column("policy_definition_id", db.String(400))
    policy_definition_name = db.Column("policy_definition_name", db.String)
    policy_definition_reference_id = db.Column("policy_definition_reference_id", db.String)
    policy_set_definition_category = db.Column("policy_set_definition_category", db.String)
    policy_set_definition_id = db.Column("policy_set_definition_id", db.String)
    policy_set_definition_name = db.Column("policy_set_definition_name", db.String)
    policy_set_definition_owner = db.Column("policy_set_definition_owner", db.String)
    policy_set_definition_parameters = db.Column("policy_set_definition_parameters", db.String)
    resource_group = db.Column("resource_group", db.String)
    resource_location = db.Column("resource_location", db.String)
    resource_tags = db.Column("resource_tags", db.String)
    resource_type = db.Column("resource_type", db.String)
    serialize = db.Column("serialize", db.String)
    subscription_id = db.Column("subscription_id", db.String)
    tenant_id = db.Column("tenant_id", db.String)
    subscription_display_name = db.Column("subscription_display_name", db.String)
    management_grp = db.Column("management_grp", db.String)
    timestamp = db.Column("timestamp", db.String)

    def __repr__(self):
        return "NonCompliantResources({})".format(self.resource_id)

class FactComplaince(db.model):
    id  = db.Column("id", db.Integer, primary_key=True),
    resource_id = db.Column("resource_id", db.String),
    subscription_id = db.Column("subscription_id", db.String),
    tenant_id = db.Column("tenant_id", db.String),
    policy_assignment_id = db.Column("policy_assignment_id", db.String),
    policy_definition_id = db.Column("policy_definition_id", db.String(400)),
    compliant = db.Column("compliant", db.Integer),
    noncompliant = db.Column("noncompliant", db.Integer)

    def __repr__(self):
        return "FactComplaince({})".format(self.resource_id, self.compliant, self.noncompliant)
