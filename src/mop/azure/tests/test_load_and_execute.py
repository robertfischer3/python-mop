import unittest

from mop.azure.plugins.execution import Execution


class TestLoadAndExecute(unittest.TestCase):
    def test_something(self):
        execute = Execution()
        execute.run('plugin_python_policies')


if __name__ == '__main__':
    unittest.main()
