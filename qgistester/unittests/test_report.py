# -*- coding: utf-8 -*-
"""unittests for Report.py."""
#
# (c) 2016 Boundless, http://boundlessgeo.com
# This code is licensed under the GPL 2.0 license.
#
import unittest
import sys
from qgistester.unittests import utils


class ReportTests(unittest.TestCase):
    """Tests for the Report class that provides QGIS User itnerface to run
    tests."""

    @classmethod
    def setUpClass(cls):
        """Test setUp method."""
        utils.setUpEnv()

    @classmethod
    def tearDownClass(cls):
        """Test tearDown method."""
        utils.cleanUpEnv()

    def testInit(self):
        """check if __init__ is correctly executed."""
        self.assertTrue(False)

    def testAddTestResult(self):
        """test if a test is added in the results array."""
        self.assertTrue(False)

class TestResultTests(unittest.TestCase):
    """Tests for the TestResult class that provides QGIS User itnerface to run
    tests."""

    @classmethod
    def setUpClass(cls):
        """Test setUp method."""
        utils.setUpEnv()

    @classmethod
    def tearDownClass(cls):
        """Test tearDown method."""
        utils.cleanUpEnv()

    def testInit(self):
        """check if __init__ is correctly executed."""
        self.assertTrue(False)

    def testFailed(self):
        """check if the fail is correctly set."""
        self.assertTrue(False)

    def testPassed(self):
        """check if the passed is correctly set."""
        self.assertTrue(False)

    def testSkipped(self):
        """check if the skipped is correctly set."""
        self.assertTrue(False)

    def test__str___(self):
        """test __str__  that convert a status in readamble string."""
        self.assertTrue(False)


###############################################################################

def suiteSubset():
    """Setup a test suit for a subset of tests."""
    tests = ['testInit']
    suite = unittest.TestSuite(map(ReportTests, tests))
    return suite


def suite():
    """Return test suite for all tests."""
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(ReportTests, 'test'))
    suite.addTests(unittest.makeSuite(TestResultTests, 'test'))
    return suite


def run_all():
    """run all tests using unittest => no nose or testplugin."""
    # demo_test = unittest.TestLoader().loadTestsFromTestCase(CatalogTests)
    unittest.TextTestRunner(verbosity=3, stream=sys.stdout).run(suite())


def run_subset():
    """run a subset of tests using unittest > no nose or testplugin."""
    unittest.TextTestRunner(verbosity=3, stream=sys.stdout).run(suiteSubset())

if __name__ == "__main__":
    run_all()
