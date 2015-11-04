from unittest.suite import TestSuite
from unittest.result import TestResult
from unittest.runner import TextTestRunner

class Test():

    def __init__(self, name):
        self.steps = []
        self.name = name
        self.group = ""

    def addStep(self, name, function=None):
        self.steps.append((name, function))

class UnitTestWrapper():

    def __init__(self, test):
        self.steps = []
        self.test = test
        self.name = unicode(test)
        self.group = ""
        def runTest():
            suite = TestSuite()
            suite.addTest(self.test)
            runner = _TestRunner()
            result = runner.run(suite)
            if result.err is not None:
                raise Exception(result.err)
        self.steps.append(("Run unit test", runTest))

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

