# -*- coding: utf-8 -*-
#
# (c) 2016 Boundless, http://boundlessgeo.com
# This code is licensed under the GPL 2.0 license.
#

import os
import codecs
import webbrowser
from collections import defaultdict

from PyQt4 import uic
from PyQt4.QtCore import Qt, QSettings, QFileInfo
from PyQt4.QtGui import QTreeWidgetItem, QMenu, QAction, QFileDialog

from qgis.core import QgsApplication

WIDGET, BASE = uic.loadUiType(
    os.path.join(os.path.dirname(__file__), 'reportdialog.ui'))


class ReportDialog(BASE, WIDGET):

    resultColor = [Qt.green, Qt.red, Qt.gray]
    resultTag = ['PASSED', 'FAILED', 'SKIPPED']

    def __init__(self, report):
        super(ReportDialog, self).__init__()
        self.setupUi(self)

        self.actionSaveAll.setIcon(QgsApplication.getThemeIcon('/mActionFileSave.svg'))
        self.actionSaveSelected.setIcon(QgsApplication.getThemeIcon('/mActionFileSaveAs.svg'))
        self.actionOpenTracker.setIcon(QgsApplication.getThemeIcon('/mActionHelpAPI.png'))

        self.actionSaveAll.triggered.connect(lambda: self.saveResults(True))
        self.actionSaveSelected.triggered.connect(lambda: self.saveResults(False))

        self.resultsTree.clear()

        results = report.results

        allResults = defaultdict(list)
        for result in results:
            test = result.test
            allResults[test.group].append(result)

        for group, groupResults in allResults.iteritems():
            groupItem = QTreeWidgetItem()
            groupItem.setText(0, group)
            for result in groupResults:
                resultItem = QTreeWidgetItem()
                resultItem.result = result
                resultItem.setText(0, result.test.name)
                resultItem.setForeground(0, self.resultColor[result.status])
                groupItem.addChild(resultItem)
            self.resultsTree.addTopLevelItem(groupItem)

        self.resultsTree.expandAll()
        self.resultsTree.itemClicked.connect(self.itemClicked)
        self.resultsTree.customContextMenuRequested.connect(self.showPopupMenu)

    def showPopupMenu(self, point):
        item = self.resultsTree.selectedItems()[0]
        url = item.result.test.issueUrl
        if url:
            menu = QMenu()
            action = QAction('Open issue page', None)
            action.triggered.connect(lambda: webbrowser.open_new(url))
            menu.addAction(action)
            point = self.mapToGlobal(point)
            menu.exec_(point)

    def itemClicked(self):
        try:
            result= self.resultsTree.currentItem().result
        except:
            return
        self.resultText.setText(str(result))

    def saveResults(self, saveAll=False):
        settings = QSettings('Boundless', 'qgistester')
        lastDirectory = settings.value('lastDirectory', '.', unicode)
        fileName = QFileDialog.getSaveFileName(self,
                                               self.tr('Save file'),
                                               lastDirectory,
                                               self.tr('HTML files (*.html)'))
        if fileName == '':
            return

        if not fileName.lower().endswith('.html'):
            fileName += '.html'

        settings.setValue('lastDirectory', QFileInfo(fileName).absoluteDir().absolutePath())

        out = '<html><head>'
        out += '<meta http-equiv="Content-Type" content="text/html; charset=utf-8" /></head><body>'

        if saveAll:
            for i in xrange(self.resultsTree.topLevelItemCount()):
                groupItem = self.resultsTree.topLevelItem(i)
                out += '<h3>{}</h3>'.format(groupItem.text(0))
                out += '<ul>'
                for j in xrange(groupItem.childCount()):
                    results = groupItem.child(j).result
                    out += '<li>[{}] {}'.format(self.resultTag[results.status], results.test.name)
                    if results.status == results.FAILED:
                        out += '<p>Failed at step {} with message</p>'.format(results.errorStep)
                        out += '<code>{}</code>'.format(results.errorMessage)
                    out += '</li>'
                out += '</ul>'
        else:
            results = self.resultsTree.currentItem().result
            out += '<h3>{}</h3>'.format(results.test.group)
            out += '<ul>'
            out += '<li>[{}] {}'.format(self.resultTag[results.status], results.test.name)
            if results.status == results.FAILED:
                out += '<p>Failed at step {} with message</p>'.format(results.errorStep)
                out += '<code>{}</code>'.format(results.errorMessage)
            out += '</li></ul>'
        out += '</body></html>'

        with codecs.open(fileName, 'w', encoding='utf-8') as f:
            f.write(out)
