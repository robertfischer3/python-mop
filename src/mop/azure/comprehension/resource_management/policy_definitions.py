import glob
import json
import os
from configparser import ConfigParser

import pandas as pd
from azure.mgmt.resource.policy import PolicyClient
from dotenv import load_dotenv
from tenacity import retry, wait_random, stop_after_attempt

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

    @retry(wait=wait_random(min=1, max=2), stop=stop_after_attempt(4))
    def get_policy_definition(self, subscription_id, policy_definition_name):
        """

        :param subscription_id:
        :param policy_definition_name:
        :return:
        """
        policy_client = PolicyClient(self.credentials, subscription_id=subscription_id)
        policy_definition = policy_client.policy_definitions.get(policy_definition_name)

        return policy_definition

    retry(wait=wait_random(min=1, max=3), stop=stop_after_attempt(4))
    def create_subscription_policy_definition(self, subscriptionId):

        results = {}
        definitions = self.get_json_policy_definitions()
        for p in definitions:
            with open(p["policy_definition_path"], "r") as pol_def_file:
                pol_def_contents = pol_def_file.read()
                result = self.create_policy_definition(
                    subscriptionId=subscriptionId,
                    policy_definition_name=p["policy_defintion_name"],
                    policy_definition_body=pol_def_contents)
                results[p["policy_defintion_name"]] = result
        return results

    def get_json_policy_definitions(self):
        paths = list()
        if os.getcwd().endswith("tests"):
            search_path = "../comprehension/resource_management/policydefinitions"
        else:
            search_path = "policydefinitions"
        with change_dir(search_path):
            for file in glob.glob("*.json"):
                policy_definition_path = os.path.abspath(file)
                base_name = os.path.basename(policy_definition_path)
                policy_defintion_name = os.path.splitext(base_name)[0]
                if not os.path.isfile(policy_definition_path):
                    raise FileNotFoundError
                paths.append(
                    {"policy_defintion_name": policy_defintion_name, "policy_definition_path": policy_definition_path})
        return paths

    retry(wait=wait_random(min=1, max=3), stop=stop_after_attempt(4))

    def create_management_group_definition(self, managementGroupId, policyDefinitionName, policy_definition_body):

        api_endpoint = self.config["AZURESDK"]['policy_definitions_create_or_update_at_management_group']
        api_endpoint = api_endpoint.format(managementGroupId=managementGroupId,
                                           policyDefinitionName=policyDefinitionName)

        headers = {'content-type': 'application/json'}

        with request_authenticated_session() as req:
            policy_definition = req.put(api_endpoint, data=policy_definition_body, headers=headers)

        return policy_definition

    def create_subscription_policy_assignment(self, subscriptionId, policy_definitions_dict):

        policy_assignments = list()
        rest_api_responses = list()

        for p in policy_definitions_dict:
            if p["policy_defintion_name"]:
                policy_definition_name = p["policy_defintion_name"]
                api_endpoint = self.config["AZURESDK"]["policy_definitions_get"]
                api_endpoint = api_endpoint.format(subscriptionId=subscriptionId,
                                                   policyDefinitionName=policy_definition_name)

                with request_authenticated_session() as req:
                    policy_definition = req.get(api_endpoint)
                    rest_api_responses.append(policy_definition)

                if policy_definition.status_code == 200:
                    policy_definition_json = policy_definition.json()
                    if policy_definition_json["name"]:
                        id = policy_definition_json["id"]
                        displayName = policy_definition_json["name"]
                        description = policy_definition_json["name"]
                        createdBy = ""
                        category = None

                        if policy_definition_json["properties"]:
                            if policy_definition_json["properties"]["displayName"]:
                                displayName = policy_definition_json["properties"]["displayName"]
                            if policy_definition_json["properties"]["description"]:
                                description = policy_definition_json["properties"]["description"]
                            if policy_definition_json["properties"]["metadata"]:
                                createdBy = policy_definition_json["properties"]["metadata"]["createdBy"]
                                if "metadata" in policy_definition_json["properties"] and "category" in \
                                    policy_definition_json["properties"]["metadata"]:
                                    category = policy_definition_json["properties"]["metadata"]["category"]

                            policy_assignment_request_body = {
                                "properties": {
                                    "displayName": displayName,
                                    "description": description,
                                    "metadata": {
                                        "assignedBy": createdBy
                                    },
                                    "policyDefinitionId": id
                                }
                            }
                            if category:
                                policy_assignment_request_body["properties"]["metadata"]["category"] = category

                            policy_assignment = self.create_policy_assignment(subscriptionId=subscriptionId,
                                                                              policyAssignmentName=
                                                                              policy_definition_json["name"],
                                                                              policyAssignmentBody=policy_assignment_request_body)


                            if policy_assignment:
                                    policy_assignments.append(policy_assignment)

        return policy_assignments, rest_api_responses

    def list_subscription_policy_definition_by_category(self, subscriptionId, category):
        """
        Finds the policies within a category
        :param subscriptionId:
        :param category:
        :return:
        """

        defintion_list_function = self.policy_definitions_by_subscription_req(
            subscriptionId=subscriptionId)

        results = defintion_list_function.json()
        category_policies = list()
        if 'value' not in results:
            return None

        policies = results['value']
        for policy in policies:
            if 'category' in policy['properties']['metadata']:
                if policy['properties']['metadata']['category'] in category:
                    category_policies.append(policy)

        return category_policies

    @retry(wait=wait_random(min=1, max=2), stop=stop_after_attempt(2))
    def create_policy_assignment(self, subscriptionId, policyAssignmentName, policyAssignmentBody):
        """

        :param subscriptionId:
        :param policy_definition_name:
        :param policy_definition_body:
        :return:
        """
        api_endpoint = self.config["AZURESDK"]["policy_assignments_create"]
        api_endpoint = api_endpoint.format(subscriptionId=subscriptionId, policyAssignmentName=policyAssignmentName)
        headers = {'content-type': 'application/json'}

        with request_authenticated_session() as req:
            policy_assignment = req.put(api_endpoint,
                                        data=json.dumps(policyAssignmentBody, indent=4, ensure_ascii=False),
                                        headers=headers)

        return policy_assignment

    @retry(wait=wait_random(min=1, max=2), stop=stop_after_attempt(2))
    def create_policy_definition(self, subscriptionId, policy_definition_name, policy_definition_body):
        """

        :param subscriptionId:
        :param policy_definition_name:
        :param policy_definition_body:
        :return:
        """
        api_endpoint = self.config["AZURESDK"]["policy_definitions_create_or_update"]
        api_endpoint = api_endpoint.format(subscriptionId=subscriptionId, policyDefinitionName=policy_definition_name)
        headers = {'content-type': 'application/json'}

        with request_authenticated_session() as req:
            policy_definitions = req.put(api_endpoint, data=policy_definition_body, headers=headers)

        return policy_definitions

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

    @retry(wait=wait_random(min=1, max=2), stop=stop_after_attempt(4))
    def policy_definition_via_policyDefinitionId(self, policyDefinitionId):
        management_root = self.config['AZURESDK']['management_root']
        api_version = self.config['AZURESDK']['apiversion']
        api_endpoint = "{management_root}{policyDefinitionId}?api-version={api_version}".format(
            management_root=management_root,
            policyDefinitionId=policyDefinitionId,
            api_version=api_version)

        with request_authenticated_session() as req:
            policy_definitions = req.get(api_endpoint)

        return policy_definitions

    @retry(wait=wait_random(min=1, max=2), stop=stop_after_attempt(4))
    def policy_definitions_by_subscription_req(self, subscriptionId):
        """

        :param subscriptionId:
        :return: Policy definitions by subscription request
        """
        api_endpoint = self.config["AZURESDK"]["policy_definitions_list"]
        api_endpoint = api_endpoint.format(subscriptionId=subscriptionId)

        with request_authenticated_session() as req:
            policy_definitions = req.get(api_endpoint)

        return policy_definitions

    @retry(wait=wait_random(min=1, max=2), stop=stop_after_attempt(4))
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

    @retry(wait=wait_random(min=1, max=2), stop=stop_after_attempt(2))
    def policy_definitions_list_by_management_group(self, management_grp, authenticated_session=None):

        api_endpoint = self.config["AZURESDK"]["policy_definitions_list_by_management_group"]
        api_endpoint = api_endpoint.format(managementGroupId=management_grp)

        if authenticated_session:
            response = authenticated_session.get(api_endpoint)
        else:
            with request_authenticated_session() as req:
                response = req.get(api_endpoint)
        if response is not None and response.status_code == 200:
            return response
        else:
            return None

    def list_by_management_group_category(self, managementGroupId, search_category=''):

        policy_definitions = PolicyDefinition()
        in_category_policies = []

        response = policy_definitions.policy_definitions_list_by_management_group(managementGroupId)

        if response.status_code >= 200 and response.status_code <= 299:
            results = response.json()
            if search_category is None:
                return results['value']

            policies = results['value']
            for policy in policies:
                if 'category' in policy['properties']['metadata'] and search_category in \
                    policy['properties']['metadata']['category']:
                    in_category_policies.append(policy)

        return in_category_policies

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
