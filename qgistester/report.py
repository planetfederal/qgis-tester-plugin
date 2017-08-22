from builtins import range
from builtins import object
# -*- coding: utf-8 -*-
#
# (c) 2016 Boundless, http://boundlessgeo.com
# This code is licensed under the GPL 2.0 license.
#

class Report(object):

    def __init__(self):
        self.results = []

    def addTestResult(self, result):
        self.results.append(result)


class TestResult(object):

    PASSED, FAILED, SKIPPED, CONTAINS_ERROR, FAILED_AT_SETUP = list(range(5))

    def __init__(self, test):
        self.test = test
        self.status = self.SKIPPED
        self.errorStep = None
        self.errorMessage = None

    def failed(self, step, message):
        self.status = self.FAILED
        self.errorStep = step
        self.errorMessage = message

    def containsError(self, step, message):
        self.status = self.CONTAINS_ERROR
        self.errorStep = step
        self.errorMessage = message

    def setupFailed(self, step, message):
        self.status = self.FAILED_AT_SETUP
        self.errorStep = step
        self.errorMessage = message

    def passed(self):
        self.status = self.PASSED

    def skipped(self):
        self.status = self.SKIPPED

    def __str__(self):
        s = "Test name: %s-%s\nTest result:" % (self.test.group, self.test.name)
        if self.status == self.SKIPPED:
            s+= "Test skipped"
        elif self.status == self.PASSED:
            s+= "Test passed correctly"
        elif self.status == self.CONTAINS_ERROR:
            s+= "Test contains an error at step '%s':\n%s" %(self.errorStep, self.errorMessage)
        elif self.status == self.FAILED_AT_SETUP:
            s+= "Test step '%s' failed at setup:\n%s" %(self.errorStep, self.errorMessage)
        else:
            s+= "Test failed at step '%s' with message:\n%s" %(self.errorStep, self.errorMessage)
        return s
