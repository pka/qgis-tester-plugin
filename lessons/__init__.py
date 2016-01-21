# -*- coding: utf-8 -*-

from examplelessons import exporttogeojson

lessons = []

def addLessonModule(module):
    if "lesson" in dir(module):
        lessons.append(module.lesson)

addLessonModule(exporttogeojson)


def classFactory(iface):
    from plugin import LessonsPlugin
    return LessonsPlugin(iface)