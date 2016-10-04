# -*- coding: utf-8 -*-
#
# (c) 2016 Boundless, http://boundlessgeo.com
# This code is licensed under the GPL 2.0 license.
#
from unittest.suite import TestSuite
from unittest.result import TestResult
from unittest.runner import TextTestRunner
import traceback

class Step():

    def __init__(self, description, function=None, prestep=None,
                 isVerifyStep=False):
        self.description = description
        self.function = function
        self.prestep = prestep
        self.isVerifyStep = isVerifyStep


class Test():

    def __init__(self, name):
        self.steps = []
        self.name = name
        self.group = ""
        self.cleanup = lambda: None
        self.issueUrl = None
        self.settings = {}

    def __eq__(self, o):
        return o.name == self.name and o.group == self.group

    def addStep(self, description, function=None, prestep=None,
                isVerifyStep=False):
        self.steps.append(Step(description, function, prestep, isVerifyStep))

    def setCleanup(self, function):
        self.cleanup = function

    def setIssueUrl(self, url):
        self.issueUrl = url


class UnitTestWrapper(Test):

    def __init__(self, test):
        Test.__init__(self, test.shortDescription() or test.id())
        self.test = test
        self.steps.append(Step("Run unit test", self._runTest))

    def setCleanup(self):
        pass

    def _runTest(self):
        """method used to run a test."""
        suite = TestSuite()
        suite.addTest(self.test)
        runner = _TestRunner()
        result = runner.run(suite)
        if result.err is not None:
            desc = unicode(result.err) + "\n" + \
                   "".join(traceback.format_tb(result.err[2]))
            raise Exception(desc)


class _TestRunner(TextTestRunner):

    def __init__(self):
        pass

    def run(self, test):
        result = _TestResult()
        test(result)

        return result


class _TestResult(TestResult):

    def __init__(self):
        TestResult.__init__(self)
        self.err = None

    def addSuccess(self, test):
        pass

    def addError(self, test, err):
        self.err = err

    def addFailure(self, test, err):
        self.err = err
