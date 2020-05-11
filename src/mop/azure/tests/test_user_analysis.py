import unittest
from configparser import ConfigParser

from dotenv import load_dotenv

from mop.azure.utils.create_configuration import change_dir, OPERATIONSPATH, TESTVARIABLES
from mop.azure.analysis.baseline.graph.user_analysis import UserAnalysis


class TestUserAnalysis(unittest.TestCase):
    def setUp(self) -> None:
        load_dotenv()
        with change_dir(OPERATIONSPATH):
            self.config = ConfigParser()
            self.config.read(TESTVARIABLES)

    def test_list_users(self):
        ua = UserAnalysis()
        response = ua.find_user_type()

        self.assertTrue(response.status_code in range(200, 299))
        user_dictionary = response.json()
        users = user_dictionary['value']
        for user in users:
            if 'Guest' in user['userType']:
                print('{}, {}, {}'.format(user['displayName'], user['id'], user['userType']))


if __name__ == '__main__':
    unittest.main()
