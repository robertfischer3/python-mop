import datetime
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


    def print_response(self, arg):
        print(arg.json())

    async def get_subscription(self, auth_token):
        print('get_subscription...')
        subscription_id = await self.queue.get()

        api_endpoint = 'https://management.azure.com/subscriptions/{subscriptionId}?api-version=2020-01-01'.format(
            subscriptionId=subscription_id)
        headers = headers = {b'Authorization': b'Bearer ' + auth_token.encode('ascii')}

        res = await treq.get(api_endpoint, headers=headers)
        content = await res.json()

        print(content)
        self.queue.task_done()

    def main(self, reactor, *args):
            token = args[0]
            subscription_id = '82746ea2-9f97-4313-b44a-e9bde3a0a241'
            self.queue.put_nowait(subscription_id)
            return defer.ensureDeferred(self.get_subscription(token))

    def entry_point(self):
        try:

            token_response = AzureSDKAuthentication().authenticate()
            token = token_response["accessToken"]
            result = react(self.main, [token])

        except SystemExit:
            print("Ignoring twisted.internet.task.react sys.exit on completion.")
