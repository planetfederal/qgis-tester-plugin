def functionalTests():
    try:
        from qgistester.test import Test
    except:
        return []

    passingTest = Test('This test should pass')
    passingTest.addStep('Click on "Test passes"')

    skippedTest = Test('This test should be skiped')
    skippedTest.addStep('Click on "Skip test"')

    def failingFunction():
        assert False
    failingTest = Test('This test should fail')
    failingTest.addStep("Failing step", function=failingFunction)

    failingSetupTest = Test('This test should fail in the step setup')
    failingSetupTest.addStep("Failing prestep", prestep=failingFunction)

    def errorFunction():
        raise Exception ("Error in test")
    errorTest = Test('This test should error')
    errorTest.addStep("Error step", function=errorFunction)

    return [passingTest, skippedTest, failingTest, failingSetupTest, errorTest]