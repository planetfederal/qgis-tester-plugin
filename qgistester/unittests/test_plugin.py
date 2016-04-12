# -*- coding: utf-8 -*-
"""Test plugin.py."""
#
# (c) 2016 Boundless, http://boundlessgeo.com
# This code is licensed under the GPL 2.0 license.
#
import unittest
import sys
from qgistester.unittests import utils


class TesterTests(unittest.TestCase):
    """Tests for the TesterPlugin class that provides QGIS User itnerface to
    run tests."""

    @classmethod
    def setUpClass(cls):
        """Test setUp method."""
        utils.setUpEnv()

    @classmethod
    def tearDownClass(cls):
        """Test tearDown method."""
        utils.cleanUpEnv()

    def testInit(self):
        """check if plugin is loaded and present in qgis loaded plugins."""
        self.assertTrue(False)

    def testUnload(self):
        """check if plugin unload is correctly executed. If possibile chech no
        error are available in qgis log."""
        self.assertTrue(False)

    def testInitGui(self):
        """Check that the plugin is correctly loaded and set actiopns and
        buttons"""
        self.assertTrue(False)

    def testTest(self):
        ''' check test (would be better called run) method that add test dock
        to qgis
        '''
        self.assertTrue(False)


###############################################################################

def suiteSubset():
    tests = ['testInit']
    suite = unittest.TestSuite(map(TesterTests, tests))
    return suite

def suite():
    suite = unittest.makeSuite(TesterTests, 'test')
    return suite

# run all tests using unittest skipping nose or testplugin
def run_all():
    # demo_test = unittest.TestLoader().loadTestsFromTestCase(CatalogTests)
    unittest.TextTestRunner(verbosity=3, stream=sys.stdout).run(suite())

# run a subset of tests using unittest skipping nose or testplugin
def run_subset():
    unittest.TextTestRunner(verbosity=3, stream=sys.stdout).run(suiteSubset())

if __name__ == "__main__":
    run_all()
