import json
import logging
import uuid
from configparser import ConfigParser
from tenacity import retry, wait_random, stop_after_attempt
from dotenv import load_dotenv

from mop.azure.connections import request_authenticated_session, Connections
from mop.azure.utils.create_configuration import (
    change_dir,
    CONFVARIABLES,
    OPERATIONSPATH,
)


class PolicySetDefinition:
    def __init__(self, credentials=None):
        load_dotenv()
        with change_dir(OPERATIONSPATH):
            self.config = ConfigParser()
            self.config.read(CONFVARIABLES)

        logging_level = int(self.config['LOGGING']['level'])
        logging.basicConfig(level=logging_level)
        if credentials:
            self.credentials = credentials
        else:
            self.credentials = Connections().get_authenticated_client()

    def list(self, subscriptionId, policySetDefinitionName):
        api_endpoint = self.config["AZURESDK"]["policy_set_definitions_create_or_update"]
        api_endpoint = api_endpoint.format(subscriptionId=subscriptionId,
                                           policySetDefinitionName=policySetDefinitionName)

        with request_authenticated_session() as req:
            policy_set_definition = req.get(api_endpoint)

        return policy_set_definition

    @retry(wait=wait_random(min=1, max=2), stop=stop_after_attempt(2))
    def create_or_update(self, subscriptionId,
                         policySetDefinitionName,
                         policy_set_properties_body,
                         policyDefinitionsList,
                         policyDefinitionReferenceId):

        api_endpoint = self.config["AZURESDK"]["policy_set_definitions_create_or_update"]
        api_endpoint = api_endpoint.format(subscriptionId=subscriptionId,
                                           policySetDefinitionName=policySetDefinitionName)
        parameters_dict = {}
        policyDefinitionReference = []
        policyDefinitionId = ''
        for policyDefinition in policyDefinitionsList:

            if 'properties' in policyDefinition and 'policyDefinitionId' in policyDefinition['properties']:
                if 'parameters' in policyDefinition:
                    parameters_dict = policyDefinition['parameters']

                policyDefinition = {
                    "policyDefinitionId": policyDefinition['properties']['policyDefinitionId'],
                    "policyDefinitionReferenceId": policyDefinitionReferenceId + str(uuid.uuid4()),
                    "parameters": parameters_dict
                }

                policyDefinitionReference.append(policyDefinition)

        policy_set_properties_body['properties']['policyDefinitions'] = policyDefinitionReference
        headers = {'content-type': 'application/json'}

        policy_set_properties_body = json.dumps(policy_set_properties_body)

        with request_authenticated_session() as req:
            policy_set_definition = req.put(api_endpoint, data=policy_set_properties_body, headers=headers)

        return policy_set_definition
