from PyQt4 import QtGui, uic, QtCore
import os
from collections import defaultdict


WIDGET, BASE = uic.loadUiType(
    os.path.join(os.path.dirname(__file__), 'reportdialog.ui'))

class ReportDialog(BASE, WIDGET):

    resultColor = [QtCore.Qt.green, QtCore.Qt.red, QtCore.Qt.gray]
    def __init__(self, report):
        QtGui.QDialog.__init__(self)
            
        self.setupUi(self)
        self.resultsTree.clear()

        results = report.results

        allResults = defaultdict(list)
        for result in results:
            test = result.test
            allResults[test.group].append(result)

        for group, groupResults in allResults.iteritems():
            groupItem = QtGui.QTreeWidgetItem()
            groupItem.setText(0, group)
            for result in groupResults:
                resultItem = QtGui.QTreeWidgetItem()
                resultItem.result = result
                resultItem.setText(0, result.test.name)
                resultItem.setForeground(0, self.resultColor[result.status])
                groupItem.addChild(resultItem)
            self.resultsTree.addTopLevelItem(groupItem)

        self.resultsTree.expandAll()
        self.resultsTree.itemClicked.connect(self.itemClicked)

        self.buttonBox.accepted.connect(self.okPressed)

    def itemClicked(self):
        result= self.resultsTree.currentItem().result
        self.resultText.setText(str(result))

    def okPressed(self):
        self.close()

