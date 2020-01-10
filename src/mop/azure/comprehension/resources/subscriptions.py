from configparser import ConfigParser

from azure.mgmt.subscription import SubscriptionClient
from azure.mgmt.subscription.operations import SubscriptionsOperations
from azure.mgmt.managementgroups import ManagementGroupsAPI
import pandas as pd
from azure.mgmt.resource.policy import PolicyClient
from azure.mgmt.resource.policy.models import PolicyAssignment

# TODO change refernce to latest
from azure.mgmt.resource.policy.v2018_03_01.models.error_response_py3 import (
    ErrorResponseException,
)
from dotenv import load_dotenv
import os

from mop.azure.connections import request_authenticated_session, Connections
from mop.azure.utils.create_configuration import change_dir, OPERATIONSPATH, CONFVARIABLES


class Subscriptions:
    def __init__(self):
        load_dotenv()
        self.credentials = Connections().get_authenticated_client()
        self.subscription_client = SubscriptionClient(self.credentials, base_url=None)

        with change_dir(OPERATIONSPATH):
            self.config = ConfigParser()
            self.config.read(CONFVARIABLES)

    def list_subscriptions(self):
        """

        :return:
        """
        subscriptions = self.subscription_client.subscription_operations.list()

        return subscriptions

    def get_subscription(self, subscription_id):

        subscription = self.subscription_client.subscriptions.get(subscription_id)
        return subscription

    def subscription_list_displayname_id(self):
        """
        Returns a list of subscriptions available to the credential
        :rtype: object
        :param creds:
        :return:
        """

        subscription_client = SubscriptionClient(self.credentials, base_url=None)
        subscription_list = [
            [subscription_item.display_name, subscription_item.subscription_id]
            for subscription_item in subscription_client.subscriptions.list()
        ]
        return subscription_list

    def get_subscription(self, subscription_id):
        """
        Gets detailed information on an individual subscription
        :rtype: object
        """
        subscription_client = SubscriptionClient(self.credentials, base_url=None)
        sub_info = subscription_client.subscriptions.get(
            subscription_id=subscription_id
        )
        return sub_info

    @staticmethod
    def limited_subscription_columns(
        cols=[
            "subscription_id",
            "tenant_id",
            "subscription_display_name",
            "management_grp",
        ]
    ):
        cols = cols
        return cols

    def list_management_grp_subcriptions(self, management_grp):
        """
        https://docs.microsoft.com/en-us/python/api/azure-mgmt-managementgroups/azure.mgmt.managementgroups.operations.entities_operations.entitiesoperations?view=azure-python
        :param management_grp:
        :return:
        """

        management_client = ManagementGroupsAPI(self.credentials)
        mngrp_subscriptions = management_client.entities.list(group_name=management_grp)

        """Here we want to only return subscriptions"""
        subscriptions_limited = [
            [
                subscriptions.name,
                subscriptions.tenant_id,
                subscriptions.display_name,
                management_grp,
            ]
            for subscriptions in mngrp_subscriptions
            if "/providers/Microsoft.Management/managementGroups"
               not in subscriptions.type
        ]
        df = pd.DataFrame(
            data=subscriptions_limited, columns=self.limited_subscription_columns()
        )
        df.set_index("subscription_id", inplace=True)

        return df

    def create_management_grp_policy_assignments(self, management_grp, subscription_id):
        """
        This method create a policies within a management group per subscription
        The subscription id in required to make a query against the Python SDK when querying a management group.
        Looking for alternatives.

        :param management_grp:
        :param subscription_id:
        :return:
        """

        with change_dir(OPERATIONSPATH):
            config = ConfigParser()
            config.read(CONFVARIABLES)


        management_client = ManagementGroupsAPI(self.credentials)
        mngrp_subscriptions = management_client.entities.list(group_name=management_grp)

        for subscription in mngrp_subscriptions:
            if (
                "/providers/Microsoft.Management/managementGroups"
                not in subscription.type
            ):

                policy_client = PolicyClient(
                    credentials=self.credentials,
                    subscription_id=subscription_id,
                    base_url=None,
                )
                policies = policy_client.policy_definitions.list_by_management_group(
                    management_grp
                )

                scope = "/subscriptions/{subscriptionId}".format(
                    subscriptionId=subscription.name
                )

                for policy in policies:
                    if (
                        not policy.metadata.get("category") is None
                        and policy.metadata.get("category") in config["FILTERS"]["policy_defition_category"]
                    ):

                        assignment = PolicyAssignment(
                            display_name=policy.display_name,
                            policy_definition_id=policy.id,
                            scope=scope,
                            parameters=None,
                            description=policy.description,
                        )

                        policy_assignment_name = "{}-assignment".format(
                            assignment.display_name
                        )
                        try:
                            result = policy_client.policy_assignments.create(
                                scope=scope,
                                policy_assignment_name=policy_assignment_name,
                                parameters=assignment,
                            )

                            if result:
                                print(
                                    "Subscription deployed: {}".format(
                                        subscription.name,
                                        policy_assignment_name,
                                        policy.display_name,
                                    )
                                )
                        except ErrorResponseException:
                            print(
                                "Subcription failed: {}".format(
                                    subscription.name,
                                    policy_assignment_name,
                                    policy.display_name,
                                )
                            )
