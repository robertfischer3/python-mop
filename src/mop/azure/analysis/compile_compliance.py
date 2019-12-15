import pandas as pd

from mop.azure.operations.policy_states import ScourPolicyStatesOperations
from mop.azure.utils.create_configuration import CONFVARIABLES, change_dir, TESTINGPATH


def summarize_subscriptions(subscriptonId):
    scour_policy = ScourPolicyStatesOperations()
    execute = scour_policy.policy_states_summarize_for_subscription(subscriptonId)
    # Execute returns a method the can be executed anywhere more than once
    result = execute()

    columns = ['subscriptionId', 'policyAssignmentId', 'policySetDefinitionId', 'compliant',
               'noncompliant']

    df = pd.DataFrame(columns=columns)

    summarize_results = result['value']
    for summary in summarize_results:
        policyAssignments = summary['policyAssignments']
        dict = None
        for policy_assignment in policyAssignments:
            dict = {'subscriptionId': subscriptonId}
            dict['policyAssignmentId'] = policy_assignment['policyAssignmentId']
            dict['policySetDefinitionId'] = policy_assignment['policySetDefinitionId']

            complianceState = policy_assignment['results']['resourceDetails'][0]
            dict['compliant'] = complianceState['count']

            if len(policy_assignment['results']['resourceDetails'])!= 2:
                print(policy_assignment)

            non_complianceState = policy_assignment['results']['resourceDetails'][1]
            non_comp_state = non_complianceState['complianceState']
            dict['noncompliant'] = non_complianceState['count']
            df.append(dict, ignore_index=True)

    return df
