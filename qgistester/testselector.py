# -*- coding: utf-8 -*-
#
# (c) 2016 Boundless, http://boundlessgeo.com
# This code is licensed under the GPL 2.0 license.
#

import os
import tests
from collections import defaultdict
from test import UnitTestWrapper

from PyQt4 import uic
from PyQt4.QtCore import Qt, QSettings
from PyQt4.QtGui import QTreeWidgetItem, QDialog

from qgis.core import QgsApplication

WIDGET, BASE = uic.loadUiType(
    os.path.join(os.path.dirname(__file__), 'testselector.ui'))


class TestSelector(BASE, WIDGET):

    def __init__(self):
        super(TestSelector, self).__init__()
        self.setupUi(self)

        self.tests = None

        allTests = defaultdict(list)
        for test in tests.tests:
            allTests[test.group].append(test)

        for group, groupTests in allTests.iteritems():
            groupItem = QTreeWidgetItem()
            groupItem.setText(0, group)
            groupItem.setFlags(groupItem.flags() | Qt.ItemIsTristate);
            unitItem = QTreeWidgetItem()
            unitItem.setText(0, "Unit tests")
            unitItem.setFlags(unitItem.flags() | Qt.ItemIsTristate);
            manualItem = QTreeWidgetItem()
            manualItem.setText(0, "Manual tests")
            manualItem.setFlags(manualItem.flags() | Qt.ItemIsTristate);
            for test in groupTests:
                testItem = QTreeWidgetItem()
                testItem.setFlags(testItem.flags() | Qt.ItemIsUserCheckable);
                testItem.setCheckState(0, Qt.Checked);
                testItem.test = test
                testItem.setText(0, test.name)
                if isinstance(test, UnitTestWrapper):
                    unitItem.addChild(testItem)
                else:
                    manualItem.addChild(testItem)
            if manualItem.childCount():
                groupItem.addChild(manualItem)                
            if unitItem.childCount():
                groupItem.addChild(unitItem)
            self.testsTree.addTopLevelItem(groupItem)
            groupItem.setExpanded(True)

        self.buttonBox.accepted.connect(self.okPressed)
        self.buttonBox.rejected.connect(self.cancelPressed)

        self.selectAllLabel.linkActivated.connect(lambda: self.checkTests(lambda t: Qt.Checked))
        self.unselectAllLabel.linkActivated.connect(lambda: self.checkTests(lambda t: Qt.Unchecked))
        def _onlyManual(t):
            if isinstance(t, UnitTestWrapper):
                return Qt.Unchecked
            else:
                return Qt.Checked
        self.onlyManualLabel.linkActivated.connect(lambda: self.checkTests(_onlyManual))
        def _onlyUnit(t):
            if isinstance(t, UnitTestWrapper):
                return Qt.Checked
            else:
                return Qt.Unchecked
        self.onlyUnitLabel.linkActivated.connect(lambda: self.checkTests(_onlyUnit))


    def checkTests(self, condition):
        for i in xrange(self.testsTree.topLevelItemCount()):
            item = self.testsTree.topLevelItem(i)
            for j in xrange(item.childCount()):
                child = item.child(j)
                for k in xrange(child.childCount()):
                    subchild = child.child(k)
                    child.setCheckState(0, condition(subchild.test))

    def cancelPressed(self):
        self.saveSettings()
        self.close()

    def okPressed(self):
        self.tests = []
        for i in xrange(self.testsTree.topLevelItemCount()):
            groupItem = self.testsTree.topLevelItem(i)
            for j in xrange(groupItem.childCount()):
                subgroupItem = groupItem.child(j)
                for k in xrange(subgroupItem.childCount()):
                    testItem = subgroupItem.child(k)
                    if testItem.checkState(0) == Qt.Checked:
                        self.tests.append(testItem.test)
        self.close()
