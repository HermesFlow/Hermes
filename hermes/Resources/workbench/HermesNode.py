
# import FreeCAD modules
import FreeCAD,FreeCADGui, WebGui
if FreeCAD.GuiUp:
    import FreeCADGui
    from PySide import QtCore

    import PySide
    # from PySide import QtGui, QtCore
    # from PySide.QtGui import *
    # from PySide.QtCore import *


# python modules
from PyQt5 import QtGui,QtCore
import json
import pydoc
import os
import copy

# Hermes modules
import HermesTools
from HermesTools import addObjectProperty
import HermesGeometryDefinerNode
from HermesBlockMesh import HermesBlockMesh





def makeNode(name, workflowObj, nodeId, nodeData):
    """ Create a Hermes Node object """

    test = pydoc.locate('HermesNode._HermesNode')
    # test = pydoc.locate('HermesGui._HermesNode')

    if test is None:
        FreeCAD.Console.PrintMessage("Not found\n")

    # Object with option to have children
    obj = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroupPython", name)
    #print ("HermesNode make node\n")

    #    # Object can not have children
    #    obj = FreeCAD.ActiveDocument.addObject("App::FeaturePython", name)

    # add Nodeobj(obj) as child of workflowObj
    workflowObj.addObject(obj)

    # ----------------dynamic find class--------------------

    # find the class of the node from the its type
    #nodecls = pydoc.locate("HermesGui." + nodeData["Type"])
    nodecls = pydoc.locate("HermesNode." +'_'+ nodeData["Type"])


    #    # if the class is not exist, create a new class
    #    if nodecls is None:
    #        nodecls = pydoc.locate("HermesGui.%s" % nodeData["Type"])

    # call to the class
    if nodecls is not None:
        nodecls(obj, nodeId, nodeData, name)

        obj.Proxy.initializeFromJson(obj)

        if FreeCAD.GuiUp:
            _ViewProviderNode(obj.ViewObject)

        if obj.Label == "BC":
            obj.Proxy.updateBCNodeFields(workflowObj.CalculatedFields, obj)

    return obj

#**********************************************************************
class _CommandHermesNodeSelection:
    """ CFD physics selection command definition """

    def GetResources(self):
        # ResourceDir = FreeCAD.getResourceDir() if list(FreeCAD.getResourceDir())[-1] == '/' else FreeCAD.getResourceDir() + "/"
        # icon_path = ResourceDir + "Mod/Hermes/Resources/icons/NewNode.png"
        icon_path = os.path.join(FreeCAD.getResourceDir(),"Mod","Hermes","Resources","icons","NewNode.png")

        return {'Pixmap': icon_path,
                'MenuText': QtCore.QT_TRANSLATE_NOOP("Hermes_Node", "Hermes Node"),
                'ToolTip': QtCore.QT_TRANSLATE_NOOP("Hermes_Node", "Creates new Hermes Node")}

    def IsActive(self):
        return HermesTools.getActiveHermes() is not None

    def Activated(self):
        FreeCAD.ActiveDocument.openTransaction("Choose appropriate Node")
        isPresent = False
        members = HermesTools.getActiveHermes().Group
        for i in members:
            if isinstance(i.Proxy, _HermesNode):
                FreeCADGui.activeDocument().setEdit(i.Name)
                isPresent = True

        # Allow to re-create if deleted
        if not isPresent:
            FreeCADGui.doCommand("")
            FreeCADGui.addModule("HermesNode")
            FreeCADGui.addModule("HermesTools")
            FreeCADGui.doCommand(
                "HermesTools.getActiveHermes().addObject(HermesNode.makeNode())")
            FreeCADGui.ActiveDocument.setEdit(FreeCAD.ActiveDocument.ActiveObject.Name)



if FreeCAD.GuiUp:
    FreeCADGui.addCommand('Hermes_Node', _CommandHermesNodeSelection())

#**********************************************************************
class _SlotHandler:
    """ Slot Handler """

    def __init__(self):
        pass

    def process(self, data):
        FreeCAD.Console.PrintMessage("Process Data\n" + str(data))


