# -*- coding: utf-8 -*-
#
# (c) 2016 Boundless, http://boundlessgeo.com
# This code is licensed under the GPL 2.0 license.
#
from PyQt4 import QtGui, uic, QtCore
import os
from collections import defaultdict
import webbrowser


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
        self.resultsTree.customContextMenuRequested.connect(self.showPopupMenu)

        self.buttonBox.accepted.connect(self.okPressed)

    def showPopupMenu(self, point):
        item = self.resultsTree.selectedItems()[0]
        url = item.result.test.issueUrl
        if url:
            menu = QtGui.QMenu()
            action = QtGui.QAction("Open issue page", None)
            action.triggered.connect(lambda: webbrowser.open_new(url))
            menu.addAction(action)
            point = self.mapToGlobal(point)
            menu.exec_(point)


    def itemClicked(self):
        result= self.resultsTree.currentItem().result
        self.resultText.setText(str(result))

    def okPressed(self):
        self.close()

