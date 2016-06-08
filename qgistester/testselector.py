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
from PyQt4.QtCore import Qt
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
            for test in groupTests:
                testItem = QTreeWidgetItem()
                testItem.setFlags(testItem.flags() | Qt.ItemIsUserCheckable);
                testItem.setCheckState(0, Qt.Checked);
                testItem.test = test
                testItem.setText(0, test.name)
                groupItem.addChild(testItem)
            self.testsTree.addTopLevelItem(groupItem)

        self.filterUnitTests()

        self.selectAllLabel.linkActivated.connect(lambda: self.checkTests(True))
        self.unselectAllLabel.linkActivated.connect(lambda: self.checkTests(False))
        self.showUnitTestsCheck.stateChanged.connect(self.filterUnitTests)


    def filterUnitTests(self):
        hidden = not self.showUnitTestsCheck.isChecked()
        for i in xrange(self.testsTree.topLevelItemCount()):
            item = self.testsTree.topLevelItem(i)
            for j in xrange(item.childCount()):
                child = item.child(j)
                if isinstance(child.test, UnitTestWrapper):
                    child.setHidden(hidden)

    def checkTests(self, b):
        state = Qt.Checked if b else Qt.Unchecked
        for i in xrange(self.testsTree.topLevelItemCount()):
            item = self.testsTree.topLevelItem(i)
            for j in xrange(item.childCount()):
                child = item.child(j)
                child.setCheckState(0, state)

    def accept(self):
        self.tests = []
        for i in xrange(self.testsTree.topLevelItemCount()):
            groupItem = self.testsTree.topLevelItem(i)
            for j in xrange(groupItem.childCount()):
                testItem = groupItem.child(j)
                if testItem.checkState(0) == Qt.Checked and not testItem.isHidden():
                    self.tests.append(testItem.test)
        QDialog.accept(self)