# =============================================================================
# Hermes Node class
# =============================================================================
class _HermesNode(_SlotHandler):
    """ The Hermes Node """

    #    def __init__(self, obj, nodeId,nodeData):
    def __init__(self, obj, nodeId, nodeData, name):

        obj.Proxy = self
        self.nodeId = nodeId
        self.nodeData = nodeData
        self.name = name
        self.initProperties(obj)

    def initializeFromJson(self, obj):

        # get list of properties from nodeData
        NodeProperties = self.nodeData["Properties"]

        # update the current value of all properties in  node object
        for x in NodeProperties:
            # get property'num' object ; num =1,2,3 ...
            propertyNum = NodeProperties[x]

            # get the prop parameter
            prop = propertyNum["prop"]

            # get the prop current_val
            current_val = propertyNum["current_val"]

            # get the Type
            Type = propertyNum["type"]

            # in case of link obj, if not None, check if exist
            if (Type == "App::PropertyLink") and (current_val is not None):
                checkObj = FreeCAD.ActiveDocument.getObject(current_val)
                if checkObj is None:
                    # link remain none cause not exist
                    current_val = None
                    FreeCAD.Console.PrintWarning("The obj to link is not exist\n")

            # get the current_val at the prop
            setattr(obj, prop, current_val)

        # additional properties RunOsCommand node
        if self.name == "RunOsCommand":

            # get the choosen methon
            method = getattr(obj, "ChooseMethod")

            # make read only the property that hasnt been choosen
            if method == "Commands list":
                obj.setEditorMode("batchFile", 1)  # Make read-only
            elif method == "batchFile":
                obj.setEditorMode("Commands", 1)  # Make read-only


    def initProperties(self, obj):

        # ^^^ Constant properties ^^^

        # References property - keeping the faces and part data attached to the GE obj
        addObjectProperty(obj, 'References', [], "App::PropertyPythonObject", "", "Boundary faces")

        # Node Id
        # Todo- is necessary?
        addObjectProperty(obj, "NodeId", "-1", "App::PropertyString", "Node Id", "Id of node",
                          4)  # the '4' hide the property

        if self.name == "BlockMesh":
            # link part - link to 1 part - Inherite from parent BM
            addObjectProperty(obj, "partLink", None, "App::PropertyLink", "BasicData", "Link blockMesh node to part")

        # Type of the Object - (web/GE)
        addObjectProperty(obj, "Type", "-1", "App::PropertyString", "Node Type", "Type of node")
        obj.setEditorMode("Type", 1)  # Make read-only (2 = hidden)

        # Is Avtive property- Boolean -keep if obj has been activated (douuble clicked get active)
        addObjectProperty(obj, "IsActiveNode", False, "App::PropertyBool", "", "Active Node object in document")
        obj.setEditorMode("IsActiveNode", 1)  # Make read-only (2 = hidden)

        # link property - link to other object (beside parent)
        addObjectProperty(obj, "linkToOtherObjects", [], "App::PropertyLinkList", "Links", "Link to")

        # NodeDataString property - keep the json  node data as a string
        addObjectProperty(obj, "NodeDataString", "-1", "App::PropertyString", "NodeData", "Data of the node", 4)

        # Exportile property- get the directory path of where we want to export our files
        addObjectProperty(obj, "ExportNodeJSONFile", "", "App::PropertyPath", "IO", "Path to save Node JSON File")

        # RunWorkflow property - Run the workflow as a basic to luigi if change to true
        addObjectProperty(obj, "RunNodeWorkflow", False, "App::PropertyBool", "Run",
                          "Run the Node workflow as a basic to luigi")

        # RunLuigi property - Run luigi
        addObjectProperty(obj, "RunNodeLuigi", False, "App::PropertyBool", "Run", "Run Node luigi")

        # Update Values at the properties from nodeData
        obj.NodeId = self.nodeId
        nodeType = self.nodeData["Type"]
        obj.Type = nodeType
        obj.Label = self.name  # automatically created with object.
        obj.setEditorMode("Label", 1)  # Make read-only
        obj.NodeDataString = json.dumps(self.nodeData)  # convert from json to string

        # ^^^^^ Properties from Json  ^^^

        # get Web node List of properties
        ListProperties = self.nodeData["Properties"]

        # Create each property from the list
        for x in ListProperties:
            # get property'num' ; num =1,2,3 ...
            propertyNum = ListProperties[x]

            # get needed parameters to create a property
            prop = propertyNum["prop"]
            init_val = propertyNum["init_val"]
            Type = propertyNum["type"]
            Heading = propertyNum["Heading"]
            tooltip = propertyNum["tooltip"]

            # in case of link obj, if not None, check if exist
            if (Type == "App::PropertyLink") and (init_val is not None):
                checkObj = FreeCAD.ActiveDocument.getObject(init_val)
                if checkObj is None:
                    # create the property, without the link
                    init_val = None

                # add Object's Property
            addObjectProperty(obj, prop, init_val, Type, Heading, tooltip)

    def onDocumentRestored(self, obj):

        workflowObj = obj.getParentGroup()
        workflowObj.Proxy.nLastNodeId = "-1"

        # parse json data
        self.nodeData = json.loads(obj.NodeDataString)

        # when restored- initilaize properties
        self.initProperties(obj)

        FreeCAD.Console.PrintMessage("Node onDocumentRestored\n")

        if FreeCAD.GuiUp:
            _ViewProviderNode(obj.ViewObject)

    # just an example - not used
    def changeLabel(self):
        #        FreeCAD.Console.PrintMessage("\nChange Label\n")
        return

    def doubleClickedNode(self, obj):

        # get "workflowObj" from been parent of the node obj
        workflowObj = obj.getParentGroup()

        # backup last node and update "nLastNodeId" in Hermes workflow
        workflowObj.Proxy.updateLastNode(workflowObj, obj.NodeId)

        # update is active
        obj.IsActiveNode = True

        return

    def backupNodeData(self, obj):
        pass

    def UpdateNodePropertiesData(self, obj):
        # update the properties in the "nodeData"
        # use this func before exporting Json

        # get node List of properties
        ListProperties = self.nodeData["Properties"]

        for y in ListProperties:

            # get property'num' object ; num =1,2,3 ...
            propertyNum = ListProperties[y]

            # get the prop parameter
            prop = propertyNum["prop"]

            # get the Object Property current value from property object
            current_val = getattr(obj, prop)

            # update the value at the propertyNum[prop]
            if type(current_val) is not int and type(current_val) is not float and type(current_val) is not list:
                # In case of 'Quantity property' (velocity,length etc.), 'current_val' need to be export as a string
                propertyNum["current_val"] = str(current_val)

            else:
                propertyNum["current_val"] = current_val

            # update propertyNum in ListProperties
            ListProperties[y] = propertyNum

        # update ListProperties in nodeData
        self.nodeData["Properties"] = ListProperties

        # Update nodeData  at the NodeDataString by converting from json to string
        obj.NodeDataString = json.dumps(self.nodeData)

        return

    def RemoveNodeObj(self, obj):
        # remove NodeObj Children
        # use when importing new json file
        for child in obj.Group:
            obj.Document.removeObject(child.Name)

        return


