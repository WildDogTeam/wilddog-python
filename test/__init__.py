import unittest

from .jsonutil_test import JSONTestCase
from .wilddog_test import WilddogTestCase


def all_tests():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(JSONTestCase))
    suite.addTest(unittest.makeSuite(WilddogTestCase))
    return suite
