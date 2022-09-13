
# import FreeCAD modules
import FreeCAD, FreeCADGui, WebGui

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

    def guiToExecute(self, obj):
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

    def executeToGui(self, obj, parameters):
        ''' import the "input_parameters" data into the json obj data '''

        method = parameters["Method"]
        if method in ["Commands list", "batchFile"]:
            setattr(obj, "ChooseMethod", method)
            # obj.ChooseMethod = parameters["Method"]

            # make read only the property that hasnt been choosen
            if method == "Commands list":
                obj.Commands = parameters["Command"]
                obj.setEditorMode("batchFile", 1)  # Make read-only
            elif method == "batchFile":
                obj.batchFile = parameters["Command"]
                obj.setEditorMode("Commands", 1)  # Make read-only
        else:
            FreeCAD.Console.printWarning(method + " is not Run Os Command options")
