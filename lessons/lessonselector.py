from PyQt4 import QtGui, uic
import os
from lessons import lessons
from collections import defaultdict

WIDGET, BASE = uic.loadUiType(
    os.path.join(os.path.dirname(__file__), 'lessonselector.ui'))

class LessonSelector(BASE, WIDGET):

    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.setupUi(self)

        self.lesson = None

        allLessons = defaultdict(list)
        for lesson in lessons:
            allLessons[lesson.group].append(lesson)

        for group, groupLessons in allLessons.iteritems():
            groupItem = QtGui.QTreeWidgetItem()
            groupItem.setText(0, group)
            for lesson in groupLessons:
                lessonItem = QtGui.QTreeWidgetItem()
                lessonItem.lesson = lesson
                lessonItem.setText(0, lesson.name)
                groupItem.addChild(lessonItem)
            self.lessonsTree.addTopLevelItem(groupItem)

        self.lessonsTree.expandAll()

        self.lessonsTree.currentItemChanged.connect(self.currentItemChanged)
        self.lessonsTree.itemDoubleClicked.connect(self.itemDoubleClicked)

        self.buttonBox.accepted.connect(self.okPressed)
        self.buttonBox.rejected.connect(self.cancelPressed)

        self.buttonBox.button(QtGui.QDialogButtonBox.Ok).setEnabled(False)

    def itemDoubleClicked(self, item, i):
        if hasattr(item, "lesson"):
            self.lesson = item.lesson
            self.close()

    def currentItemChanged(self):
        item = self.lessonsTree.currentItem()
        if item:
            self.buttonBox.button(QtGui.QDialogButtonBox.Ok).setEnabled(hasattr(item, "lesson"))

    def cancelPressed(self):
        self.close()

    def okPressed(self):
        self.lesson = self.lessonsTree.selectedItems()[0].lesson
        self.close()

