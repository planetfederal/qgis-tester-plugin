# -*- coding: utf-8 -*-
"""Test utils.py."""
#
# (c) 2016 Boundless, http://boundlessgeo.com
# This code is licensed under the GPL 2.0 license.
#
import unittest
import sys
import utilities
import mock

__author__ = 'Luigi Pirelli'
__date__ = 'April 2016'
__copyright__ = '(C) 2016 Boundless, http://boundlessgeo.com'

class UtilsTests(unittest.TestCase):
    """Tests for the utility functions in utils.py."""

    @classmethod
    def setUpClass(cls):
        """Test setUp method."""
        utilities.setUpEnv()

    @classmethod
    def tearDownClass(cls):
        """Test tearDown method."""
        utilities.cleanUpEnv()

    def testLayerFromName(self):
        """check if giving a layer name it's instance is returned."""
        self.assertTrue(False)

    def testLoadLayer(self):
        """check load layer from file (raster or vector) returning layer
        instance."""
        self.assertTrue(False)

    def testLoadLayerNoCrsDialog(self):
        """load a layer file without opening CRS dialog."""
        self.assertTrue(False)

    def testExecutorThread(self):
        """Test wrapper to QThread to manage some vars and events."""
        self.assertTrue(False)

    def testExecute(self):
        """Test execution of long time task managing dialog to show progress."""
        self.assertTrue(False)


###############################################################################

def suiteSubset():
    """Setup a test suit for a subset of tests."""
    tests = ['testInit']
    suite = unittest.TestSuite(map(UtilsTests, tests))
    return suite


def suite():
    """Return test suite for all tests."""
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(UtilsTests, 'test'))
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
