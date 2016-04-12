# -*- coding: utf-8 -*-
#
# (c) 2016 Boundless, http://boundlessgeo.com
# This code is licensed under the GPL 2.0 license.
#
import unittest
import sys
from qgistester.unittests import utils


class ReportDialogTests(unittest.TestCase):
    """Tests for the Report class that provides QGIS User itnerface to run
    tests."""

    @classmethod
    def setUpClass(cls):
        """Test setUp method."""
        utils.setUpEnv()

    @classmethod
    def tearDownClass(cls):
        """Test tearDown method."""
        utils.cleanUpEnv()

    def testInit(self):
        """check if __init__ is correctly executed."""
        self.assertTrue(False)

    def testShowPopupMenu(self):
        """check if a menu popup is opened."""
        self.assertTrue(False)

    def testItemClicked(self):
        """test the resul tis set to the ckicked value."""
        self.assertTrue(False)

    def testOkPressed(self):
        """test the widget is closed."""
        self.assertTrue(False)


###############################################################################

def suiteSubset():
    """Setup a test suit for a subset of tests."""
    tests = ['testInit']
    suite = unittest.TestSuite(map(ReportDialogTests, tests))
    return suite


def suite():
    """Return test suite for all tests."""
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(ReportDialogTests, 'test'))
    return suite


def run_all():
    """run all tests using unittest => no nose or testplugin."""
    # demo_test = unittest.TestLoader().loadTestsFromTestCase(CatalogTests)
    unittest.TextTestRunner(verbosity=3, stream=sys.stdout).run(suite())


def run_subset():
    """run a subset of tests using unittest > no nose or testplugin."""
    unittest.TextTestRunner(verbosity=3, stream=sys.stdout).run(suiteSubset())