# =============================================================================
#      "_ViewProviderNode" class
# =============================================================================
class _ViewProviderNode:
    """ A View Provider for the Hermes Node container object. """

    # =============================================================================
    #     General interface for all visual stuff in FreeCAD This class is used to
    #     generate and handle all around visualizing and presenting Node objects from
    #     the FreeCAD App layer to the user.
    # =============================================================================

    def __init__(self, vobj):
        vobj.Proxy = self
        self.NodeObjName = vobj.Object.Name
        self.NodeObjType = vobj.Object.Type

    def getIcon(self):
        # Define Resource dir end with ','
        ResourceDir = FreeCAD.getResourceDir() if list(FreeCAD.getResourceDir())[-1] == '/' else FreeCAD.getResourceDir() + "/"

        if self.NodeObjType == "WebGuiNode":
            icon_path = ResourceDir + "Mod/Hermes/Resources/icons/Web.png"
        elif self.NodeObjType == "GeometryDefinerNode":
            icon_path = ResourceDir + "Mod/Hermes/Resources/icons/GeometryDefiner.png"
        else:
            icon_path = ResourceDir + "Mod/Hermes/Resources/icons/NewNode.png"

        return icon_path

    def attach(self, vobj):
        self.ViewObject = vobj
        #        self.Object = vobj.Object
        self.bubbles = None

    def updateData(self, obj, prop):
        # We get here when the object of Node changes

        # Check if the JSONFile parameter changed and its not empty path
        # =============================================================================
        #         #not in use, just an example
        #         if (str(prop) == 'Label' and len(str(obj.Label)) > 0):
        #             obj.Proxy.changeLabel()
        #             return
        # =============================================================================

        if (str(prop) == 'ExportNodeJSONFile' and len(str(obj.ExportNodeJSONFile)) > 0):
            # get "workflowObj" from been parent of the node obj
            workflowObj = obj.getParentGroup()
            workflowObj.Proxy.prepareJsonVar(workflowObj, obj.Name)
            workflowObj.Proxy.saveJson(workflowObj, obj.ExportNodeJSONFile, obj.Label)
            obj.ExportNodeJSONFile = ''

        if (str(prop) == 'RunNodeWorkflow' and (obj.RunNodeWorkflow)):
            workflowObj = obj.getParentGroup()
            workflowObj.Proxy.prepareJsonVar(workflowObj, obj.Name)
            workflowObj.Proxy.RunworkflowCreation(workflowObj)

        if (str(prop) == 'RunNodeLuigi' and (obj.RunNodeLuigi)):
            workflowObj = obj.getParentGroup()
            workflowObj.Proxy.RunLuigiScript()

            # ----------------------------------------------------------------------------------

        # edit properties RunOsCommand node
        if str(prop) == "ChooseMethod" and obj.Name == "RunOsCommand":

            # get the choosen methon
            method = getattr(obj, "ChooseMethod")

            # make read only the property that hasnt been choosen, and read/write the one been choose
            if method == "Commands list":
                obj.setEditorMode("batchFile", 1)  # Make read-only
                obj.setEditorMode("Commands", 0)  # read/write


            elif method == "batchFile":
                obj.setEditorMode("Commands", 1)  # Make read-only
                obj.setEditorMode("batchFile", 0)  # read/write

                # ----------------------------------------------------------------------------------

        if obj.Label == 'BlockMesh':
            if prop == "partLink":

                # in case its initialized from Json stage, avoid overide data
                #
                if obj.Proxy.initBMflag and (not obj.Proxy.BMcount):
                    return

                print("viewProvider, updateData")
                #get the part object using prop
                partobj = getattr(obj, prop)

                # set the BlockMesh partlink  at each child
                for child in obj.Group:
                    setattr(child, prop, partobj)
                    setattr(child, "References", [])

                # also update part name in peoperties
                if partobj is None:
                    setattr(obj, "partName", "")
                else:
                    setattr(obj, "partName", partobj.Name)

                obj.Proxy.BMcount += 1

    #    def onChanged(self,obj, vobj, prop):
    def onChanged(self, vobj, prop):
        # not in use, just an example
        if (str(prop) == 'Label' and len(str(vobj.Label)) > 0):
            vobj.Proxy.changeLabel()
            return

    def doubleClicked(self, vobj):
        vobj.Object.Proxy.doubleClickedNode(vobj.Object)

    def __getstate__(self):

        # Create NodeObj using Object name
        NodeObj = FreeCAD.ActiveDocument.getObject(self.NodeObjName)

        # if node has been active - backup
        if NodeObj.IsActiveNode:
            NodeObj.Proxy.backupNodeData(NodeObj)

        # get the last updated NodeDataString
        getNodeString = NodeObj.NodeDataString

        # return an array with NodeObj name and the updated NodeDataString -
        # it will be recieved by "__setstate__" when opening the project
        return [self.NodeObjName, getNodeString]

    def __setstate__(self, state):

        #    #state - recieved from 'getstate', while saving the project "Hermesworkflow"
        #        type :array ,including 2 variebelles,
        #             state[0]= Name of the Node Object
        #             state[1]= nodeDataString - the last uppdated Json string before saving.

        NodeObjName = state[0]
        nodeDataString = state[1]

        # get Object using OBject name
        NodeObj = FreeCAD.ActiveDocument.getObject(NodeObjName)

        # update the nodeDataString at the NodeObj
        NodeObj.NodeDataString = nodeDataString

        return None


