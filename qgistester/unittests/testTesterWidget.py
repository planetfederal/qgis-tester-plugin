# -*- coding: utf-8 -*-
#
# (c) 2016 Boundless, http://boundlessgeo.com
# This code is licensed under the GPL 2.0 license.
#
import unittest
import sys
from qgistester.unittests import utils


class TesterWidgetTests(unittest.TestCase):
    """Tests for the TesterWidget class that create and mange the tester
    interface to execute tester plugin tests."""

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

    def testSetTests(self):
        """check if tests list is set."""
        self.assertTrue(False)

    def testStartTesting(self):
        """test the run of the fist test setting up the result."""
        self.assertTrue(False)

    def testRunNextTest(self):
        """test jump to the run of the next test."""
        self.assertTrue(False)

    def testRunNextStep(self):
        """test jump to the next step of a test."""
        self.assertTrue(False)

    def testTestPasses(self):
        """test if test step passed ckicking passes button + relative
        cleanup."""
        self.assertTrue(False)

    def testTestFails(self):
        """test if test step failed ckicking fail button + relative cleanup."""
        self.assertTrue(False)

    def testSkipTest(self):
        """test if test is kipped pressing skop test + relative cleanup."""
        self.assertTrue(False)

    def testCancelTesting(self):
        """test if a test set invisible."""
        self.assertTrue(False)


###############################################################################

def suiteSubset():
    """Setup a test suit for a subset of tests."""
    tests = ['testInit']
    suite = unittest.TestSuite(map(TesterWidgetTests, tests))
    return suite


def suite():
    """Return test suite for all tests."""
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(TesterWidgetTests, 'test'))
    return suite


def run_all():
    """run all tests using unittest => no nose or testplugin."""
    # demo_test = unittest.TestLoader().loadTestsFromTestCase(CatalogTests)
    unittest.TextTestRunner(verbosity=3, stream=sys.stdout).run(suite())


def run_subset():
    """run a subset of tests using unittest > no nose or testplugin."""
    unittest.TextTestRunner(verbosity=3, stream=sys.stdout).run(suiteSubset())
