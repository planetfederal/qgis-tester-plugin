# -*- coding: utf-8 -*-
"""Test plugin.py."""
#
# (c) 2016 Boundless, http://boundlessgeo.com
# This code is licensed under the GPL 2.0 license.
#
import mock
from mock import call
import unittest
import sys
import utilities
from qgis.testing import start_app, stop_app
from qgis.testing.mocked import get_iface
import qgistester
from qgistester.plugin import TesterPlugin
from PyQt4 import QtGui, QtCore


class TesterTests(unittest.TestCase):
    """Tests for the TesterPlugin class that provides QGIS User itnerface to
    run tests."""

    @classmethod
    def setUpClass(cls):
        """Test setUp method."""
        utilities.setUpEnv()
        cls.QGIS_APP = start_app()
        assert cls.QGIS_APP is not None
        cls.IFACE_Mock = get_iface()
        assert cls.IFACE_Mock is not None

    @classmethod
    def tearDownClass(cls):
        """Test tearDown method."""
        utilities.cleanUpEnv()
        stop_app()

    def testInit(self):
        """check if plugin is loaded and present in qgis loaded plugins."""
        # create the instance to test
        self.IFACE_Mock.reset_mock()
        self.testerPlugin = TesterPlugin(self.IFACE_Mock)
        self.assertEqual(len(self.IFACE_Mock.mock_calls), 1)
        stringToFind = 'call.initializationCompleted.connect(<bound method TesterPlugin.hideWidget of <qgistester.plugin.TesterPlugin'
        self.assertIn(stringToFind, str(self.IFACE_Mock.mock_calls[0]))

        self.assertEqual(self.IFACE_Mock, self.testerPlugin.iface)
        self.assertEqual(self.testerPlugin.widget, None)

    def testHideWidget(self):
        """check if the widget is hided."""
        # precondition
        testerPlugin = TesterPlugin(self.IFACE_Mock)
        testerPlugin.widget = mock.Mock(spec=QtGui.QWidget)
        self.assertEqual(len(testerPlugin.widget.mock_calls), 0)
        # do test
        testerPlugin.hideWidget()
        self.assertEqual(len(testerPlugin.widget.mock_calls), 1)
        self.assertEqual('call.hide()',
                         str(testerPlugin.widget.mock_calls[0]))

    def testUnload(self):
        """check if plugin unload is correctly executed. That means, menu
        remove is called and deleted relative QAction."""
        # preconditions
        testerPlugin = TesterPlugin(self.IFACE_Mock)
        action = QtGui.QAction("Start testing", self.IFACE_Mock.mainWindow())
        testerPlugin.action = action
        # do test 1) widget is None
        self.IFACE_Mock.reset_mock()
        testerPlugin.unload()
        self.assertIn("call.removePluginMenu(u'Tester'",
                      str(self.IFACE_Mock.mock_calls[0]))
        self.assertNotIn('action', testerPlugin.__dict__)
        self.assertIn('widget', testerPlugin.__dict__)

        # preconditions
        testerPlugin = TesterPlugin(self.IFACE_Mock)
        action = QtGui.QAction("Start testing", self.IFACE_Mock.mainWindow())
        testerPlugin.action = action
        # do test 2) widget is available
        self.IFACE_Mock.reset_mock()
        testerPlugin.widget = mock.MagicMock(QtGui.QWidget)
        testerPlugin.unload()
        self.assertIn("call.removePluginMenu(u'Tester'",
                      str(self.IFACE_Mock.mock_calls[0]))
        self.assertNotIn('action', testerPlugin.__dict__)
        self.assertNotIn('widget', testerPlugin.__dict__)
        # I can not check if widget.hide has been called due to delete of
        # widget during unload

    def testInitGui(self):
        """Check that the plugin create the relative action and register
        self.test linked to the action."""
        # preconditions
        testerPlugin = TesterPlugin(self.IFACE_Mock)
        self.assertNotIn('action', testerPlugin.__dict__)
        # do test
        testerPlugin.iface.reset_mock
        testerPlugin.initGui()
        self.assertIsNotNone(testerPlugin.action)
        self.assertTrue(isinstance(testerPlugin.action, QtGui.QAction))
        self.assertTrue(testerPlugin.action.receivers(
                        QtCore.SIGNAL('triggered()')) == 1)
        self.assertIn("call.addPluginToMenu(u'Tester'",
                      str(testerPlugin.iface.mock_calls[3]))


    def testTest(self):
        ''' check test method:
        1) test if messageBox.warning is called
        2) open test selector widget
            2.1) cancel => do nothing
            2.2) ok =>
                2.2.1) Create TesterWidget and dock it
                2.2.2) load atests in it
                2.2.3) start running test
        '''
        # test 1)
        # preconditions
        qwidget = mock.Mock(spec=QtGui.QWidget)
        qwidget.isVisible.return_value = True
        testerPlugin = TesterPlugin(self.IFACE_Mock)
        testerPlugin.widget = qwidget
        # do test1
        # I only test that PyQt4.QtGui.QMessageBox.warning is called in
        # the above preconditions
        qmessageboxMock = mock.Mock(spec=QtGui.QMessageBox)
        with mock.patch('PyQt4.QtGui.QMessageBox', qmessageboxMock):
            testerPlugin.test()
        self.assertIn("call.warning", str(qmessageboxMock.mock_calls[0]))

        # test 2.1)
        # preconditions: TestSelector constructor mock return a mock simulating
        # a QDialog
        dlgMock = mock.Mock()
        dlgMock.tests = None
        testselectorMock = mock.Mock(spec=qgistester.testselector.TestSelector,
                                     return_value=dlgMock)
        testerPlugin = TesterPlugin(self.IFACE_Mock)
        testerPlugin.widget = None  # necessary to overpass first tested if
        # do test
        with mock.patch('qgistester.plugin.TestSelector', testselectorMock):
            testerPlugin.test()
        self.assertIsNone(testerPlugin.widget)

        # test 2.2 and 2.3
        # preconditions: TestSelector constructor mock return a mock simulating
        # a QDialog
        testselectorMock.reset_mock
        dlgMock.reset_mock
        dlgMock.tests = 'some tests'
        testerwidgetMock = mock.Mock(spec=qgistester.testerwidget.TesterWidget,
                                     return_value=dlgMock)
        testerPlugin = TesterPlugin(self.IFACE_Mock)
        testerPlugin.widget = None  # necessary to overpass first tested if
        # do test
        with mock.patch('qgistester.plugin.TestSelector', testselectorMock):
            with mock.patch('qgistester.plugin.TesterWidget',
                            testerwidgetMock):
                testerPlugin.test()
        self.assertIsNotNone(testerPlugin.widget)
        expected = [call.exec_(), call.exec_(), call.show(),
                    call.setTests('some tests'), call.startTesting()]
        self.assertEqual(dlgMock.mock_calls, expected)


###############################################################################

def suiteSubset():
    """Setup a test suit for a subset of tests."""
    tests = ['testInit']
    suite = unittest.TestSuite(map(TesterTests, tests))
    return suite


def suite():
    """Return test suite for all tests."""
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(TesterTests, 'test'))
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
