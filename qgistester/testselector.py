from PyQt4 import QtGui, uic, QtCore
import os
import tests
from collections import defaultdict

WIDGET, BASE = uic.loadUiType(
    os.path.join(os.path.dirname(__file__), 'testselector.ui'))

class TestSelector(BASE, WIDGET):

    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.setupUi(self)

        self.tests = None

        allTests = defaultdict(list)
        for test in tests.tests:
            allTests[test.group].append(test)

        for group, groupTests in allTests.iteritems():
            groupItem = QtGui.QTreeWidgetItem()
            groupItem.setText(0, group)
            for test in groupTests:
                testItem = QtGui.QTreeWidgetItem()
                testItem.setFlags(testItem.flags() | QtCore.Qt.ItemIsUserCheckable);
                testItem.setCheckState(0, QtCore.Qt.Checked);
                testItem.test = test
                testItem.setText(0, test.name)
                groupItem.addChild(testItem)
            self.testsTree.addTopLevelItem(groupItem)

        self.testsTree.expandAll()

        self.selectAllLabel.linkActivated.connect(lambda: self.checkTests(True))
        self.unselectAllLabel.linkActivated.connect(lambda: self.checkTests(False))

        self.buttonBox.accepted.connect(self.okPressed)
        self.buttonBox.rejected.connect(self.cancelPressed)


    def checkTests(self, b):
        state = QtCore.Qt.Checked if b else QtCore.Qt.Unchecked
        for i in xrange(self.testsTree.topLevelItemCount()):
            item = self.testsTree.topLevelItem(i)
            for j in xrange(item.childCount()):
                child = item.child(j)
                child.setCheckState(0, state)

    def cancelPressed(self):
        self.close()

    def okPressed(self):
        self.tests = []
        for i in xrange(self.testsTree.topLevelItemCount()):
            groupItem = self.testsTree.topLevelItem(i)
            for j in xrange(groupItem.childCount()):
                testItem = groupItem.child(j)
                if testItem.checkState(0) == QtCore.Qt.Checked:
                    self.tests.append(testItem.test)
        self.close()

