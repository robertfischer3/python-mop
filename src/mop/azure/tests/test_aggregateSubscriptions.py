from configparser import ConfigParser
from unittest import TestCase
import pandas as pd
from dotenv import load_dotenv
from mop.azure.analysis.baseline.aggregate_subscriptions import AggregateSubscriptions
from mop.azure.utils.create_configuration import change_dir, OPERATIONSPATH, CONFVARIABLES


class TestAggregateSubscriptions(TestCase):
    def setUp(self) -> None:
        load_dotenv()
        with change_dir(OPERATIONSPATH):
            self.config = ConfigParser()
            self.config.read(CONFVARIABLES)

    def test_get_managment_grp_subscriptions(self):
        management_grp = self.config['DEFAULT']['management_grp_id']
        aggregate_subscriptions = AggregateSubscriptions()
        results = aggregate_subscriptions.get_managment_grp_subscriptions(management_grp)
        aggregate_subscriptions.create_subscriptions(results)

    def test_aggregate_tags(self):
        aggregate_subcription_tags = AggregateSubscriptions()
        aggregate_subcription_tags.compile_tags()

    def test_update_subscription_owners(self):
        aggregate_subcription_tags = AggregateSubscriptions()
        aggregate_subcription_tags.identify_subscription_owners()
