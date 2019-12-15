import unittest

class Test:
    def __init__(self, *args, **kwargs):
        if kwargs.keys().__contains__('pluto'):
            print("Huh")
        print(kwargs)

    def output(self):
        print("stuff")

class MyTestCase(unittest.TestCase):
    def test_something(self):

        t = Test(sub='1234567', pluto='not a planet')
        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
