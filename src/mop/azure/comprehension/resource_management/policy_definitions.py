from configparser import ConfigParser

import pandas as pd
from azure.mgmt.resource.policy import PolicyClient
from dotenv import load_dotenv

from mop.azure.connections import request_authenticated_session, Connections
from mop.azure.utils.create_configuration import (
    change_dir,
    CONFVARIABLES,
    OPERATIONSPATH,
)


class PolicyDefinition:
    def __init__(self, credentials=None):
        load_dotenv()
        with change_dir(OPERATIONSPATH):
            self.config = ConfigParser()
            self.config.read(CONFVARIABLES)

        self.credentials = Connections().get_authenticated_client()

    def get_policy_definition(self, policy_definition_name):

        base_subscription_id = self.config['DEFAULT']['subscription_id']
        policy_client = PolicyClient(self.credentials, subscription_id=base_subscription_id)
        policy_definition = policy_client.policy_definitions.get(policy_definition_name)

        return policy_definition

    def policyinsights_generic_req(self, api_endpoint, *args):
        """
            This function can theoretically call any Azure SDK API the service pricipal has access to
        :param api_config_key:
        :param args:
        :return:
        """
        # The policyinsights_generic_req has no way of learning the named string format parameters
        # a simple replace makes the URL a workable generic call to the API
        # example: api_config_key.replace('{subscriptionId}', '{}')

        api_endpoint = api_endpoint.format(*args)

        with request_authenticated_session() as req:
            return req.post(api_endpoint)

    def policy_definitions_by_subscription_req(self, subscriptionId):
        """

        :param subscriptionId:
        :return: Policy definitions by subscription request
        """
        api_endpoint = self.config["AZURESDK"]["policydefintionsbysubscription"]
        api_endpoint = api_endpoint.format(subscriptionId=subscriptionId)

        with request_authenticated_session() as req:
            policy_definitions = req.get(api_endpoint)

        return policy_definitions

    def get_policy_definitions(self, subscription_id, policy_definition_name, authenticated_session=None):
        """

        :param subscription_id:
        :param policy_definition_name:
        :param request_authenticated_session:
        :return:
        """

        api_endpoint = self.config["AZURESDK"]["policy_definitions_get"]
        api_endpoint = api_endpoint.format(subscriptionId=subscription_id, policyDefinitionName=policy_definition_name)

        api_endpoint_2 = self.config["AZURESDK"]["get_policy_definition_by_name"]
        api_endpoint_2 = api_endpoint_2.format(policyDefinitionName=policy_definition_name)

        policy_definitions_function = None

        if authenticated_session:
            policy_definitions_function = authenticated_session.get(api_endpoint)

            if policy_definitions_function.status_code == 404:
                policy_definitions_function = authenticated_session.get(api_endpoint_2)
        else:
            with request_authenticated_session() as req:
                policy_definitions_function = req.get(api_endpoint)

                if policy_definitions_function.status_code == 404:
                    policy_definitions_function = req.get(api_endpoint_2)

        if policy_definitions_function is not None and policy_definitions_function.status_code == 200:
            return policy_definitions_function.json
        else:
            return None

def get_policydefinitions_management_grp(creds, base_subscription, management_grp):
    """
    :param creds:
    :param base_subscription:
    :param management_grp:
    :return:
    """
    policy_client = PolicyClient(
        credentials=creds, subscription_id=base_subscription)
    results = policy_client.policy_definitions.list_by_management_group(management_grp)
    return results


def get_management_grp_policies(
    creds, management_grp, subscription, policy_type="Security"
):
    """
    Retreive policies associated with Management Grp
    :param creds:
    :param management_grp:
    :param subscription:
    :param policy_type:
    :return:
    """
    policies = get_policydefinitions_management_grp(
        creds=creds, base_subscription=subscription, management_grp=management_grp
    )
    policy_defs_limited = [
        [
            policy.name,
            policy.id,
            policy.display_name,
            policy.metadata.get("category"),
            policy.policy_type,
            policy.description,
        ]
        for policy in policies
        if policy.metadata.get("category") == policy_type
    ]

    # security_policies = [policy for policy in policy_defs_limited if policy[2] == policy_type]

    return policy_defs_limited


def management_grp_policy_list(creds, subscription_id_param, management_grp):
    """
    https://docs.microsoft.com/en-us/python/api/azure-mgmt-resource/azure.mgmt.resource.policy.v2019_06_01.operations.policydefinitionsoperations?view=azure-python#list-by-management-group-management-group-id--custom-headers-none--raw-false----operation-config-
    :param creds:
    :param subscription_id_param:
    :param management_grp:
    :return:
    """

    policy_client = PolicyClient(
        credentials=creds, subscription_id=subscription_id_param, base_url=None
    )
    mangrp_policy_definitions = policy_client.policy_definitions.list_by_management_group(
        management_group_id=management_grp, custom_headers=None, raw=False
    )
    policy_defs_limited = [
        [
            policy.name,
            policy.display_name,
            policy.metadata.get("category"),
            policy.policy_type,
            policy.description,
        ]
        for policy in mangrp_policy_definitions
    ]

    return policy_defs_limited


def get_subscription_policies(subscription_id, credentials):
    policy_client = PolicyClient(credentials=credentials, subscription_id=subscription_id, base_url=None)
    policy_client.policy_definitions()
    pass
    # TODO complete this later


def management_grp_policy_list_as_df(creds, subscription_id_param, management_grp):
    list = management_grp_policy_list(creds, subscription_id_param, management_grp)
    df = pd.DataFrame(
        data=list,
        columns=[
            "policy_definition_name",
            "display_name",
            "category",
            "policy_type",
            "description",
        ],
    )
    df.set_index("policy_definition_name", inplace=True)

    return df
