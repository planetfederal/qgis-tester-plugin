# -*- coding: utf-8 -*-
"""Test TesterWidget.py."""
#
# (c) 2016 Boundless, http://boundlessgeo.com
# This code is licensed under the GPL 2.0 license.
#
import unittest
import sys
import os
import utilities
from PyQt4.QtTest import QTest
from PyQt4.QtGui import QApplication
from qgistester.testerwidget import TesterWidget
from qgistester.tests import findTests
from qgistester.report import Report, TestResult

class TesterWidgetTests(unittest.TestCase):
    """Tests for the TesterWidget class that create and mange the tester
    interface to execute tester plugin tests."""

    @classmethod
    def getWidget(cls):
        """Create and return a widget instance with tests loaded"""
        cls.widget = TesterWidget()
        cls.widget.setTests(cls.tests)
        return cls.widget

    @classmethod
    def setUpClass(cls):
        """Test setUp method."""
        cls.tests = findTests(path=[os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')], prefix='data.')
        cls.app = QApplication(sys.argv)
        # Not part of the unit tests, just makes sure that some tests exists
        assert(len(cls.tests) > 0)
        utilities.setUpEnv()

    @classmethod
    def tearDownClass(cls):
        """Test tearDown method."""
        utilities.cleanUpEnv()

    def testInit(self):
        """check if __init__ is correctly executed."""
        self.assertTrue(False)

    def testSetTests(self):
        """check if tests list is set."""
        self.assertEquals(self.getWidget().tests, self.tests)

    def testStartTesting(self):
        """test the run of the first test setting up the result."""
        widget = self.getWidget()
        widget.startTesting()
        self.assertTrue(isinstance(widget.report, Report))
        self.assertEqual(widget.report.results, [])

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

if __name__ == "__main__":
    run_all()
