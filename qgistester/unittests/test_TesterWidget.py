# -*- coding: utf-8 -*-
"""Test TesterWidget.py."""
#
# (c) 2016 Boundless, http://boundlessgeo.com
# This code is licensed under the GPL 2.0 license.
#
import unittest
import sys
import mock
import utilities
from qgistesting import start_app
from qgistesting.mocked import get_iface
from qgistester.test import UnitTestWrapper
from qgistester.testerwidget import TesterWidget
from qgistester.unittests.data.plugin1 import functionalTests, unitTests
from qgistester.report import Report, TestResult

__author__ = 'Alessandro Pasotti'
__date__ = 'April 2016'
__copyright__ = '(C) 2016 Boundless, http://boundlessgeo.com'


class TesterWidgetTests(unittest.TestCase):
    """Tests for the TesterWidget class that create and mange the tester
    interface to execute tester plugin tests."""

    @classmethod
    def setUpClass(cls):
        """Test setUp method."""
        cls.functionalTests = functionalTests()
        cls.unitTests = [UnitTestWrapper(unit) for unit in unitTests()]
        cls.allTests = cls.functionalTests + cls.unitTests
        cls.QGIS_APP = start_app()
        assert cls.QGIS_APP is not None
        cls.IFACE_Mock = get_iface()
        assert cls.IFACE_Mock is not None
        utilities.setUpEnv()

    @classmethod
    def tearDownClass(cls):
        """Test tearDown method."""
        utilities.cleanUpEnv()

    def __testInit(self):
        """check if __init__ is correctly executed."""
        self.assertTrue(False)

    def testSetTests(self):
        """check if tests list is set."""
        widget = TesterWidget()
        widget.setTests(self.allTests)
        self.assertEquals(widget.tests, self.allTests)

    def testStartTesting_UnitTests(self):
        """test the run of the first unit tests setting up the result."""
        widget = TesterWidget()
        widget.setTests(self.unitTests)
        widget.getReportDialog = mock.Mock()
        with mock.patch('qgistester.utils.iface', self.IFACE_Mock):
            widget.startTesting()
        self.assertEqual(widget.getReportDialog.call_count, 1)
        self.assertIsInstance(widget.report, Report)
        self.assertEqual(len(widget.report.results), 2)
        self.assertEqual(widget.report.results[0].status, TestResult.FAILED)
        self.assertEqual(widget.report.results[1].status, TestResult.PASSED)

    def testStartTesting_FunctionalTests(self):
        """test the run of the first functional tests setting up the result."""
        widget = TesterWidget()
        widget.setTests(self.functionalTests)
        widget.getReportDialog = mock.Mock()
        widget.startTesting()
        for t in widget.tests:
            for s in t.steps:
                widget.testPasses()
        self.assertEqual(widget.getReportDialog.call_count, 1)
        self.assertIsInstance(widget.report, Report)
        self.assertGreater(len(widget.report.results), 0)
        for r in widget.report.results:
            self.assertEqual(r.status, TestResult.PASSED)

    def testSkipTest(self):
        """test if test is skipped pressing stop test + relative cleanup."""
        widget = TesterWidget()
        widget.setTests(self.functionalTests)
        widget.getReportDialog = mock.Mock()
        widget.startTesting()
        for t in widget.tests:
            widget.skipTest()
        self.assertEqual(widget.getReportDialog.call_count, 1)
        self.assertIsInstance(widget.report, Report)
        self.assertGreater(len(widget.report.results), 0)
        for r in widget.report.results:
            self.assertEqual(r.status, TestResult.SKIPPED)

    def testCancelTesting(self):
        """test if a test set invisible."""
        widget = TesterWidget()
        widget.setVisible = mock.Mock()
        widget.cancelTesting()
        self.assertEqual(widget.setVisible.call_count, 1)


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
