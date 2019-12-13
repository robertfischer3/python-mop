import sqlalchemy as db

import uuid
import pandas as pd


class BaseDB():

    def initialize(self, engine_string):

        engine = db.create_engine(engine_string) #Create test.sqlite automatically
        connection = engine.connect()
        metadata = db.MetaData()

        emp = db.Table('emp', metadata,
                      db.Column('Id', db.Integer()),
                      db.Column('name', db.String(255), nullable=False),
                      db.Column('salary', db.Float(), default=100.0),
                      db.Column('active', db.Boolean(), default=True)
                      )
