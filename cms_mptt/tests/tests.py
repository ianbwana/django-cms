import doctest
import unittest

from cms_mptt.tests import doctests
from cms_mptt.tests import testcases

def suite():
    s = unittest.TestSuite()
    s.addTest(doctest.DocTestSuite(doctests))
    s.addTest(unittest.defaultTestLoader.loadTestsFromModule(testcases))
    return s
