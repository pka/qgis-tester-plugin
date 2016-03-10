# -*- coding: utf-8 -*-
#
# (c) 2016 Boundless, http://boundlessgeo.com
# This code is licensed under the GPL 2.0 license.
#
from PyQt4 import QtGui, QtCore
from testerwidget import TesterWidget
from testselector import TestSelector

class TesterPlugin:

	def __init__(self, iface):
		self.iface = iface
		self.toolbar = None

	def unload(self):
		self.iface.removePluginMenu(u"Tester", self.action)
		del self.action
		if self.toolbar:
			self.toolbar.setVisible(False)
			del self.toolbar

	def initGui(self):
		self.action = QtGui.QAction("Start testing", self.iface.mainWindow())
		self.action.triggered.connect(self.test)
		self.iface.addPluginToMenu(u"Tester", self.action)


	def test(self):
		if self.toolbar is not None and self.toolbar.isVisible():
			QtGui.QMessageBox.warning(self.iface.mainWindow(), "Tester plugin", "A test cycle is currently being run")
			return 
		dlg = TestSelector()
		dlg.exec_()
		if dlg.tests:
			self.toolbar = QtGui.QToolBar("Tester", self.iface.mainWindow())
			self.toolbar.setAllowedAreas(QtCore.Qt.BottomToolBarArea)
			self.toolbar.setFloatable(False)
			self.toolbar.setMovable(False)
			self.iface.mainWindow().addToolBar(QtCore.Qt.BottomToolBarArea, self.toolbar)
			self.widget = TesterWidget(self.toolbar)
			self.widget.setMaximumHeight(100)
			self.toolbar.addWidget(self.widget)
			self.toolbar.setVisible(True)
			self.widget.setTests(dlg.tests)
			self.widget.startTesting()




