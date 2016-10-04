# -*- coding: utf-8 -*-
#
# (c) 2016 Boundless, http://boundlessgeo.com
# This code is licensed under the GPL 2.0 license.
#

import os
from PyQt4 import uic, QtGui

WIDGET, BASE = uic.loadUiType(
    os.path.join(os.path.dirname(__file__), 'settingswindow.ui'))

class SettingsWindow(BASE, WIDGET):

    def __init__(self, settings):
        super(SettingsWindow, self).__init__()
        self.setupUi(self)
        self.settings = {}

        self.tableWidget.setRowCount(len(settings))
        for i, key in enumerate(settings):
            self.tableWidget.setItem(i, 0, QtGui.QTableWidgetItem(key))
            self.tableWidget.setItem(i, 1, QtGui.QTableWidgetItem(settings[key]))

        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.buttonBox.accepted.connect(self.okPressed)
        self.buttonBox.rejected.connect(self.cancelPressed)

    def okPressed(self):
        for i in xrange(self.tableWidget.rowCount()):
            self.settings[self.tableWidget.item(i, 0).text()] = self.tableWidget.item(i, 1).text()
        self.close()

    def cancelPressed(self):
        self.close()