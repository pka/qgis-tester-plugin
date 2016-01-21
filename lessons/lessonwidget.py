import os
from PyQt4 import uic, QtGui, QtCore
from utils import execute
from lesson import Step

WIDGET, BASE = uic.loadUiType(
    os.path.join(os.path.dirname(__file__), 'lessonwidget.ui'))

class LessonWidget(BASE, WIDGET):

    lessonFinished = QtCore.pyqtSignal()

    def __init__(self, lesson):
        QtGui.QWidget.__init__(self)
        self.setupUi(self)
        self.lesson = lesson
        for step in lesson.steps:
            item = QtGui.QListWidgetItem(step.name)
            self.listSteps.addItem(item)
            item.setHidden(step.steptype == Step.AUTOMATEDSTEP)
        self.btnFinish.clicked.connect(self.finishLesson)
        self.btnMove.clicked.connect(self.stepFinished)
        self.btnRunStep.clicked.connect(self.runCurrentStepFunction)
        self.currentStep = 0
        self.moveToNextStep()


    def runCurrentStepFunction(self):
        QtCore.QCoreApplication.processEvents()
        step = self.lesson.steps[self.currentStep]
        self.webView.setEnabled(False)
        execute(step.function)
        self.webView.setEnabled(True)
        self.stepFinished()

    def stepFinished(self):
        step = self.lesson.steps[self.currentStep]
        if step.endcheck is not None and not step.endcheck():
            QtGui.QMessageBox.warning(self, "Lesson", "It seems that the previous step\nwas not correctly completed")
            return
        item = self.listSteps.item(self.currentStep)
        item.setBackground(QtCore.Qt.white)
        if step.endsignal is not None:
            step.endsignal.disconnect(self.stepFinished)
        self.currentStep += 1
        self.moveToNextStep()


    def moveToNextStep(self):
        if self.currentStep == len(self.lesson.steps):
            QtGui.QMessageBox.information(self, "Lesson", "You have reached the end of this lesson")
            self.finishLesson()
        else:
            step = self.lesson.steps[self.currentStep]
            if step.endsignal is not None:
                step.endsignal.connect(self.stepFinished)
            item = self.listSteps.item(self.currentStep)
            item.setBackground(QtCore.Qt.green)
            if os.path.exists(step.description):
                self.webView.setUrl(QtCore.QUrl(step.description))
            else:
                self.webView.setHtml(step.description)
            QtCore.QCoreApplication.processEvents()
            if step.prestep is not None:
                execute(step.prestep)
            if step.function is not None:
                self.btnRunStep.setEnabled(step.steptype != Step.AUTOMATEDSTEP)
                self.btnMove.setEnabled(step.steptype != Step.AUTOMATEDSTEP)
                if step.steptype == Step.AUTOMATEDSTEP:
                    self.runCurrentStepFunction()
            else:
                self.btnRunStep.setEnabled(False)
                self.btnMove.setEnabled(True)

    def finishLesson(self):
        self.setVisible(False)
        self.lessonFinished.emit()





