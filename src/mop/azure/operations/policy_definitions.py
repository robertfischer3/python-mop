from azure.mgmt.resource.policy import PolicyClient
import pandas as pd

class PolicyDefinitions():
    pass

def get_policydefinitions_management_grp(creds, base_subscription, management_grp):
    '''
    :param creds:
    :param base_subscription:
    :param management_grp:
    :return:
    '''
    policy_client = PolicyClient(credentials=creds, subscription_id=base_subscription, base_url=None)
    results = policy_client.policy_definitions.list_by_management_group(management_grp)
    return results


def get_management_grp_policies(creds, management_grp, subscription, policy_type='Security'):
    '''
    Retreive policies associated with Management Grp
    :param creds:
    :param management_grp:
    :param subscription:
    :param policy_type:
    :return:
    '''
    policies = get_policydefinitions_management_grp(creds=creds,
                                                    base_subscription=subscription,
                                                    management_grp=management_grp)
    policy_defs_limited = [[policy.name,
                            policy.id,
                            policy.display_name,
                            policy.metadata.get("category"),
                            policy.policy_type,
                            policy.description] for policy in policies if policy.metadata.get("category") == policy_type]

    #security_policies = [policy for policy in policy_defs_limited if policy[2] == policy_type]

    return policy_defs_limited


def management_grp_policy_list(creds, subscription_id_param, management_grp):
    '''
    https://docs.microsoft.com/en-us/python/api/azure-mgmt-resource/azure.mgmt.resource.policy.v2019_06_01.operations.policydefinitionsoperations?view=azure-python#list-by-management-group-management-group-id--custom-headers-none--raw-false----operation-config-
    :param creds:
    :param subscription_id_param:
    :param management_grp:
    :return:
    '''

    policy_client = PolicyClient(credentials=creds, subscription_id=subscription_id_param, base_url=None)
    mangrp_policy_definitions = \
        policy_client.policy_definitions.list_by_management_group(management_group_id=management_grp,
                                                                  custom_headers=None,
                                                                  raw=False)
    policy_defs_limited = [
        [policy.name, policy.display_name, policy.metadata.get("category"), policy.policy_type, policy.description] for
        policy in mangrp_policy_definitions]

    return policy_defs_limited


def management_grp_policy_list_as_df(creds, subscription_id_param, management_grp):
    list = management_grp_policy_list(creds, subscription_id_param, management_grp)
    df = pd.DataFrame(data=list, columns=['policy_definition_name', 'display_name', 'category', 'policy_type', 'description'])
    df.set_index('policy_definition_name', inplace=True)

    return df