import datetime
import jmespath
import json

from configparser import ConfigParser
from dotenv import load_dotenv
from tenacity import retry, wait_random, stop_after_attempt

from mop.framework.azure_connections import AzureConnections, request_authenticated_azure_session
from mop.azure.utils.create_configuration import (
    change_dir,
    CONFVARIABLES,
    OPERATIONSPATH,
)


class PolicyAssignments():
    def __init__(self, credentials=None):
        load_dotenv()
        with change_dir(OPERATIONSPATH):
            self.config = ConfigParser()
            self.config.read(CONFVARIABLES)

        self.credentials = AzureConnections().get_authenticated_client()

    def policy_assignments_list(self, subscriptionId):
        """

        :param subscriptionId:
        :return: Policy definitions by subscription request
        """
        api_endpoint = self.config["AZURESDK"]["policy_assignments_list"]
        api_endpoint = api_endpoint.format(subscriptionId=subscriptionId)

        with request_authenticated_azure_session() as req:
            policy_assignments_request = req.get(api_endpoint)

        return policy_assignments_request

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

        with request_authenticated_azure_session() as req:
            policy_assignment = req.put(api_endpoint,
                                        data=json.dumps(policyAssignmentBody, indent=4, ensure_ascii=False),
                                        headers=headers)

        return policy_assignment

    def create_management_group_policy_assignment_at_subscription_level(self, managementGroupId, subscriptionId,
                                                                        policyDefinitionName):
        policy_assignments = list()
        rest_api_responses = list()

        created = datetime.datetime.utcnow()

        api_endpoint = self.config['AZURESDK']['policy_definitions_get_at_management_group']
        api_endpoint = api_endpoint.format(managementGroupId=managementGroupId,
                                           policyDefinitionName=policyDefinitionName)

        with request_authenticated_azure_session() as req:
            policy_definition_response = req.get(api_endpoint)

        policy_assignment_response = None

        if policy_definition_response.status_code == 200:
            policy_definition_json = policy_definition_response.json()
            if policy_definition_json["name"]:
                id = policy_definition_json["id"]
                displayName = policy_definition_json["name"]
                description = policy_definition_json["name"]
                createdBy = ""
                category = None
                parameters = {}

                if policy_definition_json["properties"]:
                    if policy_definition_json["properties"]["displayName"]:
                        displayName = policy_definition_json["properties"]["displayName"]
                    if 'description' in policy_definition_json["properties"]:
                        description = policy_definition_json["properties"]["description"]
                    else:
                        print("No decription, using policy name: {}".format(displayName))
                    if 'parameters' in policy_definition_json["properties"]:
                        parameter_dict = policy_definition_json["properties"]['parameters']
                        defaultValues = jmespath.search("*.defaultValue", data=parameter_dict)
                        for key in parameter_dict.keys():
                            if 'defaultValue' in parameter_dict[key]:
                                value = parameter_dict[key]['defaultValue']
                                parameters[key] = {"value": value}
                        # if len(parameter_dict) > 0:
                        #     if len(parameter_dict) != len(parameters):
                        #         print("Policy assignment {} skipped".format(policyDefinitionName), len(parameter_dict),
                        #               len(parameters))
                        #         return None

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
                            "policyDefinitionId": id,
                            "parameters": parameters
                        }
                    }
                    if category:
                        policy_assignment_request_body["properties"]["metadata"]["category"] = category

                    policy_assignment_response = self.create_policy_assignment(subscriptionId=subscriptionId,
                                                                               policyAssignmentName=
                                                                               policy_definition_json["name"],
                                                                               policyAssignmentBody=policy_assignment_request_body)

        return policy_assignment_response

    def create_subscription_policy_assignment(self, subscriptionId, policy_definitions_dict):

        policy_assignments = list()
        rest_api_responses = list()

        for p in policy_definitions_dict:
            if p["policy_defintion_name"]:
                policy_definition_name = p["policy_defintion_name"]
                api_endpoint = self.config["AZURESDK"]["policy_definitions_get"]
                api_endpoint = api_endpoint.format(subscriptionId=subscriptionId,
                                                   policyDefinitionName=policy_definition_name)

                with request_authenticated_azure_session() as req:
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
