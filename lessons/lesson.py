import os
from utils import openProject, unfoldMenu, menuFromName

class Step():

    MANUALSTEP, AUTOMATEDSTEP = range(2)

    def __init__(self, name, description, function=None, prestep=None, endsignal=None, endcheck=lambda:True, steptype=1):
        self.name = name
        self.description = description or ""
        self.function = function
        self.prestep = prestep
        self.endcheck = endcheck
        self.endsignal = endsignal
        self.steptype = steptype

import traceback

class Lesson():

    def __init__(self, name, group):
        self.folder = os.path.dirname(traceback.extract_stack()[-2][0])
        self.steps = []
        self.name = name
        self.group = group
        self.cleanup = lambda: None
        path = os.path.join(self.folder, "project.qgs")
        if os.path.exists(path):
            self.addStep("Open project", "Open project", lambda: openProject(path))


    def setCleanup(self,function):
        self.cleanup = function


    def addStep(self, name, description, function=None, prestep=None, endsignal=None, endcheck=lambda:True, steptype=1):
        if description is None:
            description = ""
        elif not os.path.exists(description):
            path = os.path.join(self.folder, description)
            if os.path.exists(path):
                description = path
        step = Step(name, description, function, prestep, endsignal, endcheck, steptype)
        self.steps.append(step)

    def addMenuClickStep(self, menuName):
        menu, action = menuFromName(menuName)
        name = "Click on '%s' menu item" % menuName
        self.addStep(name, name, None, lambda:unfoldMenu(menu, action), action.triggered, None, Step.MANUALSTEP)