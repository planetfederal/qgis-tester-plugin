# -*- coding: utf-8 -*-
#
# (c) 2016 Boundless, http://boundlessgeo.com
# This code is licensed under the GPL 2.0 license.
#
class Report():

    def __init__(self):
        self.results = []

    def addTestResult(self, result):
        self.results.append(result)


class TestResult():

    PASSED, FAILED, SKIPPED = range(3)
    def __init__(self, test):
        self.test = test
        self.state = self.SKIPPED
        self.errorStep = None
        self.errorMessage = None

    def failed(self, step, message):
        self.status = self.FAILED
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
        else:
            s+= "Test failed at step '%s' with message:\n%s" %(self.errorStep, self.errorMessage)
        return s