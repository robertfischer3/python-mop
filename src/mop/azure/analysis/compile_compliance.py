import os
from configparser import ConfigParser

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from mop.azure.operations.policy_states import ScourPolicyStatesOperations
from mop.azure.utils.create_configuration import CONFVARIABLES, change_dir, OPERATIONSPATH
from mop.db.basedb import BaseDB

class SummarizeSubscription():

    def __init__(self):
        load_dotenv()
        with change_dir(OPERATIONSPATH):
            self.config = ConfigParser()
            self.config.read(CONFVARIABLES)

        self.server = self.config['SQLSERVER']['server']
        self.database = self.config['SQLSERVER']['database']
        self.username = self.config['SQLSERVER']['username']
        self.db_driver = self.config['SQLSERVER']['db_driver']
        self.dialect = self.config['SQLSERVER']['dialect']

        password = os.environ['DATABASEPWD']

        baseDb = BaseDB(server=self.server,
               database=self.database,
               user=self.username,
               driver=self.db_driver,
               dialect=self.dialect,
               password=password)

        self.engine = baseDb.get_db_engine()
        if self.engine:
            self.factcompliance, self.noncompliant =baseDb.get_db_model(self.engine)

        if not self.factcompliance:
            raise
        if not self.noncompliant:
            raise

    def summarize_subscriptions(self, subscriptonId):
        scour_policy = ScourPolicyStatesOperations()
        execute = scour_policy.policy_states_summarize_for_subscription(subscriptonId)
        # Execute returns a method the can be executed anywhere more than once
        result = execute()
        if result:
            session = Session(self.engine)

        tenant = self.config['DEFAULT']['tenant_id']
        columns = [
            "subscriptionId",
            "policyAssignmentId",
            "policyDefinitionId",
            "compliant",
            "noncompliant",
        ]

        summarize_results = result["value"]
        for summary in summarize_results:
            policyAssignments = summary["policyAssignments"]
            dict = None
            for policy_assignment in policyAssignments:
                dict = {"subscriptionId": subscriptonId}
                dict["policyAssignmentId"] = policy_assignment["policyAssignmentId"]
                dict["policySetDefinitionId"] = policy_assignment["policySetDefinitionId"]

                if len(policy_assignment["results"]["resourceDetails"]) <= 2:
                    complianceState = policy_assignment["results"]["resourceDetails"][0]
                    if complianceState['complianceState'] in 'compliant':
                        dict["compliant"] = complianceState["count"]
                    else:
                        dict["noncompliant"] = complianceState["count"]

                if len(policy_assignment["results"]["resourceDetails"]) == 2:
                    complianceState = policy_assignment["results"]["resourceDetails"][1]
                    if complianceState['complianceState'] in 'compliant':
                        dict["compliant"] = complianceState["count"]
                    else:
                        dict["noncompliant"] = complianceState["count"]
                if not 'commpliant' in dict:
                    dict["compliant"] = 0
                if not 'noncompliant'in dict:
                    dict['noncompliant'] = 0

                    session.add(self.factcompliance(subscription_id=dict['subscriptionId'],
                                                tenant_id=tenant,
                                                policy_definition_id=dict["policySetDefinitionId"],
                                                compliant=dict["compliant"],
                                                noncompliant=dict["noncompliant"],
                                                ))
                    session.commit()
