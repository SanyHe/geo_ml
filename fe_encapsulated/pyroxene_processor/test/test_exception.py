import unittest
import pandas as pd
import sys
sys.path.append("..")
from exception import *

class MyTestCase(unittest.TestCase):
    def test_check_oxide(self):
        data = pd.read_excel("testing_pyroxene_data_failed.xlsx")
        self.assertRaises(Exception, check_oxide, data)

if __name__ == '__main__':
    unittest.main()


