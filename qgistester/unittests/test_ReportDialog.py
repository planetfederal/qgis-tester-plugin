# -*- coding: utf-8 -*-
"""Test ReportDialog.py."""
#
# (c) 2016 Boundless, http://boundlessgeo.com
# This code is licensed under the GPL 2.0 license.
#
import unittest
import sys
import utilities
import mock
from qgis.testing import start_app
from qgis.testing.mocked import get_iface
from PyQt4 import QtCore, QtGui, QtTest
from qgistester.reportdialog import ReportDialog
from qgistester.report import Report, TestResult
from qgistester.unittests.data.plugin1 import functionalTests, unitTests
from qgistester.test import UnitTestWrapper

__author__ = 'Luigi Pirelli'
__date__ = 'April 2016'
__copyright__ = '(C) 2016 Boundless, http://boundlessgeo.com'


class ReportDialogTests(unittest.TestCase):
    """Tests for the Report class that provides QGIS User itnerface to run
    tests."""

    @classmethod
    def setUpClass(cls):
        """Test setUp method."""
        utilities.setUpEnv()
        # load sample tests
        cls.functionalTests = functionalTests()
        cls.unitTests = [UnitTestWrapper(unit) for unit in unitTests()]
        cls.allTests = cls.functionalTests + cls.unitTests
        # start qgis app stub
        cls.QGIS_APP = start_app()
        assert cls.QGIS_APP is not None
        cls.IFACE_Mock = get_iface()
        assert cls.IFACE_Mock is not None

    @classmethod
    def tearDownClass(cls):
        """Test tearDown method."""
        utilities.cleanUpEnv()

    def testInit(self):
        """check if __init__ is correctly executed."""
        # test1
        # preconditions
        r = Report()  # => r.results is empty
        # do test
        dlg = ReportDialog(r)  # dlg.resultsTree is a QTreeWidget
        expectedColorList = [QtCore.Qt.green, QtCore.Qt.red, QtCore.Qt.gray]
        self.assertTrue(dlg.resultColor == expectedColorList)
        self.assertTrue(dlg.resultsTree.topLevelItemCount() == 0)
        self.assertTrue(dlg.resultsTree.receivers(QtCore.SIGNAL('itemClicked(QTreeWidgetItem *, int)')) == 1)
        self.assertTrue(dlg.resultsTree.receivers(QtCore.SIGNAL('customContextMenuRequested(const QPoint &)')) == 1)
        self.assertTrue(dlg.buttonBox.receivers(QtCore.SIGNAL('accepted()')) == 1)

        # test2
        # preconditions: populate with tests results
        r = Report()
        for test in self.allTests:
            tr = TestResult(test)
            r.addTestResult(tr)
        # do test
        dlg = ReportDialog(r)  # dlg.resultsTree is a QTreeWidget
        self.assertTrue(dlg.resultsTree.topLevelItemCount() == 1)
        self.assertTrue(dlg.resultsTree.topLevelItem(0).isExpanded())
        self.assertTrue(dlg.resultsTree.topLevelItem(0).childCount() == 3)
        self.assertTrue(dlg.resultsTree.topLevelItem(0).child(0).text(0) ==
                        'Functional test')
        self.assertTrue(dlg.resultsTree.topLevelItem(0).child(1).text(0) ==
                        'Test that fails')
        self.assertTrue(dlg.resultsTree.topLevelItem(0).child(2).text(0) ==
                        'Test that passes')

    def testShowPopupMenu(self):
        """check if a menu popup is opened if issue url is present."""
        # test1
        # preconditions
        r = Report()
        for test in self.allTests:
            tr = TestResult(test)
            r.addTestResult(tr)
        dlg = ReportDialog(r)  # dlg.resultsTree is a QTreeWidget
        dlg.resultsTree.topLevelItem(0).child(1).setSelected(True)  # select 'Test that fails' that does NOT have url
        # do test
        point = QtCore.QPoint(0, 0)
        qmenuMock = mock.Mock(spec=QtGui.QMenu)
        qactionMock = mock.Mock(spec=QtGui.QAction)
        with mock.patch('PyQt4.QtGui.QMenu', qmenuMock):
            with mock.patch('PyQt4.QtGui.QAction', qactionMock):
                dlg.showPopupMenu(point)
        self.assertTrue(qmenuMock.mock_calls == [])
        self.assertTrue(qactionMock.mock_calls == [])

        # test2
        # preconditions
        r = Report()
        for test in self.allTests:
            tr = TestResult(test)
            r.addTestResult(tr)
        dlg = ReportDialog(r)  # dlg.resultsTree is a QTreeWidget
        dlg.resultsTree.topLevelItem(0).child(0).setSelected(True)  # select 'Functional tests' that does have url
        # do test
        point = QtCore.QPoint(0, 0)
        qmenuMock = mock.Mock(spec=QtGui.QMenu)
        qactionMock = mock.Mock(spec=QtGui.QAction)
        with mock.patch('PyQt4.QtGui.QMenu', qmenuMock):
            with mock.patch('PyQt4.QtGui.QAction', qactionMock):
                dlg.showPopupMenu(point)
        self.assertIn('call()', str(qmenuMock.mock_calls[0]))
        self.assertIn('call().addAction', str(qmenuMock.mock_calls[1]))
        self.assertIn('call().exec_(PyQt4.QtCore.QPoint())',
                      str(qmenuMock.mock_calls[2]))
        self.assertIn("call('Open issue page', None)",
                      str(qactionMock.mock_calls[0]))
        self.assertIn("call().triggered.connect",
                      str(qactionMock.mock_calls[1]))

    def testItemClicked(self):
        """test the result is set to the clicked value."""
        # preconditions
        r = Report()
        for test in self.allTests:
            tr = TestResult(test)
            r.addTestResult(tr)
        dlg = ReportDialog(r)  # dlg.resultsTree is a QTreeWidget
        # do test1
        self.assertTrue(dlg.resultText.toPlainText() == '')
        dlg.itemClicked()
        self.assertTrue(dlg.resultText.toPlainText() == '')
        # do test 2
        currentItem = dlg.resultsTree.topLevelItem(0).child(0)
        dlg.resultsTree.setCurrentItem(currentItem)
        dlg.itemClicked()
        self.assertIn('Test name: -Functional test',
                      dlg.resultText.toPlainText())
        self.assertIn('Test result:Test skipped', dlg.resultText.toPlainText())

    def testOkPressed(self):
        """test the widget is closed."""
        # preconditions
        r = Report()
        dlg = ReportDialog(r)  # dlg.resultsTree is a QTreeWidget
        dlg.show()
        # do test
        self.assertTrue(dlg.isVisible())
        dlg.okPressed()
        self.assertFalse(dlg.isVisible())


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

if __name__ == "__main__":
    run_all()
