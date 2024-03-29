
# import FreeCAD modules
import FreeCAD, FreeCADGui, WebGui

# Hermes modules
# from hermes.Resources.workbench.HermesNode import WebGuiNode
from ...workbench.HermesNode import WebGuiNode

# =============================================================================
# CopyDirectory
# =============================================================================
class CopyDirectory(WebGuiNode):
    def __init__(self, obj, nodeId, nodeData, name):
        super().__init__(obj, nodeId, nodeData, name)

    def guiToExecute(self, obj):
        ''' convert the json data to "input_parameters" structure '''

        parameters = dict()
        parameters["Source"] = obj.Source
        parameters["Target"] = obj.Target
        parameters["dirs_exist_ok"] = obj.dirs_exist_ok

        return parameters

    def executeToGui(self, obj, parameters):
        ''' import the "input_parameters" data into the json obj data '''

        obj.Source = parameters["Source"]
        obj.Target = parameters["Target"]
        obj.dirs_exist_ok = parameters["dirs_exist_ok"]

