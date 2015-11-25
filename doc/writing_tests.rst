Writing tests
=============

Instructions to write new tests are described in this document

To write a new set of tests, add a python module file in the *tests* folder of the plugin. The module must can have two functions, to define unit tests (automated) and functional tests (semi-automated):  *functionalTests()* and *unitTests()*. None of these functions is mandatory. The plugin will look for them and, if found, will call them to retrieve the tests decalred by the module.

Plugins can add their tests suite to this tester plugin by using the addTestModule() function.

In your plugin *__init__* method add something like this:

        try:
            from qgistester.tests import addTestModule
            addTestModule(testmodule, "Name_of_my_plugin")
        except:
            pass

Unit Tests
***********

Unit tests are created wrapping a python test suite. Create your test suite in the usual Python way and then return it from the *unitTests()* method

Functional Tests
*****************

Functional tests are defined using the *Test* class from the qgistester.test module. Here is an example of a test

vectorRenderingTest = Test("Verify rendering of uploaded style")
vectorRenderingTest.addStep("Preparing data", _openAndUpload)
vectorRenderingTest.addStep("Check that WMS layer is correctly rendered")
vectorRenderingTest.setCleanup(_clean)

To add a step to the test, the *addStep()* method is used. It accepts two parameters. The first one is mandatory and is a string with the description of the test. The second one is optional and should be a function. If this parameters is passed, the function will be executed at that step, and it will be an automated step. If no function is passed, the step will be considered a manual one. The description will be shown to the user and he will perform the step manually.

You can add a cleanup task to be performed when the test is finished (or skipped), by using the *setCleanup()* method and passing a function where the cleanup is to be performed.

See the *tests* folder to see the current tests and see how they are implemented.
