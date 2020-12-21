import unittest
import sys
sys.path.append("..")

class MyTestCase(unittest.TestCase):
    def test_model_selection(self):
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
