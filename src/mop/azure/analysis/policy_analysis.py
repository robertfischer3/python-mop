from mop.azure.operations.policy_definitions import management_grp_policy_list, management_grp_policy_list_as_df
from mop.azure.operations.policy_insights import PolicyInsights
from mop.azure.resources.subscriptions import Subscriptions
from mop.azure.resources import subscriptions
from configparser import ConfigParser

from dotenv import load_dotenv
import pandas as pd

from azure.mgmt.policyinsights.models.query_failure_py3 import QueryFailureException
import os

import adal
import requests
from configparser import ConfigParser
from mop.azure.utils.manage_api import CONFVARIABLES, OPERATIONSPATH
from mop.azure.utils.manage_api import change_dir


class EvaluatePolicies:

    def __init__(self, credentials):

        load_dotenv()
        self.credentials = credentials
        self.subscriptions = None
        self.policy_insights = None

        with change_dir(OPERATIONSPATH):
            self.config = ConfigParser()
            self.config.read(CONFVARIABLES)

    def capture_subscriptions(self, management_grp, save_file=False, filename=""):
        '''
        Grab all the subscriptions associated with a management group
        :param management_grp:
        :return:
        '''
        if management_grp is None:
            raise ValueError

        subscriptions = Subscriptions(self.credentials).list_management_grp_subcriptions(
            management_grp=management_grp)
        df = pd.DataFrame(data=subscriptions,
                          columns=['subscription', 'tenant_id', 'subscription_name', 'managment_grp'])

        df.set_index('subscription', inplace=True)

        self.subscriptions = df

        if save_file:
            df.to_csv(filename)

    def capture_policy_insights_for_subscription(self, subscription):

        raw_policy_insights = PolicyInsights(self.credentials).policy_insights_client_query(
            subscription_id_param=subscription, policy_states='latest')
        mapped_policy_insights = PolicyInsights.mapped_columns_policy_insights(raw_policy_insights)

        df_mapped = pd.DataFrame(data=mapped_policy_insights, columns=PolicyInsights.get_row_names())

        return df_mapped

    def process_management_grp_subscriptions(self, management_grp):
        '''
        The method finds all the subscriptions in a management group and then returns all the subscriptions underneath
        The method then finds all the policy insights for each subscription and aggregates them
        :param management_grp:
        :return: pandas dataframe
        '''
        subscriptions = Subscriptions(self.credentials).list_management_grp_subcriptions(
            management_grp=management_grp)
        aggregate_df = None

        data_frame_list = list()

        for index, row in subscriptions.iterrows():
            try:
                df_policy_insights = self.capture_policy_insights_for_subscription(index)

                if not df_policy_insights.empty:
                    print(df_policy_insights.shape)
                    print(len(df_policy_insights.index))
                    data_frame_list.append(df_policy_insights)

            except QueryFailureException:
                print("Subscription off limits: ", index)

        if len(data_frame_list) > 0:
            tmp_dataframe = data_frame_list[0]
            for i in data_frame_list[1:]:
                aggregate_df = tmp_dataframe.append(i)
                tmp_dataframe = aggregate_df
        return aggregate_df

    def correlate_management_grp_data(self, management_grp, subscription):

        df_management_grp_insights = self.process_management_grp_subscriptions(management_grp)

        print(df_management_grp_insights.columns)

        policy_definitions = management_grp_policy_list_as_df(self.credentials,
                                                              management_grp=management_grp,
                                                              subscription_id_param=subscription)

        subscription_info = Subscriptions(self.credentials).list_management_grp_subcriptions(
            management_grp=management_grp)

        tmp_merge_step1 = pd.merge(df_management_grp_insights, policy_definitions, on='policy_definition_name', how='left')

        tmp_merge_step2 = pd.merge(tmp_merge_step1, subscription_info, on='subscription_id', how='left')

        df_management_grp_results = tmp_merge_step2

        return df_management_grp_results

