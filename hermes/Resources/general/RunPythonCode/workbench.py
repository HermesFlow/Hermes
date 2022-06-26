
# import FreeCAD modules
# import FreeCAD, FreeCADGui, WebGui

# Hermes modules
# from hermes.Resources.workbench.HermesNode import WebGuiNode
from ...workbench.HermesNode import WebGuiNode

# =============================================================================
# RunPythonCode
# =============================================================================
class RunPythonCode(WebGuiNode):
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