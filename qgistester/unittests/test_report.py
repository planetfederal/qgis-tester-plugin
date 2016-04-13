# -*- coding: utf-8 -*-
"""unittests for Report.py."""
#
# (c) 2016 Boundless, http://boundlessgeo.com
# This code is licensed under the GPL 2.0 license.
#
import unittest
import sys
import utilities
from qgistester.report import Report, TestResult
from qgistester.test import Test

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
        r.addTestResult('PASSED')
        self.assertEqual(r.results[0], 'PASSED')
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
        self.assertEqual(tr.state, tr.SKIPPED)
        self.assertEqual(tr.errorStep, None)
        self.assertEqual(tr.errorMessage, None)


    def testFailed(self):
        """check if the fail is correctly set."""
        t = Test('Test that fail is set')
        t.addStep('Fail', lambda: False)
        tr = TestResult(t)
        self.assertEqual(tr.status, t.FAILED)
        import ipdb; ipdb.set_trace()
        self.assertEqual(tr.errorStep, step)
        self.errorMessage = message

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