# =============================================================================
# #_WebGuiNode
# =============================================================================
class _WebGuiNode(_HermesNode):
    #    super().funcName(var1,var,2..) - allow to use the function of the Parent,
    #    and add current class functionalites

    def __init__(self, obj, nodeId, nodeData, name):
        super().__init__(obj, nodeId, nodeData, name)

    def doubleClickedNode(self, obj):
        super().doubleClickedNode(obj)

        self.selectNode(obj)

    def selectNode(self, obj):

        # get node WebGui- Scheme,uiScheme,FormData
        nodeWebGUI = self.nodeData["WebGui"]

        if obj.Label == "BC":
            self.updateBCPartList(obj)

        # Check if webGui is empty
        if not ((len(nodeWebGUI) == 0)):
            # define web address & pararmeters
            ResourceDir = FreeCAD.getResourceDir() if list(FreeCAD.getResourceDir())[-1] == '/' else FreeCAD.getResourceDir() + "/"
            path = ResourceDir + 'Mod/Hermes/Resources/jsonReactWebGui.html?parameters='
            address = 'file:///' + path

            # str JSON 'nodeWebGUI' using "dumps"
            parameters = json.dumps(nodeWebGUI)

            # open the jsonReact html page using the following command
            browser = WebGui.openSingleBrowser(address + parameters)
            sRegName = '0,' + self.name;
            browser.registerHandler(sRegName)

        return

    def process(self, data):

        UpdateWebGUI = data
        #        FreeCAD.Console.PrintMessage("WebGUI Process Data\n" + str(data))

        if (0 == len(UpdateWebGUI)):
            return

        # parse the 'UpdateWebGUI'
        UpdateWebGUIJson = json.loads(UpdateWebGUI)

        # update in our global json data the updated parsed 'WebGUI'
        # first update the node
        self.nodeData["WebGui"] = UpdateWebGUIJson

    #        formData=UpdateWebGUIJson["formData"]
    #        FreeCAD.Console.PrintMessage("----------------------------------------------------------------\n")
    #        FreeCAD.Console.PrintMessage("backup--nodedata.webgui['formData']="+str(formData)+"\n")

    def backupNodeData(self, obj):
        # backup the data of the last node pressed
        super().backupNodeData(obj)

        # then Update nodeData  at the NodeDataString by converting from json to string
        obj.NodeDataString = json.dumps(self.nodeData)

    def updateBCNodeFields(self, fieldList, obj):

        # take the WebGui part to a var
        nodeWebGUI = self.nodeData["WebGui"]
        currentBCList = list(nodeWebGUI["Schema"]["properties"].keys())

        # create list of items need to be added or removed from webGui
        add_list = [field for field in fieldList if field not in currentBCList]
        del_list = [field for field in currentBCList if field not in fieldList]
        del_list.remove("partName") # need to remain in dictionary

        # remove fields from webGui
        for field in del_list:
            nodeWebGUI["Schema"]["properties"].pop(field)

        # add fields to webGui
        for field in add_list:
            if len(field) > 0:

                # deep cp of template BCLisy to a new dict
                field_dict = copy.deepcopy(self.nodeData["BCList"])

                # update the data in structure
                field_dict["title"] = field
                field_dict["description"] = "Defined " + field + " Boundary condition for the part."

                # insert the the new dict into the webGui under ["Schema"]["properties"]
                nodeWebGUI["Schema"]["properties"][field] = field_dict

        # return data to the webGui node
        self.nodeData["WebGui"] = nodeWebGUI

    def updateBCPartList(self, obj):

        # get the active document
        doc = FreeCAD.ActiveDocument

        # get the part names from the active document
        partList = [obj.Label for obj in doc.Objects if obj.Module == "Part"]

        # FreeCAD.Console.PrintMessage("partList = " + str(partList) + "\n")

        # update the list in the webGui and description - depend if the list is empty or not
        if len(partList) == 0:
            self.nodeData["WebGui"]["Schema"]["properties"]["partName"]["description"] = "There are no parts in the FreeCAD document"
            self.nodeData["WebGui"]["Schema"]["properties"]["partName"]["enum"] = []
        else:
            self.nodeData["WebGui"]["Schema"]["properties"]["partName"]["description"] = "Defined Boundary condition for this part"
            self.nodeData["WebGui"]["Schema"]["properties"]["partName"]["enum"] = partList









