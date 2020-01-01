from sqlalchemy import MetaData, Table, Column, Integer, String, Float

class AnalysisDb():
    def __init__(self, meta):
        self.meta = meta

    def noncompliant_table(self):
        noncompliant = Table(
            "noncompliant",
            self.meta,
            Column("id", Integer, primary_key=True),
            Column("resource_id", String),
            Column("management_group_ids", String),
            Column("policy_assignment_id", String),
            Column("policy_assignment_name", String),
            Column("policy_assignment_owner", String),
            Column("policy_assignment_parameters", String),
            Column("policy_assignment_scope", String),
            Column("policy_definition_action", String),
            Column("policy_definition_category", String),
            Column("policy_definition_id", String),
            Column("policy_definition_name", String),
            Column("policy_definition_reference_id", String),
            Column("policy_set_definition_category", String),
            Column("policy_set_definition_id", String),
            Column("policy_set_definition_name", String),
            Column("policy_set_definition_owner", String),
            Column("policy_set_definition_parameters", String),
            Column("resource_group", String),
            Column("resource_location", String),
            Column("resource_tags", String),
            Column("resource_type", String),
            Column("serialize", String),
            Column("subscription_id", String),
            Column("tenant_id", String),
            Column("subscription_display_name", String),
            Column("management_grp", String),
            Column("timestamp", String),
        )
        return noncompliant

    def factcompliance_table(self):
        factcompliance = Table(
            "factcompliance",
            self.meta,
            Column("id", Integer, primary_key=True),
            Column("resource_id", String),
            Column("subscription_id", String(36)),
            Column("tenant_id", String(36)),
            Column("policy_definition_name", String(36)),
            Column("policy_assignment_id", String),
            Column("policy_definition_id", String),
            Column("compliant", Integer),
            Column("noncompliant", Integer),
            Column("total_resources_measured", Integer),
            Column("percent_compliant", Float)

        )
        return factcompliance

    def policydefinitions_table(self):
        policydefinitions = Table(
            "policydefinitions",
            self.meta,
            Column("id", Integer, primary_key=True),
            Column("policy_definition_name", String(36)),
            Column("policy_display_name"),
        )
        return policydefinitions

    def subscription_table(self):
        subscriptions = Table(
            "subscriptions",
            self.meta,
            Column("id", Integer, primary_key=True),
            Column("tenant_id", String(36)),
            Column("subscription_id", String(36)),
            Column("management_grp", String(36)),
            Column("subscription_display_name", String),

        )
        return subscriptions
