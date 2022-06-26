
# import FreeCAD modules
# import FreeCAD, FreeCADGui, WebGui

# Hermes modules
# from hermes.Resources.workbench.HermesNode import WebGuiNode
from ...workbench.HermesNode import WebGuiNode

# =============================================================================
# RunOsCommand
# =============================================================================
class RunOsCommand(WebGuiNode):
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