# =============================================================================
# #_GeometryDefinerNode
# =============================================================================
class _GeometryDefinerNode(_HermesNode):
    #    super().funcName(var1,var,2..) - allow to use the function of the Parent,
    #    and add current class functionalites

    def __init__(self, obj, nodeId, nodeData, name):
        super().__init__(obj, nodeId, nodeData, name)

    def initializeFromJson(self, obj):
        super().initializeFromJson(obj)

        # get Geometry Face types section from json
        GeometryFaceTypes = self.nodeData["GeometryFaceTypes"]

        # get the list of available Geometry Face types
        TypeList = GeometryFaceTypes["TypeList"]

        # get the list of Geometry Entities that has been saved
        # GeometryEntityList = self.nodeData["GeometryEntityList"]
        # To make sure entities are not uploaded from json
        GeometryEntityList = []

        # Loop all the Geometry Entities that has been saved (GE = GeometryEntity )
        for y in GeometryEntityList:
            # get GE'num' object ; num =1,2,3 ...
            GEnum = GeometryEntityList[y]

            # get Name,Type and Properties of the GE
            GEName = GEnum["Name"]
            GEType = GEnum["Type"]

            # Create the GE node
            GENodeObj = HermesGeometryDefinerNode.makeEntityNode('GEtemp', TypeList, GEnum, obj)
            if GENodeObj is None:
                return None

            # get the GE properties, and update their current value
            GEProperties = GEnum["Properties"]
            GENodeObj.Proxy.setCurrentPropertyGE(GENodeObj, GEProperties)

            # Update the faces attach to the GE (also create the parts)
            GENodeObj.Proxy.initFacesFromJson(GENodeObj)

            # get GE Name and update his Label property
            GEName = GEnum["Name"]
            GENodeObj.Label = GEName

            # get GE type and update his Type property
            GEType = GEnum["Type"]
            GENodeObj.Type = GEType

    def doubleClickedNode(self, obj):
        super().doubleClickedNode(obj)

        # create CGEDialogPanel Object
        geDialog = HermesGeometryDefinerNode.CGEDialogPanel(obj)

        # get GEtypes section from json
        GETypes = self.nodeData["GeometryFaceTypes"]

        # get the list of available GE types from GEtypes section
        TypeList = GETypes["TypeList"]

        # add the GE types to options at GE dialog
        for types in TypeList:
            geDialog.addGE(types)

        # update the first value to be showen in the comboBox
        geDialog.setCurrentGE(types[0])

        # add node Object name to the geDialog name
        geDialog.setCallingObject(obj.Name)

        # show the Dialog in FreeCAD
        FreeCADGui.Control.showDialog(geDialog)

    def backupNodeData(self, obj):
        super().backupNodeData(obj)
        # Update faceList in GeometryEntityList section to each Geometry Entity node
        for child in obj.Group:
            child.Proxy.UpdateFacesInJson(child)

    def UpdateNodePropertiesData(self, obj):
        super().UpdateNodePropertiesData(obj)

        # in case amount of GE has been changed
        # Create basic structure of a GeometryEntityList (string) in the length of Children's obj amount
        # structure example:
        # -- "GeometryEntityList":{
        # --     "GE1":{ },
        # --     "GE2":{ },
        # --     "GE3":{ }
        # --  }
        x = 1
        GEListStr = "{"
        for child in obj.Group:
            if (x > 1):
                GEListStr += ','
            childStr = '"GE' + str(x) + '":{}'
            GEListStr += childStr
            x = x + 1
        GEListStr += "}"

        # convert structure from string to json
        GeometryEntityList = json.loads(GEListStr)

        # loop all GE(Geometry Entities) objects in Nodeobj
        x = 1
        for child in obj.Group:
            # update current properties value of the GE-child
            child.Proxy.UpdateGENodePropertiesData(child)

            # get GE-child nodeDate from EntityNodeDataString property
            GEnodeData = json.loads(child.EntityNodeDataString)

            # get GE'node' object ; node =1,2,3 ...
            GEnode = 'GE' + str(x)

            # update the GE-child nodeDate in the Geometry Entity List section
            GeometryEntityList[GEnode] = GEnodeData

            x = x + 1

        # update the Geometry Entity List section data in nodeData
        self.nodeData['GeometryEntityList'] = GeometryEntityList

        # Update nodeData  at the NodeDataString by converting from json to string
        obj.NodeDataString = json.dumps(self.nodeData)

        # # update properties of the current node(before updated only the children)
        # super().UpdateNodePropertiesData(obj)

        # workflowObj = obj.getParentGroup()
        # if "BlockMesh" in workflowObj.Proxy.JsonObject["workflow"]["nodes"]:
        #     # update block mesh with its vertices and boundry
        #     HermesBlockMesh().updateJson(obj)


    def geDialogClosed(self, obj, GEtype, GEname):
        # call when created new GE node

        # Create basic structure of a GENodeData
        GENodeData = {
            "Name": "",
            "Type": "",
            "Properties": {}
        }

        # get the GE Type available from Json, and their list of properties
        GETypes = self.nodeData["GeometryFaceTypes"]
        TypeList = GETypes["TypeList"]
        TypeProperties = GETypes["TypeProperties"]

        # take the properties of the choosen GEtype from dialog
        GEJsonType = TypeProperties[GEtype]
        GEProperties = GEJsonType["Properties"]

        # update values in GENodeData structure
        GENodeData["Name"] = GEname  # meaningful name is thr type
        GENodeData["Type"] = GEtype
        GENodeData["Properties"] = GEProperties

        # Create the GEObject
        GENodeObj = HermesGeometryDefinerNode.makeEntityNode('GEtemp', TypeList, GENodeData, obj)
        if GENodeObj is None:
            return None

        # get the References from the parent node to the the new GE child
        GENodeObj.References = obj.References
        GENodeObj.Proxy.geDialogClosed(GENodeObj, GEtype, GEname)


        # Empty the parent node References for further use
        obj.References = []

        return

