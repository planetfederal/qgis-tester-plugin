# -*- coding: utf-8 -*-
"""Test TestSelectpo.py."""
#
# (c) 2016 Boundless, http://boundlessgeo.com
# This code is licensed under the GPL 2.0 license.
#
import unittest
import sys
import utilities


class TestSelectorTests(unittest.TestCase):
    """Tests for the TestSelector widget that select the list of tests to
    execute."""

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
        self.assertTrue(False)

    def testCheckTests(self):
        """check if all tests are checked/unchecked dependin on previous
        state."""
        self.assertTrue(False)

    def testCancelPressed(self):
        """check the widget is closed."""
        self.assertTrue(False)

    def testOkPressed(self):
        """check the list of checked tests ar added to test suite."""
        self.assertTrue(False)


###############################################################################

def suiteSubset():
    """Setup a test suit for a subset of tests."""
    tests = ['testInit']
    suite = unittest.TestSuite(map(TestSelectorTests, tests))
    return suite


def suite():
    """Return test suite for all tests."""
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(TestSelectorTests, 'test'))
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
