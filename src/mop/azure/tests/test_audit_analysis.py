import unittest
from configparser import ConfigParser

from dotenv import load_dotenv

from mop.azure.utils.create_configuration import change_dir, OPERATIONSPATH, TESTVARIABLES
from mop.azure.analysis.baseline.graph.audit_analysis import AuditAnalysis


class TestAuditAnalysis(unittest.TestCase):
    def setUp(self) -> None:
        load_dotenv()
        with change_dir(OPERATIONSPATH):
            self.config = ConfigParser()
            self.config.read(TESTVARIABLES)

    def test_audit_list(self):
        audit_analysis = AuditAnalysis()
        audit_analysis.find_user_records()


if __name__ == '__main__':
    unittest.main()