# =============================================================================
# #_CommandGeometryDefinerSelection
# =============================================================================
class _CommandGeometryDefinerSelection:
    """ Geometry Definer selection command definition """

    def GetResources(self):
        ResourceDir = FreeCAD.getResourceDir() if list(FreeCAD.getResourceDir())[-1] == '/' else FreeCAD.getResourceDir() + "/"
        icon_path = ResourceDir + "Mod/Hermes/Resources/icons/GeometryDefiner.png"
        # icon_path = os.path.join(CfdTools.get_module_path(), "Gui", "Resources", "icons", "physics.png")

        return {'Pixmap': icon_path,
                'MenuText': QtCore.QT_TRANSLATE_NOOP("GeometryDefinerSelection", "Export Geometry Definer"),
                'Accel': "",
                'ToolTip': QtCore.QT_TRANSLATE_NOOP("GeometryDefinerSelection", "Export Geometry Definer as obj")}

    def IsActive(self):
        GD = FreeCAD.ActiveDocument.getObjectsByLabel("GeometryDefiner")[0]
        if GD is not None:
            children = GD.Group
            if len(children) > 0:
                return True
            else:
                return False
        return False

    def Activated(self):
        FreeCAD.ActiveDocument.openTransaction("Choose export")

        # get GeometryDefiner FreeCAD object
        GD = FreeCAD.ActiveDocument.getObjectsByLabel("GeometryDefiner")[0]

        # add all GeometryDefiner objects to a list
        objs = []
        for child in GD.Group:
            objs.append(child)

        # create help cube
        h_cube = FreeCAD.ActiveDocument.addObject("Part::Box", "NoNameCube")
        # h_cube.Label = "NoNameCube"
        FreeCAD.ActiveDocument.recompute()
        # Add to objs list -> in case of 1 object will still exports in names
        objs.append(h_cube)

        # save file in wanted location
        self.save_obj_file(objs)

        #  remove help object
        FreeCAD.ActiveDocument.removeObject("NoNameCube")

        del objs

    def save_obj_file(self, objs):
        import Mesh
        import re

        # what the dialog open dir - path
        # path = FreeCAD.ConfigGet("UserAppData")
        path = os.getcwd()

        try:
            SaveName = QFileDialog.getSaveFileName(None, QString.fromLocal8Bit("Save Geometry Definer as obj file"), path,
                                                   "*.obj")  # PyQt4
        #                          "here the text displayed on windows" "here the filter (extension)"

        except Exception:
            SaveName, Filter = PySide.QtGui.QFileDialog.getSaveFileName(None, "Save Geometry Definer as obj file", path,
                                                                        "*.obj")  # PySide
        #       "here the text displayed on windows" "here the filter (extension)"

        if SaveName == "":  # if the name file are not selected then Abord process
            FreeCAD.Console.PrintMessage("Export obj file aborted" + "\n")
        else:  # if the name file are selected
            # remove unnecessary suffix if user added it
            if SaveName.endswith(".obj"):
                SaveName = re.sub('\.obj$', '', SaveName)

            FreeCAD.Console.PrintMessage(
                "Exporting file " + SaveName + ".obj" + "\n")  # text displayed to Report view (Menu > View > Report view checked)
            try:  # if error detected to export ...
                outpath = u"" + SaveName + ".obj"
                Mesh.export(objs, outpath)
            except Exception:  # if error detected to write
                FreeCAD.Console.PrintError(
                        "Error Exporting file " + "\n")  # detect error ... display the text in red (PrintError)




