from report import TestResult
from unittest.suite import TestSuite

class Test():

    steps = []

    def __init__(self, group, name):
        self.name = name
        self.group = group

    def addStep(self, name, function=None):
        self.steps.append((name, function))

class UnitTestWrapper():

    steps = []

    def __init__(self, group, test):
        self.group = group
        self.test = test
        self.name = unicode(test)
        def runTest():
            suite = TestSuite()
            suite.addTest(self.test)
            runner = _TestRunner()
            result = runner.run(suite)
            if result.err is not None:
                raise Exception(result.err)
        self.steps.append(("Run unit test", runTest))

class _TestRunner():

    def __init__(self):
        pass

    def run(self, test):
        result = _TestResult(self)
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

