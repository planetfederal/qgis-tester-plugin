# -*- coding: utf-8 -*-
"""Test tests sumbmodule with methods in __init__.py and packaging.py."""
#
# (c) 2016 Boundless, http://boundlessgeo.com
# This code is licensed under the GPL 2.0 license.
#
import unittest
import sys
import utilities

from qgistester.tests import findTests, addTestModule
from qgistester.tests.packaging import _loadSpatialite, \
                                       _openDBManager, \
                                       _openLogMessagesDialog


class StepTests(unittest.TestCase):
    """Tests for the Step class that describes a test step."""

    @classmethod
    def setUpClass(cls):
        """Test setUp method."""
        utilities.setUpEnv()

    @classmethod
    def tearDownClass(cls):
        """Test tearDown method."""
        utilities.cleanUpEnv()

    def test(self):
        """check ."""
        self.assertTrue(False)

    def testFindTests(self):
        """check findTests method to find all tests inside a plugin."""
        self.assertTrue(False)

    def testAddTestModule(self):
        """check addTestModule methiod to add a test in the qgistester
        plugin."""
        self.assertTrue(False)

    def testLoadSpatialite(self):
        """check _loadSpatialite method to check if provider is available."""
        self.assertTrue(False)

    def testOpenDBManager(self):
        """check if Db Manager is available."""
        self.assertTrue(False)

    def testOpenLogMessagesDialog(self):
        """check if LogMessageDialog is available."""
        self.assertTrue(False)


###############################################################################

def suiteSubset():
    """Setup a test suit for a subset of tests."""
    tests = ['testInit']
    suite = unittest.TestSuite(map(StepTests, tests))
    return suite


def suite():
    """Return test suite for all tests."""
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(StepTests, 'test'))
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
