
# import FreeCAD modules
# import FreeCAD, FreeCADGui, WebGui

# Hermes modules
# from hermes.Resources.workbench.HermesNode import WebGuiNode
from ....workbench.HermesNode import WebGuiNode

# =============================================================================
# CopyDirectory
# =============================================================================
class TurbulenceProperties(WebGuiNode):
    def __init__(self, obj, nodeId, nodeData, name):
        super().__init__(obj, nodeId, nodeData, name)

    # def jsonToJinja(self, obj):
    #     ''' convert the json data to "input_parameters" structure '''
    #     super().jsonToJinja(obj)
