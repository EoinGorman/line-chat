import unittest
import unittest.mock
import sys, os

sys.path.append(os.path.join(sys.path[0], '../',  '../', 'lib'))
import user_manager as um

class TestUserManager(unittest.TestCase):
    def test_add_user(self):
        self.assertEqual(1, 1, 'should be 1')

    def test_user_exists(self):
        return 1