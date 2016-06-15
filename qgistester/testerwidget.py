# -*- coding: utf-8 -*-
#
# (c) 2016 Boundless, http://boundlessgeo.com
# This code is licensed under the GPL 2.0 license.
#
import os
from PyQt4 import uic, QtGui, QtCore
from report import *
import traceback
import sys
from qgistester.reportdialog import ReportDialog
from utils import execute

WIDGET, BASE = uic.loadUiType(
    os.path.join(os.path.dirname(__file__), 'testerwidget.ui'))


class TesterWidget(BASE, WIDGET):

    currentTestResult = None
    currentTest = 0
    currentTestStep = 0

    BLINKING_INTERVAL = 1000

    buttonColors = ["", 'QPushButton {color: yellow;}']
                    #[QtGui.QPushButton().palette().color(QtGui.QPalette.Button),
                    #QtGui.QColor.fromRgb(200,200,0)]


    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.setupUi(self)
        self.setObjectName("TesterPluginPanel")
        self.btnCancel.clicked.connect(self.cancelTesting)
        self.btnTestOk.clicked.connect(self.testPasses)
        self.btnTestFailed.clicked.connect(self.testFails)
        self.btnSkip.clicked.connect(self.skipTest)
        self.btnNextStep.clicked.connect(self.runNextStep)
        self.buttons = [self.btnTestOk, self.btnTestFailed, self.btnNextStep]

        self.blinkTimer = QtCore.QTimer()
        self.blinkTimer.timeout.connect(self._blink)


    def startBlinking(self):
        self.currentBlinkingTime = 0
        self.blinkTimer.start(self.BLINKING_INTERVAL)

    def stopBlinking(self):
        self.blinkTimer.stop()
        for button in self.buttons:
            button.setStyleSheet(self.buttonColors[0])

    def _blink(self):
        self.currentBlinkingTime += 1
        color = self.buttonColors[self.currentBlinkingTime % 2]
        for button in self.buttons:
            if button.isEnabled():
                button.setStyleSheet(color)

    def setTests(self, tests):
        self.tests = tests

    def startTesting(self):
        self.currentTest = 0
        self.report = Report()
        self.runNextTest()

    def getReportDialog(self):
        """Wrapper for easy mocking"""
        self.reportDialog = ReportDialog(self.report)
        return self.reportDialog

    def runNextTest(self):
        if self.currentTestResult:
            self.report.addTestResult(self.currentTestResult)
        if self.currentTest < len(self.tests):
            test = self.tests[self.currentTest]
            self.labelCurrentTest.setText("Current test: %s-%s" % (test.group.upper(), test.name))
            self.currentTestResult = TestResult(test)
            self.currentTestStep = 0
            self.runNextStep()
        else:
            self.setVisible(False)
            dlg = self.getReportDialog()
            dlg.exec_()

    def runNextStep(self):
        self.stopBlinking()
        test = self.tests[self.currentTest]
        step = test.steps[self.currentTestStep]
        self.btnSkip.setEnabled(True)
        self.btnCancel.setEnabled(True)
        if os.path.exists(step.description):
            with open(step.description) as f:
                html = "".join(f.readlines())
            self.webView.setHtml(html, QtCore.QUrl.fromUserInput(step.description))
        else:
            if step.function is not None:
                self.webView.setHtml(step.description + "<p><b>[This is an automated step. Please, wait until it has been completed]</b></p>")
            else:
                self.webView.setHtml(step.description + "<p><b>[Click on the right-hand side buttons once you have performed this step]</b></p>")
        QtCore.QCoreApplication.processEvents()
        if self.currentTestStep == len(test.steps) - 1:
            if step.function is not None:
                self.btnTestOk.setEnabled(False)
                self.btnTestFailed.setEnabled(False)
                self.btnNextStep.setEnabled(False)
                self.btnSkip.setEnabled(False)
                self.btnCancel.setEnabled(False)
                self.webView.setEnabled(False)
                QtCore.QCoreApplication.processEvents()
                try:
                    execute(step.function)
                    self.testPasses()
                except:
                    self.testFails(traceback.format_exc())
            else:
                self.btnTestOk.setEnabled(True)
                self.btnTestOk.setText("Test passes")
                self.btnTestFailed.setEnabled(True)
                self.btnTestFailed.setText("Test fails")
                self.webView.setEnabled(True)
                self.btnNextStep.setEnabled(False)
                if step.prestep:
                    step.prestep()
        else:
            if step.function is not None:
                self.btnTestOk.setEnabled(False)
                self.btnTestFailed.setEnabled(False)
                self.btnNextStep.setEnabled(False)
                self.btnSkip.setEnabled(False)
                self.btnCancel.setEnabled(False)
                self.webView.setEnabled(False)
                QtCore.QCoreApplication.processEvents()
                try:
                    execute(step.function)
                    self.currentTestStep += 1
                    self.runNextStep()
                except:
                    self.testFails(traceback.format_exc())
            else:
                self.currentTestStep += 1
                self.webView.setEnabled(True)
                self.btnNextStep.setEnabled(not step.isVerifyStep)
                if step.isVerifyStep:
                    self.btnTestOk.setEnabled(True)
                    self.btnTestOk.setText("Step passes")
                    self.btnTestFailed.setEnabled(True)
                    self.btnTestFailed.setText("Step fails")
                else:
                    self.btnTestOk.setEnabled(False)
                    self.btnTestFailed.setEnabled(False)
                if step.prestep:
                    step.prestep()
        if step.function is None:
            self.startBlinking()

    def testPasses(self):
        test = self.tests[self.currentTest]
        if self.btnTestOk.isEnabled() and self.btnTestOk.text() == "Step passes":
            self.runNextStep()
        else:
            try:
                test = self.tests[self.currentTest]
                test.cleanup()
                self.currentTestResult.passed()
            except:
                self.currentTestResult.failed("Test cleanup", traceback.format_exc())

            self.currentTest +=1
            self.runNextTest()


    def testFails(self, msg = ""):
        test = self.tests[self.currentTest]
        if self.btnTestOk.isEnabled() and self.btnTestOk.text() == "Step passes":
            desc = test.steps[self.currentTestStep - 1].description
        else:
            desc = test.steps[self.currentTestStep].description
        self.currentTestResult.failed(desc, msg)
        try:
            test.cleanup()
        except:
            pass
        self.currentTest +=1
        self.runNextTest()

    def skipTest(self):
        try:
            test = self.tests[self.currentTest]
            test.cleanup()
        except:
            pass
        self.currentTest +=1
        self.currentTestResult.skipped()

        self.runNextTest()

    def cancelTesting(self):
        self.setVisible(False)
