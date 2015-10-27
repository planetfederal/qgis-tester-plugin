class Report():

    results = []

    def addTestResult(self, result):
        self.results.append(result)


class TestResult():

    PASSED, FAILED, SKIPPED = range(3)
    def __init__(self):
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