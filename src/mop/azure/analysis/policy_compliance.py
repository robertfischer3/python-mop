import os
from configparser import ConfigParser

import jmespath
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker

from mop.azure.connections import request_authenticated_session
from mop.azure.operations.policy_states import ScourPolicyStatesOperations
from mop.azure.comprehension.resource_management.policy_definitions import PolicyDefinition
from mop.azure.utils.create_configuration import CONFVARIABLES, change_dir, OPERATIONSPATH
from mop.db.basedb import BaseDb


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

        self.baseDb = BaseDb(server=self.server,
                             database=self.database,
                             user=self.username,
                             driver=self.db_driver,
                             dialect=self.dialect,
                             password=password)

        self.engine = self.baseDb.get_db_engine()
        self.Session = sessionmaker(bind=self.engine)

    def summarize_query_results_for_policy_definitions(self):

        models = self.baseDb.get_db_model(self.engine)
        FactCompliance = models.classes.fact_compliance
        SCIDimPolicies = models.classes.sci_dim_policies

        session = self.Session()
        results = session.query(FactCompliance).all()
        pf = session.query(SCIDimPolicies).all()

        policies_found = list()
        for row in pf:
            policies_found.append(row.policy_definition_name)

        bulk_insert = list()

        try:

            for row in results:
                print(row.subscription_id, row.policy_definition_name)
                if row.policy_definition_name not in policies_found:
                    with request_authenticated_session() as req:
                        policy = PolicyDefinition().get_policy_definitions(row.subscription_id, row.policy_definition_name, req)
                        if policy:
                            policy_defintion = policy()

                            displayName = policy_defintion['properties']['displayName']
                            description = policy_defintion['properties']['description']
                            policyType = policy_defintion['properties']['policyType']
                            if 'category' in policy_defintion['properties']['metadata']:
                                category = policy_defintion['properties']['metadata']['category']
                            else:
                                category = ''
                            print(displayName)
                            policy = SCIDimPolicies(policy_definition_name=row.policy_definition_name,
                                           policy_description=description,
                                           policy_display_name=displayName,
                                           policy_type=policyType,
                                           policy_category=category)

                            policies_found.append(policy.policy_definition_name)
                            bulk_insert.append(policy)



        except ConnectionError:
            pass
        finally:
            session.bulk_save_objects(bulk_insert)
            session.commit()

    def summarize_subscriptions(self, management_grp):
        # create a configured "Session" class

        # create a Session
        session = Session()
        # Execute returns a method the can be executed anywhere more than once
        models = self.baseDb.get_db_model(self.engine)
        subscriptions = models.classes.subscriptions
        FactCompliance = models.classes.fact_compliance
        session = self.Session()
        results = session.query(subscriptions).all()

        for row in results:
            print(row.subscription_display_name)
            if row.subscription_id:
                df = subscription_policy_compliance(row.subscription_id)
                if df is None: continue
                bulk_insert = list()
                for index, dfrow in df.iterrows():
                    fact = FactCompliance(
                        subscription_id=row.subscription_id,
                        policy_definition_name=dfrow['policy_definition_name'],
                        policy_definition_id=dfrow['policy_definition_id'],
                        compliant=dfrow['compliant'],
                        noncompliant=dfrow['noncompliant'],
                        total_resources_measured=dfrow['total_resources_measured'],
                        percent_compliant=dfrow['percent_compliant'])
                    bulk_insert.append(fact)
                session.bulk_save_objects(bulk_insert)
                session.commit()


def determine_compliance_ratio(resourceDetails):
    compliance_dict = dict()
    if len(resourceDetails) <= 2:
        complianceState = resourceDetails[0]
        if complianceState['complianceState'] in 'compliant':
            compliance_dict["compliant"] = int(complianceState["count"])
        else:
            compliance_dict["noncompliant"] = int(complianceState["count"])
    if len(resourceDetails) == 2:
        complianceState = resourceDetails[1]
        if complianceState['complianceState'] in 'compliant':
            compliance_dict["compliant"] = int(complianceState["count"])
        else:
            compliance_dict["noncompliant"] = int(complianceState["count"])
    if not 'compliant' in compliance_dict:
        compliance_dict["compliant"] = 0
    if not 'noncompliant' in compliance_dict:
        compliance_dict['noncompliant'] = 0

    compliance_dict['total_resources_measured'] = compliance_dict["compliant"] + compliance_dict['noncompliant']
    compliance_dict['percent_compliant'] = compliance_dict["compliant"] / compliance_dict[
        'total_resources_measured'] * 100

    return compliance_dict


def subscription_policy_compliance(subscriptionId):
    with change_dir(OPERATIONSPATH):
        config = ConfigParser()
        config.read(CONFVARIABLES)

    jmespath_expression = jmespath.compile("value[*].policyAssignments[*].policyDefinitions[*]")
    jmespath_results = jmespath.compile("[0].results.resourceDetails")
    scour_policy = ScourPolicyStatesOperations()
    response = scour_policy.policy_states_summarize_for_subscription(subscriptionId)

    # Execute returns a method the can be executed anywhere more than once
    result = response.json()
    df = pd.DataFrame(columns=['subscription_id',
                               'policy_definition_name',
                               'policy_definition_id',
                               'compliant',
                               'noncompliant',
                               'total_resources_measured',
                               'percent_compliant'])
    jmes_result = jmespath_expression.search(result)

    if jmespath_expression is None or jmes_result is None or jmes_result[0] is None:
        return
    else:
        # flatten results
        try:

            policyresults = jmes_result[0][0]
            for policyresult in policyresults:
                policy_definition_name = str(policyresult['policyDefinitionId']).split('/')[-1]
                resourceDetails = jmespath.search('results.resourceDetails[*]', policyresult)

                compliance_ratio = determine_compliance_ratio(resourceDetails)
                new_row = {'subscription_id': subscriptionId,
                           'policy_definition_name': policy_definition_name,
                           'policy_definition_id': policyresult['policyDefinitionId'],
                           'compliant': compliance_ratio['compliant'],
                           'noncompliant': compliance_ratio['noncompliant'],
                           'total_resources_measured': compliance_ratio['total_resources_measured'],
                           'percent_compliant': compliance_ratio['percent_compliant'],
                           }

                df = df.append(new_row, ignore_index=True)

        except IndexError:
            return None

    return df
