from configparser import ConfigParser

from dotenv import load_dotenv

from mop.azure.comprehension.resource_management.py_policy_definitions.glbl_pr_sec_adls2_aadauth_scr import main as glbl_pr_sec_adls2_aadauth_scr
from mop.azure.comprehension.resource_management.py_policy_definitions.glbl_pr_sec_acr_buildfromsource_scr import main as glbl_pr_sec_acr_buildfromsource_scr
from mop.azure.comprehension.resource_management.py_policy_definitions.glbl_pr_sec_adf_credinkv_scr import main as glbl_pr_sec_adf_credinkv_scr
from mop.azure.comprehension.resource_management.py_policy_definitions.glbl_pr_sec_adlsgen1_ipfilter_scr import main as glbl_pr_sec_adlsgen1_ipfilter_scr
from mop.azure.comprehension.resource_management.py_policy_definitions.glbl_pr_sec_aps_mfa_scr import main as glbl_pr_sec_aps_mfa_scr
from mop.azure.comprehension.resource_management.py_policy_definitions.glbl_pr_sec_aps_waf_scr import main as glbl_pr_sec_aps_waf_scr
from mop.azure.comprehension.resource_management.py_policy_definitions.glbl_pr_sec_cbd_rbac_scr import main as glbl_pr_sec_cbd_rbac_scr
from mop.azure.comprehension.resource_management.py_policy_definitions.glbl_pr_sec_databricks_egressfilter_scr import main as glbl_pr_sec_databricks_egressfilter_scr
from mop.azure.comprehension.resource_management.py_policy_definitions.glbl_pr_sec_databricks_subnet_scr import main as glbl_pr_sec_databricks_subnet_scr
from mop.azure.comprehension.resource_management.py_policy_definitions.glbl_pr_sec_databricks_vnetinjection_scr import main as glbl_pr_sec_databricks_vnetinjection_scr
#from mop.azure.comprehension.resource_management.py_policy_definitions.glbl_pr_sec_dsvm_nsg_scr import main as glbl_pr_sec_dsvm_nsg_scr
from mop.azure.comprehension.resource_management.py_policy_definitions.glbl_pr_sec_kv_accesscontrol_scr import main as glbl_pr_sec_kv_accesscontrol_scr
from mop.azure.comprehension.resource_management.py_policy_definitions.glbl_pr_sec_kv_kvwebapp_scr import main as glbl_pr_sec_kv_kvwebapp_scr
from mop.azure.comprehension.resource_management.py_policy_definitions.glbl_pr_sec_kv_noprodenv_scr import main as glbl_pr_sec_kv_noprodenv_scr
#from mop.azure.comprehension.resource_management.py_policy_definitions.glbl_pr_sec_la_sas_scr import main as glbl_pr_sec_la_sas_scr
from mop.azure.comprehension.resource_management.py_policy_definitions.glbl_pr_sec_logicapp_adauth_scr import main as glbl_pr_sec_logicapp_adauth_scr
from mop.azure.comprehension.resource_management.py_policy_definitions.glbl_pr_sec_logicapp_securestring_scr import main as glbl_pr_sec_logicapp_securestring_scr
from mop.azure.comprehension.resource_management.py_policy_definitions.glbl_pr_sec_netapp_backupaudit_scr import main as glbl_pr_sec_netapp_backupaudit_scr
from mop.azure.comprehension.resource_management.py_policy_definitions.glbl_pr_sec_storage_aadauth_scr import main as glbl_pr_sec_storage_aadauth_scr
from mop.azure.comprehension.resource_management.py_policy_definitions.glbl_pr_sec_cdb_aadauth_scr import main as glbl_pr_sec_cdb_aadauth_scr
from mop.azure.comprehension.resource_management.py_policy_definitions.glbl_pr_sec_databricks_vnetfilter_scr import main as glbl_pr_sec_databricks_vnetfilter_scr


from mop.azure.utils.create_configuration import change_dir, OPERATIONSPATH, CONFVARIABLES


class PyPolicyRunner():
    def __init__(self):
        load_dotenv()
        with change_dir(OPERATIONSPATH):
            self.config = ConfigParser()
            self.config.read(CONFVARIABLES)

    def run(self, tenant_id, subscripiton_id, client_id, client_secret, customer_id, shared_key):

        glbl_pr_sec_adls2_aadauth_scr(tenant_id, subscripiton_id, client_id, client_secret, customer_id, shared_key, debug=True)
        #glbl_pr_sec_acr_buildfromsource_scr(tenant_id, subscripiton_id, client_id, client_secret, customer_id, shared_key, debug=True)
        glbl_pr_sec_adf_credinkv_scr(tenant_id, subscripiton_id, client_id, client_secret)
        glbl_pr_sec_adlsgen1_ipfilter_scr(tenant_id, subscripiton_id, client_id, client_secret, customer_id, shared_key, start_ip="203.145.180.59", end_ip="203.145.180.59", debug=True)
        glbl_pr_sec_aps_mfa_scr(tenant_id, subscripiton_id, client_id, client_secret)
        glbl_pr_sec_aps_waf_scr(tenant_id, subscripiton_id, client_id, client_secret)
        glbl_pr_sec_cbd_rbac_scr(tenant_id, subscripiton_id, client_id, client_secret)
        glbl_pr_sec_databricks_egressfilter_scr(tenant_id, subscripiton_id, client_id, client_secret, customer_id, shared_key, debug=True)
        glbl_pr_sec_databricks_subnet_scr(tenant_id, subscripiton_id, client_id, client_secret, customer_id, shared_key, debug=True)
        glbl_pr_sec_databricks_vnetinjection_scr(tenant_id, subscripiton_id, client_id, client_secret, customer_id, shared_key, debug=True)
        #glbl_pr_sec_dsvm_nsg_scr(tenant_id, subscripiton_id, client_id, client_secret, customer_id, shared_key, debug=True)
        glbl_pr_sec_kv_accesscontrol_scr(tenant_id, subscripiton_id, client_id, client_secret, customer_id, shared_key, debug=True)
        glbl_pr_sec_kv_kvwebapp_scr(tenant_id, subscripiton_id, client_id, client_secret)
        glbl_pr_sec_kv_noprodenv_scr(tenant_id, subscripiton_id, client_id, client_secret)
        #glbl_pr_sec_la_sas_scr(tenant_id, subscripiton_id, client_id, client_secret)
        glbl_pr_sec_logicapp_adauth_scr(tenant_id, subscripiton_id, client_id, client_secret, customer_id, shared_key, debug=True)
        glbl_pr_sec_logicapp_securestring_scr(tenant_id, subscripiton_id, client_id, client_secret, customer_id, shared_key, debug=True)
        glbl_pr_sec_netapp_backupaudit_scr(tenant_id, subscripiton_id, client_id, client_secret, customer_id, shared_key, debug=True)
        glbl_pr_sec_storage_aadauth_scr(tenant_id, subscripiton_id, client_id, client_secret, customer_id, shared_key, debug=True)
        glbl_pr_sec_cdb_aadauth_scr(tenant_id, subscripiton_id, client_id, client_secret, customer_id, shared_key, debug=True)
        glbl_pr_sec_databricks_vnetfilter_scr(tenant_id, subscripiton_id, client_id, client_secret, customer_id, shared_key, debug=True)
