# -*- coding: utf-8 -*-
"""Test test.py."""
#
# (c) 2016 Boundless, http://boundlessgeo.com
# This code is licensed under the GPL 2.0 license.
#
import unittest
import sys
from qgistester.unittests import utils


class StepTests(unittest.TestCase):
    """Tests for the Step class that describes a test step."""

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


class TestTests(unittest.TestCase):
    """Tests for the Test class that define a TesterPlugin test."""

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

    def testAddStep(self):
        """check if a test is correclty added."""
        self.assertTrue(False)

    def testSetCleanup(self):
        """test the cleanup function is set."""
        self.assertTrue(False)

    def testSetIssueUrl(self):
        """test the issue url is set."""
        self.assertTrue(False)


class UnitTestWrapperTests(unittest.TestCase):
    """Tests for the UnitTestWrapper class that is a specialization of Test
    class."""

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

    def testSetCleanup(self):
        """check if cleanup is set."""
        self.assertTrue(False)


class _TestRunnerTests(unittest.TestCase):
    """Tests for the _TestRunner class that provides a TextTestRunner
    specialization overloading run method."""

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

    def testRun(self):
        """check if rest is run setting resul."""
        self.assertTrue(False)


class _TestResultTests(unittest.TestCase):
    """Tests for the _TestResult class that wraps test result."""

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

    def testAddSuccess(self):
        """check if success state is added."""
        self.assertTrue(False)

    def testAddError(self):
        """test the error state is added."""
        self.assertTrue(False)

    def testAddFailure(self):
        """test the failure state is added."""
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
    suite.addTests(unittest.makeSuite(TestTests, 'test'))
    suite.addTests(unittest.makeSuite(UnitTestWrapperTests, 'test'))
    suite.addTests(unittest.makeSuite(_TestRunnerTests, 'test'))
    suite.addTests(unittest.makeSuite(_TestResultTests, 'test'))
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