if FreeCAD.GuiUp:
    FreeCADGui.addCommand('GeometryDefinerSelection', _CommandGeometryDefinerSelection())


# =============================================================================
# #_BlockMeshNode
# =============================================================================
class _BlockMeshNode(_GeometryDefinerNode):
    '''
        the  class inherited from _GeometryDefinerNode -
            - use same functionality
            - update differnt structure of json
    '''


    def __init__(self, obj, nodeId, nodeData, name):
        super().__init__(obj, nodeId, nodeData, name)
        self.initBMflag = False
        self.BMcount = 0



    def initializeFromJson(self, obj):
        _HermesNode.initializeFromJson(self, obj)

        # additional initialization BlockMesh node
        self.linkPartToBM(obj)

        # get Geometry Face types section from json
        GeometryFaceTypes = self.nodeData["GeometryFaceTypes"]

        # get the list of available Geometry Face types
        TypeList = GeometryFaceTypes["TypeList"]

        # get the list of Geometry Entities that has been saved
        # boundaryList = self.nodeData["boundary"]
        # to make sure entities are not uploaded from json
        boundaryList = []

        # Loop all the Geometry Entities that has been saved (BME = BlockMeshEntity )
        for boundary in boundaryList:

            # Create the BME node
            BMENodeObj = HermesGeometryDefinerNode.makeEntityNode('BME', TypeList, boundary, obj)
            if BMENodeObj is None:
                return None

            # get the GE properties, and update their current value
            GEProperties = boundary["Properties"]
            BMENodeObj.Proxy.setCurrentPropertyGE(BMENodeObj, GEProperties)

            # Update the faces attach to the BME (also create the parts)
            BMENodeObj.Proxy.initFacesFromJson(BMENodeObj)

            # get BME Name and update his Label property
            BMEName = boundary["Name"]
            BMENodeObj.Label = BMEName

            # get BME type and update his Type property
            BMEType = boundary["Type"]
            BMENodeObj.Type = BMEType



    def linkPartToBM(self, obj):

        # get the part name and path
        partPath = getattr(obj, "partPath")
        partName = getattr(obj, "partName")

        if len(partPath) != 0 and len(partName) != 0:

            # Create full path of the part for Import
            pathPartStr = partPath + partName + ".stp" if list(partPath)[-1] == '/' else partPath + "/" + partName + ".stp"

            # get workflow obj
            workflowObj = obj.getParentGroup()

            # create the part
            # partNameFC = workflowObj.Proxy.loadPart(workflowObj, pathPartStr)
            partNameFC = ""

            # make sure part imported
            if len(partNameFC) != 0:

                # get part by its name in FC
                partObj = FreeCAD.ActiveDocument.getObject(partNameFC)

                # update the part Name at the BlockMesh node properties
                setattr(obj, "partName", partNameFC)

                # link the part to thr BlockMesh node
                setattr(obj, "partLink", partObj)

                # flag for linking from json
                self.initBMflag = True

                # link the part to BM children
                for child in obj.Group:
                    # set the BlockMesh partlink  at each child
                    setattr(child, "partLink", partObj)
            else:
                FreeCAD.Console.PrintWarning('BlockMesh part has not been uploaded - check path and/or name of the part\n')
        else:
            FreeCAD.Console.PrintWarning('path or name of the BlockMesh part is missing\n')

    def backupNodeData(self, obj):
        # super().backupNodeData(obj)
        for child in obj.Group:
            child.Proxy.UpdateFacesInJson(child)

        # get workflow object
        workflowObj = obj.getParentGroup()

        # get part object
        partObj = getattr(obj, "partLink")
        if partObj is not None:
            # get the part dictionary with and vertices data
            partName = partObj.Name
            partDict = workflowObj.Proxy.partList[partName]
            vertices = partDict["Vertices"]["openFoam"]

            # export BM partand json - do no export part here
            # remove connection part
            # workflowObj.Proxy.ExportPart(partName)

            # update vertices in nodedata
            self.updateVertices(vertices)

        # update boundry in nodedata
        self.updateBoundry(obj)

        # Update nodeData  at the NodeDataString by converting from json to string
        obj.NodeDataString = json.dumps(self.nodeData)

    def updateBoundry(self, obj):
        # initialize boundry list
        boundryList = []

        # loop all objects in Nodeobj
        for child in obj.Group:

            # get GE-child nodeDate from EntityNodeDataString property
            BMEnodeData = json.loads(child.EntityNodeDataString)

            # update the GE-child nodeDate in the Geometry Entity List section
            boundryList.append(BMEnodeData)

        # update the Geometry Entity List section data in nodeData
        self.nodeData['boundary'] = boundryList


    def updateVertices(self, vertices):

        # create a list of string vertices
        stringVertices = []
        for ver in vertices:
            string = self.createVerticesString(vertices[ver])
            stringVertices.append(string)

        # push the list to the form data
        self.nodeData['vertices'] = stringVertices

    def createVerticesString(self, ver):
        string =""
        for cor in ver['coordinates']:
            string += str(ver['coordinates'][cor]) + " "

        return string


    def UpdateNodePropertiesData(self, obj):

        # get workflow object
        workflowObj = obj.getParentGroup()

        # update part path
        setattr(obj, "partPath", workflowObj.ExportJSONFile)

        # update properties as parent
        _HermesNode.UpdateNodePropertiesData(self, obj)

        # update children propeties
        for child in obj.Group:
            # update current properties value of the GE-child
            child.Proxy.UpdateGENodePropertiesData(child)






