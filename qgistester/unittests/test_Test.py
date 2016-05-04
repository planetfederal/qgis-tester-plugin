# -*- coding: utf-8 -*-
"""Test test.py."""
#
# (c) 2016 Boundless, http://boundlessgeo.com
# This code is licensed under the GPL 2.0 license.
#
import unittest
import sys
import utilities
import mock
from qgistester.test import Step
from qgistester.test import Test
from qgistester.test import UnitTestWrapper
from qgistester.test import _TestRunner
from qgistester.test import _TestResult
from qgistester.unittests.data.plugin1 import unitTests

__author__ = 'Luigi Pirelli'
__date__ = 'April 2016'
__copyright__ = '(C) 2016 Boundless, http://boundlessgeo.com'


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

    def testInit(self):
        """check if __init__ is correctly executed."""
        def testFunction1():
            pass

        def testFunction2():
            pass

        description1 = "this is a step description"
        description2 = "this is a step description"
        preStep = Step(description1, testFunction1)
        # do test
        s2 = Step(description2, testFunction2, preStep, True)
        self.assertTrue(s2.description == description2)
        self.assertTrue(s2.function == testFunction2)
        self.assertTrue(s2.prestep == preStep)
        self.assertTrue(s2.isVerifyStep)


class TestTests(unittest.TestCase):
    """Tests for the Test class that define a TesterPlugin test."""

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
        name = "this is the test name"
        t = Test(name)
        self.assertEqual(len(t.steps), 0)
        self.assertEqual(t.name, name)
        self.assertEqual(t.group, '')
        self.assertIn('<function <lambda> at ', str(t.cleanup))
        self.assertIsNone(t.cleanup())
        self.assertIsNone(t.issueUrl)

    def testAddStep(self):
        """check if a test is correclty added."""
        def testFunction1():
            pass

        def testFunction2():
            pass

        description1 = "this is a step description"
        description2 = "this is a step description"
        preStep = Step(description1, testFunction1)
        t = Test('this is the test name')
        # do test
        t.addStep(description2, testFunction2, preStep, True)
        self.assertEqual(len(t.steps), 1)
        s = t.steps[0]
        self.assertTrue(s.description == description2)
        self.assertTrue(s.function == testFunction2)
        self.assertTrue(s.prestep == preStep)
        self.assertTrue(s.isVerifyStep)

    def testSetCleanup(self):
        """test the cleanup function is set."""
        def testFunction1():
            pass
        name = "this is the test name"
        t = Test(name)
        # do test
        t.setCleanup(testFunction1)
        self.assertEqual(t.cleanup, testFunction1)

    def testSetIssueUrl(self):
        """test the issue url is set."""
        issueUrl = 'http://www.example.com'
        name = "this is the test name"
        t = Test(name)
        # do test
        t.setIssueUrl(issueUrl)
        self.assertEqual(t.issueUrl, issueUrl)


class UnitTestWrapperTests(unittest.TestCase):
    """Tests for the UnitTestWrapper class that is a specialization of Test
    class."""

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
        # preconditions
        unitTest = unitTests()[0]
        # do test
        utw = UnitTestWrapper(unitTest)
        self.assertTrue(isinstance(utw, Test))
        self.assertEqual(utw.test, unitTest)
        self.assertEqual(len(utw.steps), 1)
        step = utw.steps[0]
        self.assertEqual(step.description, 'Run unit test')
        self.assertEqual(step.function, utw._runTest)

    def testSetCleanup(self):
        """check if cleanup is set (do nothing now => pass)."""
        pass

    def test_runTest(self):
        """check if _runTest is set."""
        # preconditions
        unitTest = unitTests()[0]
        utw = UnitTestWrapper(unitTest)
        # do test 1: _TestRunner.run return None
        resultMock = mock.Mock(spect=_TestResult)
        resultMock.err = None
        _TestRunnerMock = mock.Mock(spect=_TestRunner)
        _TestRunnerMock.run.return_value = resultMock
        with mock.patch('qgistester.test._TestRunner',
                        mock.Mock(return_value=_TestRunnerMock)):
            try:
                utw._runTest()
            except:
                # if exception then error
                self.assertTrue(False)
            self.assertIn('call.run', str(_TestRunnerMock.mock_calls[0]))

        # preconditions
        unitTest = unitTests()[0]
        utw = UnitTestWrapper(unitTest)
        # do test 2: _TestRunner.run return something
        err = []
        uknownContent = "I don't know the type of the first element"
        attrs = {'message': "this is the error message"}
        errMessage = type('errMessage', (object,), attrs)
        exc_type, exc_value, exc_traceback = sys.exc_info()

        err.append(uknownContent)
        err.append(errMessage)
        err.append(exc_traceback)

        resultMock = mock.Mock(spect=_TestResult)
        resultMock.err = err
        _TestRunnerMock = mock.Mock(spect=_TestRunner)
        _TestRunnerMock.run.return_value = resultMock
        with mock.patch('qgistester.test._TestRunner',
                        mock.Mock(return_value=_TestRunnerMock)):
            try:
                utw._runTest()
            except:
                pass
            else:
                # if NO exception then error
                self.assertTrue(False)
            self.assertIn('call.run', str(_TestRunnerMock.mock_calls[0]))


class _TestRunnerTests(unittest.TestCase):
    """Tests for the _TestRunner class that provides a TextTestRunner
    specialization overloading run method."""

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
        runner = _TestRunner()
        self.assertIsInstance(runner, unittest.runner.TextTestRunner)

    def testRun(self):
        """check if test is run setting result."""
        # preconditions
        unitTestMock = mock.Mock(spec=unittest.TestCase)
        runner = _TestRunner()
        # do test
        result = runner.run(unitTestMock)
        self.assertIsInstance(result, _TestResult)
        self.assertIn('call(<qgistester.test._TestResult run=0 errors=0 failures=0>)',
                      str(unitTestMock.mock_calls[0]))


class _TestResultTests(unittest.TestCase):
    """Tests for the _TestResult class that wraps test result."""

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
        runner = _TestResult()
        self.assertIsInstance(runner, unittest.result.TestResult)
        self.assertIsNone(runner.err)

    def testAddSuccess(self):
        """check if success state is added (do nothing => pass)."""
        pass

    def testAddError(self):
        """test the error state is added."""
        # preconditions
        unitTestMock = mock.Mock(spec=unittest.TestCase)
        errMock = mock.Mock()  # overengineered but I can't understand the type used for err
        tr = _TestResult()
        # do test
        tr.addError(unitTestMock, errMock)
        self.assertTrue(len(unitTestMock.mock_calls) == 0)
        self.assertEqual(tr.err, errMock)

    def testAddFailure(self):
        """test the failure state is added."""
        """This test is alamost similar to testAddError because the code to test
        is the same. Probably the differenziacion would be based on passed
        data."""
        # preconditions
        unitTestMock = mock.Mock(spec=unittest.TestCase)
        errMock = mock.Mock()  # overengineered but I can't understand the type used for err
        tr = _TestResult()
        # do test
        tr.addError(unitTestMock, errMock)
        self.assertTrue(len(unitTestMock.mock_calls) == 0)
        self.assertEqual(tr.err, errMock)


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
