# import FreeCAD modules
import FreeCAD, FreeCADGui, WebGui
if FreeCAD.GuiUp:
    import FreeCADGui
    from PySide import QtCore

    import PySide
    from PySide import QtGui, QtCore
    from PySide.QtGui import *
    from PySide.QtCore import *


# python modules
from PyQt5 import QtGui,QtCore
import json
import pydoc
import os
import sys
import copy

# Hermes modules
# from hermes.Resources.workbench.HermesNode import _WebGuiNode
from ..HermesNode import _WebGuiNode, _HermesNode
# from ... import HermesNode


# =============================================================================
# CopyDirectory
# =============================================================================
class CopyDirectory(_WebGuiNode):
    def __init__(self, obj, nodeId, nodeData, name):
        super().__init__(obj, nodeId, nodeData, name)

    def jsonToJinja(self, obj):
        ''' convert the json data to "input_parameters" structure '''

        parameters = dict()
        parameters["Source"] = obj.Source
        parameters["Target"] = obj.Target
        parameters["dirs_exist_ok"] = obj.dirs_exist_ok

        return parameters

# =============================================================================
# CopyFile
# =============================================================================
class CopyFile(_WebGuiNode):
    def __init__(self, obj, nodeId, nodeData, name):
        super().__init__(obj, nodeId, nodeData, name)

    def jsonToJinja(self, obj):
        ''' convert the json data to "input_parameters" structure '''

        parameters = dict()
        parameters["Source"] = obj.Source
        parameters["Target"] = obj.Target

        return parameters

# =============================================================================
# RunOsCommand
# =============================================================================
class RunOsCommand(_WebGuiNode):
    def __init__(self, obj, nodeId, nodeData, name):
        super().__init__(obj, nodeId, nodeData, name)

    def initializeFromJson(self, obj):
        '''
            Takes the properties from JSON and update its value
             at the FreeCAD object
        '''
        super().initializeFromJson(obj)

        # get the choosen methon
        method = getattr(obj, "ChooseMethod")

        # make read only the property that hasnt been choosen
        if method == "Commands list":
            obj.setEditorMode("batchFile", 1)  # Make read-only
        elif method == "batchFile":
            obj.setEditorMode("Commands", 1)  # Make read-only

    def jsonToJinja(self, obj):
        ''' convert the json data to "input_parameters" structure '''

        parameters = dict()
        parameters["Method"] = obj.ChooseMethod

        method = getattr(obj, "ChooseMethod")

        # take the choosen property to the input_parameters command
        if method == "Commands list":
            parameters["Command"] = obj.Commands
        elif method == "batchFile":
            parameters["Command"] = obj.batchFile

        return parameters

# =============================================================================
# RunPythonCode
# =============================================================================
class RunPythonCode(_WebGuiNode):
    def __init__(self, obj, nodeId, nodeData, name):
        super().__init__(obj, nodeId, nodeData, name)

    def jsonToJinja(self, obj):
        ''' convert the json data to "input_parameters" structure '''

        parameters = dict()
        parameters["ModulePath"] = obj.ModulePath
        parameters["ClassName"] = obj.ClassName
        parameters["MethodName"] = obj.MethodName
        if "formData" in self.nodeData["WebGui"]:
            parameters["Parameters"] = self.nodeData["WebGui"]["formData"]


        return parameters