from lessons.lesson import Lesson, Step
from lessons.utils import *
from qgis.utils import iface

def isLayerActive():
    layer = iface.activeLayer()
    return layer is not None and layer.name() == "points"

def setActiveLayer():
    layer = layerFromName("points")
    iface.setActiveLayer(layer)

lesson = Lesson("Export to geojson", "Basic lessons")
lesson.addStep("Set 'points' layer as active layer", "activelayer.html",
               function = setActiveLayer, endcheck = isLayerActive, steptype=Step.MANUALSTEP)
lesson.addMenuClickStep("Layer/Save As...")
lesson.addStep("Save the file as geojson", "saveas.html", steptype=Step.MANUALSTEP)