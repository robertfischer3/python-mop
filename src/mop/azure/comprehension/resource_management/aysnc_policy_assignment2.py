import json
import re
from re import Pattern

import aiohttp
import jmespath
from codetiming import Timer
from configparser import ConfigParser
from dotenv import load_dotenv
from azure.storage.queue.aio import QueueClient
import asyncio
from mop.azure.comprehension.storage.async_storage_queue import AsyncStorageQueue
from mop.framework.azure_connections import AzureConnections, request_authenticated_azure_session, \
    AzureSDKAuthentication
from mop.azure.utils.create_configuration import (
    change_dir,
    CONFVARIABLES,
    OPERATIONSPATH,
)


class AsynchPolicyAssignment():
    def __init__(self, filter_name_regex=None, filter_category=None, semaphore=10):
        load_dotenv()
        with change_dir(OPERATIONSPATH):
            self.config = ConfigParser()
            self.config.read(CONFVARIABLES)

        self.policy_assignments_create_api = self.config["AZURESDK"]["policy_assignments_create"]
        self.queue = asyncio.Queue()
        self.loop = asyncio.get_event_loop()
        self.semaphore = asyncio.BoundedSemaphore(semaphore)
        self.filter_name_regex = filter_name_regex
        self.filter_category_regex = filter_category
        self.queue_url = 'default'
        self.credential = 'default'

    def create_assignment_body(self, policy_definition):

        if type(policy_definition) is dict:
            policy_definition_json = policy_definition
        elif type(policy_definition) is str:
            policy_definition_json = json.loads(policy_definition)
        else:
            return None

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
                    try:
                        return json.dumps(policy_assignment_request_body, indent=4, ensure_ascii=False)
                    except:
                        pass

    async def get_subscription(self, session):
        """
        Method is here to test asynchronous behavior, subscriptions should appear in a different library
        """
        print('get_subscription...')
        assignment = await self.queue.get()
        subscription_id = assignment['subscription_id']

        api_endpoint = 'https://management.azure.com/subscriptions/{subscriptionId}?api-version=2020-01-01'.format(
            subscriptionId=subscription_id)
        # headers = headers = {b'Authorization': b'Bearer ' + auth_token.encode('ascii')}

        async with session.get(api_endpoint) as response:
            self.queue.task_done()
            return await response.json()

    async def create_policy_assignment(self, session):

        assignment = await self.queue.get()
        subscription_id = assignment['subscription_id']
        policyAssignmentName = assignment['policy_name']
        policyAssignmentBody = assignment['policy_assignment']

        api_endpoint = self.policy_assignments_create_api
        api_endpoint = api_endpoint.format(subscriptionId=subscription_id, policyAssignmentName=policyAssignmentName)
        headers = {'content-type': 'application/json'}

        async with session.put(url=api_endpoint, data=policyAssignmentBody) as response:
            self.queue.task_done()
            return await response.text()


    async def put_policy_assignment(self, session, auth_token):
        async with self.semaphore:
            assignment = await self.queue.get()
            subscription_id = assignment['subscription_id']
            policy_assignment_bodies = assignment['policy_assignment']

            for policy_assignment_body in policy_assignment_bodies:
                print(policy_assignment_body)

    async def main(self, *args):
        token = args[0]
        assignment_list = args[1]
        headers = {'Authorization': 'Bearer ' + token, 'content-type': 'application/json'}

        await self.queue_assignments(assignment_list)

        tasks = []

        async with aiohttp.ClientSession(headers=headers) as session:
            for i in range(self.queue.qsize()):
                tasks.append(self.create_policy_assignment(session))

            responses = await asyncio.gather(*tasks)
            await self.log_responses(responses)

    async def log_responses(self, responses):
        if self.credential == 'default' or self.queue_url == 'default':
            for response in responses:
                print(response)
            return
        else:
            async with QueueClient.from_queue_url(queue_url=self.queue_url, credential=self.credential) as async_storage_queue:
                for response in responses:
                    await async_storage_queue.send_message(str(response))


    async def queue_assignments(self, assignment_list: list):

        if self.filter_name_regex:
            p = re.compile(self.filter_name_regex)
        else:
            p = False
        if self.filter_category_regex:
            raise NotImplementedError

        for assignment in assignment_list[600:650]:
            if len(assignment['policy_definitions']) > 0:
                policy_definitions = assignment['policy_definitions']
                for policy_definition in policy_definitions:
                    policyDefinitionName = ''
                    if 'name' in policy_definition:
                        policyDefinitionName = policy_definition['name']
                        if self.filter_name_regex and not p.match(policyDefinitionName):
                            continue
                    else:
                        continue
                    policy_assignment_body = self.create_assignment_body(policy_definition)
                    if policy_assignment_body:
                        queue_assignment = dict()
                        queue_assignment['policy_assignment'] = policy_assignment_body
                        queue_assignment['subscription_id'] = assignment['subscription_id']
                        queue_assignment['policy_name'] = policyDefinitionName
                        self.queue.put_nowait(queue_assignment)
                    else:
                        continue

    def create_storage_logging(self, url, sas_token):
            self.queue_url = url
            self.credential = sas_token

    def batch_assignment(self, assignment_list):
        try:

            token_response = AzureSDKAuthentication().authenticate()
            token = token_response["accessToken"]
            try:
                self.loop.run_until_complete(self.main(token, assignment_list))

            except RuntimeError:
                print("Oops!")
            # result = react(self.main, [token])
            self.loop.close()
        except SystemExit:
            print("Ending loop")
