# -*- coding: utf-8 -*-
"""Test tests sumbmodule with methods in __init__.py and packaging.py."""
from __future__ import absolute_import
from builtins import map
#
# (c) 2016 Boundless, http://boundlessgeo.com
# This code is licensed under the GPL 2.0 license.
#
import os
import unittest
import sys
import utilities
from qgistester.tests import findTests, addTestModule

__author__ = 'Alessandro Pasotti'
__date__ = 'April 2016'
__copyright__ = '(C) 2016 Boundless, http://boundlessgeo.com'


class StepTests(unittest.TestCase):
    """Tests for the Step class that describes a test step."""

    @classmethod
    def setUpClass(cls):
        """Test setUp method."""
        utilities.setUpEnv()

    @classmethod
    def tearDownClass(cls):
        """Test tearDown method."""
        utilities.cleanUpEnv()

    def testFindTests(self):
        """check findTests method to find all tests inside a plugin."""
        tests = findTests(path=[os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')], prefix='data.')
        test_names = [utw.name for utw in tests]
        self.assertIn('Test that fails', test_names)
        self.assertIn('Test that passes', test_names)
        self.assertIn('Functional test', test_names)


    def testAddTestModule(self):
        """check addTestModule method to add a test in the qgistester
        plugin."""
        from qgistester import tests
        if tests.tests is None:
            tests.tests = []
        from .data import plugin1
        addTestModule(plugin1, 'Plugin1')
        test_names = [utw.name for utw in tests.tests]
        self.assertIn('Test that fails', test_names)
        self.assertIn('Test that passes', test_names)
        self.assertIn('Functional test', test_names)


    # def testLoadSpatialite(self):
    #     """check _loadSpatialite method to check if provider is available."""
    #     self.assertTrue(False)
    #
    # def testOpenDBManager(self):
    #     """check if Db Manager is available."""
    #     self.assertTrue(False)
    #
    # def testOpenLogMessagesDialog(self):
    #     """check if LogMessageDialog is available."""
    #     self.assertTrue(False)


###############################################################################

def suiteSubset():
    """Setup a test suite for a subset of tests."""
    tests = ['testInit']
    suite = unittest.TestSuite(list(map(StepTests, tests)))
    return suite


def suite():
    """Return test suite for all tests."""
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(StepTests, 'test'))
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
