# -*- coding: utf-8 -*-
#
# (c) 2016 Boundless, http://boundlessgeo.com
# This code is licensed under the GPL 2.0 license.
#
import unittest
import sys
from qgistester.unittests.plugintests import suite as pluginTestsSuite
from qgistester.unittests.reportTests import suite as reportTestsSuite
from qgistester.unittests.testReportDialog import suite as \
                                           reportDialogTestsSuite
from qgistester.unittests.testTest import suite as testTestsSuite
from qgistester.unittests.testTesterWidget import suite as \
                                           testerWidgetTestsSuite
from qgistester.unittests.testTestSelector import suite as \
                                           testSelectorTestsSuite

# Tests for the QGIS Tester plugin. To know more see
# https://github.com/boundlessgeo/qgis-tester-plugin


def unitTests():
    """return array of test suites."""
    _tests = []
    _tests.extend(pluginTestsSuite())
    _tests.extend(reportTestsSuite())
    _tests.extend(reportDialogTestsSuite())
    _tests.extend(testTestsSuite())
    _tests.extend(testerWidgetTestsSuite())
    _tests.extend(testSelectorTestsSuite())
    return _tests


def runAllUnitTests():
    """run all unittests."""
    _suite = unittest.TestSuite()
    _suite.addTest(pluginTestsSuite())
    _suite.addTest(reportTestsSuite())
    _suite.addTest(reportDialogTestsSuite())
    _suite.addTest(testTestsSuite())
    _suite.addTest(testerWidgetTestsSuite())
    _suite.addTest(testSelectorTestsSuite())
    unittest.TextTestRunner(verbosity=3, stream=sys.stdout).run(_suite)
