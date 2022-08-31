
# import FreeCAD modules
# import FreeCAD, FreeCADGui, WebGui

# Hermes modules
# from hermes.Resources.workbench.HermesNode import WebGuiNode
from ....workbench.HermesNode import WebGuiNode

# =============================================================================
# CopyDirectory
# =============================================================================
class TransportProperties(WebGuiNode):
    def __init__(self, obj, nodeId, nodeData, name):
        super().__init__(obj, nodeId, nodeData, name)

    # def guiToExecute(self, obj):
    #     ''' convert the json data to "input_parameters" structure '''
    #     super().guiToExecute(obj)

   # def executeToGui(self, obj, parameters):
   #      ''' import the "input_parameters" data into the json obj data '''
   #      super().executeToGui(obj)