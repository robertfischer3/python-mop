import datetime
from asyncio import Queue

import aiohttp
import jmespath
import json
from codetiming import Timer
from configparser import ConfigParser
from dotenv import load_dotenv


import collections, json, os, sys, urllib.parse
import asyncio
from twisted import logger
from twisted.internet import task, defer
from twisted.protocols.tls import Protocol
import treq
import os
import queue

from twisted.internet.task import react

from mop.framework.azure_connections import AzureConnections, request_authenticated_azure_session, \
    AzureSDKAuthentication
from mop.azure.utils.create_configuration import (
    change_dir,
    CONFVARIABLES,
    OPERATIONSPATH,
)

class AsynchPolicyAssignment():
    def __init__(self, credentials=None):
        load_dotenv()
        with change_dir(OPERATIONSPATH):
            self.config = ConfigParser()
            self.config.read(CONFVARIABLES)

        self.policy_assignments_create = self.config["AZURESDK"]["policy_assignments_create"]
        self.queue = asyncio.Queue()
        self.loop = asyncio.get_event_loop()

    async def get_subscription(self, session, auth_token):
        print('get_subscription...')
        subscription_id = await self.queue.get()

        api_endpoint = 'https://management.azure.com/subscriptions/{subscriptionId}?api-version=2020-01-01'.format(
            subscriptionId=subscription_id)
        # headers = headers = {b'Authorization': b'Bearer ' + auth_token.encode('ascii')}

        async with session.get(api_endpoint) as response:
            self.queue.task_done()
            return await response.text()

    async def process_data(self, num: int, data: asyncio.Queue):
        processed = 0

        while processed < num:
            item = await data.get()


    async def main(self, *args):
        token = args[0]
        assignment_list = args[1]

        headers = {'Authorization': 'Bearer ' + token}

        for assignment in assignment_list:
            self.queue.put_nowait(assignment['subscription_id'])
        tasks = []
        async with aiohttp.ClientSession(headers=headers) as session:
            for i in range(self.queue.qsize()):
                tasks.append(self.get_subscription(session, token))

            responses = await asyncio.gather(*tasks)
            for response in responses:
                print(response)

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
            print("Ignoring twisted.internet.task.react sys.exit on completion.")
