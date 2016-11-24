# -*- coding: utf-8 -*-
"""unittests for Report.py."""
from __future__ import absolute_import
from builtins import map
from builtins import str
#
# (c) 2016 Boundless, http://boundlessgeo.com
# This code is licensed under the GPL 2.0 license.
#
import unittest
import sys
import mock
from . import utilities
from qgistester.report import Report, TestResult
from qgistester.test import Test, UnitTestWrapper

__author__ = 'Alessandro Pasotti'
__date__ = 'April 2016'
__copyright__ = '(C) 2016 Boundless, http://boundlessgeo.com'


class ReportTests(unittest.TestCase):
    """Tests for the Report class that provides QGIS User interface to run
    tests."""

    @classmethod
    def setUpClass(cls):
        """Test setUp method."""
        utilities.setUpEnv()

    @classmethod
    def tearDownClass(cls):
        """Test tearDown method."""
        utilities.cleanUpEnv()

    def testInit(self):
        """check if __init__ is correctly executed."""
        r = Report()
        self.assertTrue(type(r.results) == list)
        self.assertTrue(len(r.results) == 0)

    def testAddTestResult(self):
        """test if a test is added in the results array."""
        r = Report()
        test = mock.Mock()
        tr = TestResult(test)
        r.addTestResult(tr)
        self.assertEqual(r.results[0], tr)
        self.assertTrue(len(r.results) == 1)


class TestResultTests(unittest.TestCase):
    """Tests for the TestResult class that provides QGIS User interface to run
    tests."""

    @classmethod
    def setUpClass(cls):
        """Test setUp method."""
        utilities.setUpEnv()

    @classmethod
    def tearDownClass(cls):
        """Test tearDown method."""
        utilities.cleanUpEnv()

    def testInit(self):
        """check if __init__ is correctly executed."""
        tr = TestResult('fake_test')
        self.assertEqual(tr.test, 'fake_test')
        self.assertEqual(tr.status, tr.SKIPPED)
        self.assertEqual(tr.errorStep, None)
        self.assertEqual(tr.errorMessage, None)


    def testFailed(self):
        """check if the fail flag is correctly set."""
        t = Test('Test that fail is set')
        t.addStep('Fail', lambda: False)
        tr = TestResult(t)
        tr.failed('fake_step', 'FAILED')
        self.assertEqual(tr.status, tr.FAILED)
        self.assertEqual(tr.errorStep, 'fake_step')
        self.assertEqual(tr.errorMessage, 'FAILED')

    def testPassed(self):
        """check if the passed is correctly set."""
        t = Test('Test that passed is set')
        t.addStep('Passed', lambda: False)
        tr = TestResult(t)
        tr.passed()
        self.assertEqual(tr.status, tr.PASSED)
        self.assertIsNone(tr.errorStep)
        self.assertIsNone(tr.errorMessage, 'PASSED')


    def testSkipped(self):
        """check if the skipped is correctly set."""
        t = Test('Test that skipped is set')
        t.addStep('Skipped', lambda: False)
        tr = TestResult(t)
        tr.skipped()
        self.assertEqual(tr.status, tr.SKIPPED)
        self.assertIsNone(tr.errorStep)
        self.assertIsNone(tr.errorMessage, 'PASSED')


    def test__str___(self):
        """test __str__  that convert a status in readamble string."""
        t = Test('Test that skipped is set')
        t.addStep('Skipped', lambda: False)
        tr = TestResult(t)
        self.assertEquals(u"%s" % tr, 'Test name: -Test that skipped is set\nTest result:Test skipped')



class TestRealRunner(unittest.TestCase):
    """Tests that TestResult is correctly populated after a real test run"""

    @classmethod
    def runner(cls, suite):
        test = list(suite)[0]
        utw = UnitTestWrapper(test)
        report = Report()
        result = TestResult(test)
        step = utw.steps[0]
        try:
            step.function()
            result.passed()
        except Exception as e:
            result.failed(test, str(e))
        report.addTestResult(result)
        return report.results[0]

    @classmethod
    def setUpClass(cls):
        """Test setUp method."""
        utilities.setUpEnv()

    @classmethod
    def tearDownClass(cls):
        """Test tearDown method."""
        utilities.cleanUpEnv()

    def testPassed(self):
        """Tests if a passed test correctly set PASSED in TestResult"""

        class TestPassed(unittest.TestCase):
            def testPassed(self):
                self.assertTrue(True)

        # Mimick the behaviour in testerwidget.py
        suite = unittest.makeSuite(TestPassed, 'test')
        result = self.runner(suite)
        self.assertEquals(result.status, result.PASSED)

    def testFailed(self):
        """Tests if a passed test correctly set FAILED in TestResult"""

        class TestFailed(unittest.TestCase):
            def testFailed(self):
                self.assertTrue(False)

        # Mimick the behaviour in testerwidget.py
        suite = unittest.makeSuite(TestFailed, 'test')
        result = self.runner(suite)
        self.assertEquals(result.status, result.FAILED)



###############################################################################

def suiteSubset():
    """Setup a test suit for a subset of tests."""
    tests = ['testInit']
    suite = unittest.TestSuite(list(map(ReportTests, tests)))
    return suite


def suite():
    """Return test suite for all tests."""
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(ReportTests, 'test'))
    suite.addTests(unittest.makeSuite(TestResultTests, 'test'))
    suite.addTests(unittest.makeSuite(TestRealRunner, 'test'))
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
