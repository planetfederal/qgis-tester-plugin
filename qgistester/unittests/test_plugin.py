# -*- coding: utf-8 -*-
"""Test plugin.py."""
#
# (c) 2016 Boundless, http://boundlessgeo.com
# This code is licensed under the GPL 2.0 license.
#import qgis
import utilities
import unittest
import sys

from qgistester.plugin import TesterPlugin

class TesterTests(unittest.TestCase):
    """Tests for the TesterPlugin class that provides QGIS User itnerface to
    run tests."""

    @classmethod
    def setUpClass(cls):
        """Test setUp method."""
        utilities.setUpEnv()
        # create qgis application stub
        # do not need to call exitQgis()
        cls.QGIS_APP, cls.CANVAS, cls.IFACE, cls.PARENT = utilities.get_qgis_app()
        # create the instance to test
        cls.testerPlugin = TesterPlugin(cls.IFACE)

    @classmethod
    def tearDownClass(cls):
        """Test tearDown method."""
        utilities.cleanUpEnv()

    def testInit(self):
        """check if plugin is loaded and present in qgis loaded plugins."""
        self.assertEqual(self.IFACE, self.testerPlugin.iface)
        self.assertEqual(self.testerPlugin.widget, None)
        import ipdb; ipdb.set_trace()

        # check if p.iface.initializationCompleted has a new slot connected
        # this check can be done for SIP binded classes like all comes from
        # SIP binding. In that case I can't use QObject.receivers method

    def testHideWidget(self):
        """check if the widget is hided."""
        # precondition
        self.testerPlugin.widget = self.PARENT
        self.testerPlugin.widget.show()
        self.assertTrue(self.testerPlugin.widget.isVisible())
        # do test
        self.testerPlugin.hideWidget()
        self.assertFalse(self.testerPlugin.widget.isVisible())

    def testUnload(self):
        """check if plugin unload is correctly executed. If possibile chech no
        error are available in qgis log."""
        # preconditions
        action = QtGui.QAction("Start testing", self.IFACE.mainWindow())
        self.IFACE.addPluginToMenu(u"Tester", action)
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
