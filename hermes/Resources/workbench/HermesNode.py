# import FreeCAD modules
import FreeCAD, FreeCADGui, WebGui

if FreeCAD.GuiUp:
    import FreeCADGui
    from PySide import QtCore

    # from PySide import QtGui, QtCore
    # from PySide.QtGui import *
    # from PySide.QtCore import *

# python modules
from PyQt5 import QtCore
import json
import pydoc
import os
import copy

# Hermes modules
import HermesTools
from HermesTools import addObjectProperty


def makeNode(name, workflowObj, nodeId, nodeData):
    """ Create a Hermes Node object """

    # Object with option to have children
    obj = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroupPython", name)

    #    # Object can not have children
    #    obj = FreeCAD.ActiveDocument.addObject("App::FeaturePython", name)

    # add Nodeobj(obj) as child of workflowObj
    workflowObj.addObject(obj)

    # ----------------dynamic find class--------------------
    nodecls = None
    # find the class of the node from the its type
    # nodecls = pydoc.locate("HermesNode." + '_' + nodeData["Type"])
    try:
        nodecls = pydoc.locate(nodeData["Type"])
    except:
        # in case pydoc couldn't find the class, try with another method
        import importlib
        workbencj_path = "hermes.Resources.workbench"
        path = nodeData["Type"]

        # join and make sure path with '.'
        path = os.path.join(workbencj_path, path)
        path = path.replace("/", ".")

        module_name, class_name = path.rsplit(".", 1)
        try:
            FreeCAD.Console.PrintMessage("module_name = " + module_name + "\n")
            FreeCAD.Console.PrintMessage("class_name = " + class_name + "\n")
            # if "BlockMeshNode" in class_name:
            #     module_name = "hermes.Resources.workbench.openFOAM2.mesh.HermesBlockMesh"
            #     class_name ="_BlockMeshNode"
            # FreeCAD.Console.PrintMessage("module_name = " + module_name + "\n")
            # FreeCAD.Console.PrintMessage("class_name = " + class_name + "\n")

            nodecls = getattr(importlib.import_module(module_name), class_name)
        except Exception:  # if error detected to write
            FreeCAD.Console.PrintError("Error locating class" + class_name + "\n")


    # call to the class
    if nodecls is not None:
        nodecls(obj, nodeId, nodeData, name)

        # if name == "BlockMesh":
        #     return
        obj.Proxy.initializeFromJson(obj)

        if FreeCAD.GuiUp:
            if (nodeData["Type"] in ['HermesNode._BCNode', 'HermesNode._BCGeometryNode', 'HermesNode._BCFieldNode']):
                _ViewProviderNodeBC(obj.ViewObject)
            else:
                _ViewProviderNode(obj.ViewObject)

        FreeCAD.ActiveDocument.recompute()
    else:
        FreeCAD.Console.PrintWarning("Could not locate node name = " + name + ": ")
        FreeCAD.Console.PrintWarning("nodeData['Type'] = " + nodeData["Type"] + "\n")

    return obj


# **********************************************************************
class _CommandHermesNodeSelection:
    """ CFD physics selection command definition """

    def GetResources(self):
        icon_path = os.path.join(FreeCAD.getResourceDir(), "Mod", "Hermes", "Resources", "icons", "NewNode.png")

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


# **********************************************************************
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
        else:
            # addObjectProperty(obj, "partLink", None, "App::PropertyLink", "BasicData", "Link to part")
            addObjectProperty(obj, "partLinkName", "", "App::PropertyString", "BasicData", "Link to part by Name")
            obj.setEditorMode("partLinkName", 1)  #(2 = hidden)

        # Type of the Object - (web/GE)
        addObjectProperty(obj, "Type", "-1", "App::PropertyString", "Node Type", "Type of node")
        obj.setEditorMode("Type", 1)  # Make read-only (2 = hidden)

        # Is Avtive property- Boolean -keep if obj has been activated (douuble clicked get active)
        addObjectProperty(obj, "IsActiveObj", False, "App::PropertyBool", "", "Active Node object in document")
        obj.setEditorMode("IsActiveObj", 1)  # Make read-only (2 = hidden)

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

        FreeCAD.Console.PrintMessage("Node " + obj.Name + " onDocumentRestored\n")

        if FreeCAD.GuiUp:
            _ViewProviderNode(obj.ViewObject)

    # just an example - not used
    def changeLabel(self):
        #        FreeCAD.Console.PrintMessage("\nChange Label\n")
        return

    def doubleClickedNode(self, obj):

        # get "workflowObj" from been parent of the node obj
        workflowObj = self.getRootParent(obj)

        # backup last node and update "nLastNodeId" in Hermes workflow
        workflowObj.Proxy.updateLastNode(workflowObj)

        # update is active
        obj.IsActiveObj = True

        # FreeCAD.ActiveDocument.recompute()

        return

    def getRootParent(self, obj):
        if obj.getParentGroup() is None:
            return obj
        else:
            rootParent = self.getRootParent(obj.getParentGroup())

        return rootParent

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
            child.Proxy.RemoveNodeObj(child)
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
        ResourceDir = FreeCAD.getResourceDir() if list(FreeCAD.getResourceDir())[
                                                      -1] == '/' else FreeCAD.getResourceDir() + "/"
        # if self.NodeObjType == "WebGuiNode" or self.NodeObjType == "SnappyHexMeshCastellatedMeshControls" or self.NodeObjType == 'SnappyHexMesh' or self.NodeObjType == "FvSolution" or self.NodeObjType == "FvSchemes":
        if self.NodeObjType in ["HermesNode._WebGuiNode","HermesSnappyHexMesh._SnappyHexMesh", "HermesSnappyHexMesh._SnappyHexMeshCastellatedMeshControls"]:
            icon_path = ResourceDir + "Mod/Hermes/Resources/icons/Web.png"
        elif "FvSolution" in self.NodeObjType:
            icon_path = ResourceDir + "Mod/Hermes/Resources/icons/Web.png"
        elif "FvSchemes" in self.NodeObjType:
            icon_path = ResourceDir + "Mod/Hermes/Resources/icons/Web.png"
        elif self.NodeObjType == "HermesNode._GeometryDefinerNode":
            icon_path = ResourceDir + "Mod/Hermes/Resources/icons/GeometryDefiner.png"
        else:
            icon_path = ResourceDir + "Mod/Hermes/Resources/icons/NewNode.png"
        #
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
                # get the part object using prop
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

        # delay recompute of all objects, and return the touch to the current object
        QtCore.QTimer.singleShot(350, FreeCAD.ActiveDocument.recompute)
        QtCore.QTimer.singleShot(350, vobj.Object.touch)

    def __getstate__(self):
        # Create NodeObj using Object name
        NodeObj = FreeCAD.ActiveDocument.getObject(self.NodeObjName)

        if NodeObj is None:
            return

        # if node has been active - backup
        if NodeObj.IsActiveObj:
            NodeObj.Proxy.backupNodeData(NodeObj)

        # get the last updated NodeDataString
        getNodeString = NodeObj.NodeDataString

        # return an array with NodeObj name and the updated NodeDataString -
        # it will be recieved by "__setstate__" when opening the project
        return [self.NodeObjName, getNodeString]

    def __setstate__(self, state):
        ''' state - recieved from 'getstate', while saving the project "Hermesworkflow"
                type :array ,including 2 variebelles,
                     state[0]= Name of the Node Object
                     state[1]= nodeDataString - the last uppdated Json string before saving.'''

        NodeObjName = state[0]
        nodeDataString = state[1]

        # get Object using OBject name
        NodeObj = FreeCAD.ActiveDocument.getObject(NodeObjName)
        if NodeObj is None:
            return

        # update the nodeDataString at the NodeObj
        NodeObj.NodeDataString = nodeDataString

        return None


# =============================================================================
# #_WebGuiNode
# =============================================================================
class _WebGuiNode(_HermesNode):

    def __init__(self, obj, nodeId, nodeData, name):
        super().__init__(obj, nodeId, nodeData, name)

    def doubleClickedNode(self, obj):
        super().doubleClickedNode(obj)
        self.selectNode(obj)

    def selectNode(self, obj):

        # get node WebGui- Scheme,uiScheme,FormData
        nodeWebGUI = self.nodeData["WebGui"]

        # FreeCAD.Console.PrintMessage("Schema = " + str(nodeWebGUI["Schema"]) + "\n")
        # FreeCAD.Console.PrintMessage("==========================\n")

        # Check if webGui is empty
        if not ((len(nodeWebGUI) == 0)):
            # define web address & pararmeters
            ResourceDir = FreeCAD.getResourceDir() if list(FreeCAD.getResourceDir())[
                                                          -1] == '/' else FreeCAD.getResourceDir() + "/"
            path = ResourceDir + 'Mod/Hermes/Resources/jsonReactWebGui.html?parameters='
            address = 'file:///' + path

            # FreeCAD.Console.PrintMessage("path = " + path + "\n")
            # FreeCAD.Console.PrintMessage("address = " + address + "\n")


            # str JSON 'nodeWebGUI' using "dumps"
            parameters = json.dumps(nodeWebGUI)

            # open the jsonReact html page using the following command
            browser = WebGui.openSingleBrowser(address + parameters)
            sRegName = '0,' + self.name
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

        # self.print_formData()

    def backupNodeData(self, obj):
        # backup the data of the last node pressed
        super().backupNodeData(obj)

        # then Update nodeData  at the NodeDataString by converting from json to string
        obj.NodeDataString = json.dumps(self.nodeData)

    def jsonToJinja(self, obj):
        if obj.Name == "ControlDict":
            return dict(values="{WebGui.formData}")
        elif "formData" in self.nodeData["WebGui"]:
            return self.nodeData["WebGui"]["formData"]
        else:
            return None

    def print_formData(self):
        formData = self.nodeData["WebGui"]["formData"]
        FreeCAD.Console.PrintMessage("----------------------------------------------------------------\n")
        FreeCAD.Console.PrintMessage("print_formData of node " + self.name +"\n")
        FreeCAD.Console.PrintMessage("['formData']="+str(formData)+"\n")
        FreeCAD.Console.PrintMessage("----------------------------------------------------------------\n")

# =============================================================================
# _BCNode
# =============================================================================
class _BCNode(_WebGuiNode):
    #    super().funcName(var1,var,2..) - allow to use the function of the Parent,
    #    and add current class functionalites

    def __init__(self, obj, nodeId, nodeData, name):
        super().__init__(obj, nodeId, nodeData, name)
        self.iconColor = "red"

        workflowObj = self.getRootParent(obj)

        # self.updateBCNodeFields(workflowObj.CalculatedFields, obj)

    def selectNode(self, obj):
        self.updateBCPartList(obj)
        super().selectNode(obj)


    def updateNodeFields(self, fieldList, obj):

        for bcObj in obj.Group:
            bcObj.Proxy.updateNodeFields(fieldList, bcObj)


    def updateBCPartList(self, obj):

        workflowObj = self.getRootParent(obj)
        nodesPartList = list()
        nodesObjList = list()

        # create bc nodes to these geometries
        # get each node geometries
        for node in self.nodeData["GeometriesSource"]:
            split_node = node.split('.')

            # case it is first order node
            if len(split_node) == 1:
                nodeGroup = FreeCAD.ActiveDocument.getObject(node)
            # case of inner node holding the geometries
            elif len(split_node) > 1:
                treeObjList = [FreeCAD.ActiveDocument.getObject(node) for node in split_node]
                treeObjList.reverse()
                i = 0
                while len(treeObjList) > 1:
                    if treeObjList[i] in treeObjList[i + 1].Group:
                        if i == 0:
                            nodeGroup = treeObjList[i]

                        treeObjList.remove(treeObjList[i])
                    else:
                        FreeCAD.Console.PrintWarning("node " + node + "has not been found \n")
                    i = i + 1


            nodePartList = list()
            # get node and BC part list
            if nodeGroup is not None:
                for nodeObj in nodeGroup.Group:
                    if nodeObj.Module == 'Part':
                        # nodePartList.append(nodeObj)
                        nodePartList.append(nodeObj.Name)
                    else:
                        # part = FreeCAD.ActiveDocument.getObject(nodeObj.partLinkName)
                        part = nodeObj.partLinkName
                        # if part is not None:
                        if len(part) > 0:
                            nodePartList.append(part)

            nodesPartList += nodePartList
            nodesObjList.append(nodeGroup)

        # BCpartList = [FreeCAD.ActiveDocument.getObject(BCobj.partLinkName) for BCobj in obj.Group if len(BCobj.partLinkName) > 0]
        BCpartList = [BCobj.partLinkName for BCobj in obj.Group if len(BCobj.partLinkName) > 0]

        # compare the list - check if need to delete or add objects
        add_list = [part for part in nodesPartList if part not in BCpartList]
        del_list = [part for part in BCpartList if part not in nodesPartList]


        # get Hermes workflow



        # for nodeGroup in nodesObjList:
            # create a new bc geometry object
        if len(add_list) > 0:
            for partName in add_list:
                # part = FreeCAD.ActiveDocument.getObject(partName)

                # bc_part_name = "bc_" + self.getNodeLabel(part, nodeGroup)
                bc_part_name = "bc_" + self.getNodeLabel(partName, nodesObjList)
                bc_part_obj = makeNode(bc_part_name, obj, str(0), copy.deepcopy(self.nodeData["Templates"]["BCGeometry"]))
                if bc_part_obj is None:
                    FreeCAD.Console.PrintMessage("add None: bc_part_name = " + bc_part_name + "\n")

                bc_part_obj.partLinkName = partName
                bc_part_obj.Proxy.updateNodeFields(workflowObj.CalculatedFields, bc_part_obj)

         # remove bc geometry objects
        if len(del_list) > 0:
            for partName in del_list:
                for bcPart in BCpartList:
                    if bcPart == partName:

                        bcPartObj = self.getDelNode(partName, obj)
                        for child in bcPartObj.Group:
                            obj.Document.removeObject(child.Name)
                        obj.Document.removeObject(bcPartObj.Name)

    def getNodeLabel(self, partName, nodeGroupList):
        for nodeGroup in nodeGroupList:
            for node in nodeGroup.Group:
                if node.Name == partName:
                    return node.Label
                elif 'partLinkName' in node.PropertiesList:
                    if partName == node.partLinkName:
                        return node.Label
        return None

    def getDelNode(self, partName, obj):
        for child in obj.Group:
            if child.partLinkName == partName:
                return child
        return None

    def getIconColor(self, obj):
        if len(obj.Group) == 0:
            self.iconColor = 'red'
            return 'red'

        # colorList = [child.Proxy.iconColor for child in obj.Group]
        colorList = [child.Proxy.getIconColor(child) for child in obj.Group]

        # FreeCAD.Console.PrintMessage("BC.getIconColor: colorList = "+ str(colorList) + "\n")


        countRed = 0
        countGreen = 0
        for color in colorList:
            if color == 'green':
                countGreen += 1
            if color == 'red':
                countRed += 1

        iconColor = ""
        if countGreen == len(colorList):
            iconColor = "green"
        elif countRed == len(colorList):
            iconColor = "red"
        else:
            iconColor = "yellow"

        self.iconColor = iconColor
        return iconColor

    def backupNodeData(self, obj):
        super().backupNodeData(obj)
        # FreeCADGui.doCommand("FreeCAD.ActiveDocument.getObject('" + obj.Name + "').enforceRecompute()")
        # FreeCADGui.doCommand("FreeCAD.ActiveDocument.getObject('" + obj.Name + "').recompute()")



    def onDocumentRestored(self, obj):

        workflowObj = obj.getParentGroup()
        workflowObj.Proxy.nLastNodeId = "-1"

        # parse json data
        self.nodeData = json.loads(obj.NodeDataString)

        # when restored- initilaize properties
        self.initProperties(obj)

        FreeCAD.Console.PrintMessage("Node " + obj.Name + " onDocumentRestored\n")

        if FreeCAD.GuiUp:
            _ViewProviderNodeBC(obj.ViewObject)

    def jsonToJinja(self, obj):

        HermesWorkflow = self.getRootParent(obj)
        jinja = dict()
        # loop all fields defined
        for field in HermesWorkflow.CalculatedFields:
            obj_field = dict()
            # loop each geom and get its field BC data
            for geom in obj.Group:
                geom_fields = geom.Group
                for cf in geom_fields:
                    if field in cf.Name:
                        part = FreeCAD.ActiveDocument.getObject(geom.partLinkName)
                        formData = cf.Proxy.nodeData["WebGui"]["formData"]
                        obj_jinja = dict()
                        for key, value in formData.items():
                            if "type" in key:
                                obj_jinja["type"] = value
                            else:
                                obj_jinja[key] = value
                        obj_field[part.Label] = obj_jinja

            jinja[field] = copy.deepcopy(obj_field)

        # FreeCAD.Console.PrintMessage("BC jinja = " + str(jinja) + "\n")
        return dict(fields=jinja)

# =============================================================================
# _BCGeometryNode
# =============================================================================
class _BCGeometryNode(_WebGuiNode):
    def __init__(self, obj, nodeId, nodeData, name):
        super().__init__(obj, nodeId, nodeData, name)
        self.iconColor = "red"

    def initProperties(self, obj):
        super().initProperties(obj)

        # Is Avtive property- Boolean -keep if obj has been activated (douuble clicked get active)
        addObjectProperty(obj, "colorFlag", False, "App::PropertyBool", "", "update color flag")
        obj.setEditorMode("colorFlag", 2)  # Make read-only (2 = hidden)



    def getIconColor(self, obj):
        if len(obj.Group) == 0:
            self.iconColor = 'red'
            return 'red'

        # colorList = [child.Proxy.iconColor for child in obj.Group]
        colorList = [child.Proxy.getIconColor(child) for child in obj.Group]

        # FreeCAD.Console.PrintMessage("BCGeometryNode.getIconColor: colorList = "+ str(colorList) + "\n")

        countRed = 0
        countGreen = 0
        for color in colorList:
            if color == 'green':
                countGreen += 1
            if color == 'red':
                countRed += 1

        iconColor = "red"
        if countGreen == len(colorList):
            iconColor = "green"
        elif countRed == len(colorList):
            iconColor = "red"
        else:
            iconColor = "yellow"

        self.iconColor = iconColor
        return iconColor


    def backupNodeData(self, obj):
        super().backupNodeData(obj)

    def onDocumentRestored(self, obj):

        workflowObj = obj.getParentGroup()
        workflowObj.Proxy.nLastNodeId = "-1"

        # parse json data
        self.nodeData = json.loads(obj.NodeDataString)

        # when restored- initilaize properties
        self.initProperties(obj)

        FreeCAD.Console.PrintMessage("Node " + obj.Name + " onDocumentRestored\n")

        if FreeCAD.GuiUp:
            _ViewProviderNodeBC(obj.ViewObject)

    def updateNodeFields(self, fieldList, bcObj):

        # get part from Name
        part = FreeCAD.ActiveDocument.getObject(bcObj.partLinkName)

        # get the Field name from the bc_field obj - remove the "part_" from obj label
        # BCfieldList = [bcField.Label.replace(part.Label + '_', '') for bcField in bcObj.Group]
        BCfieldList = list()
        for bcField in bcObj.Group:
            # remove the "part_" from obj label
            field = bcField.Label.split('_')[-1]

            # remove spaces
            field.replace(" ", "")

            if len(field) > 0:
                BCfieldList.append(field)

        # remove spaces from Hermes field list
        fieldList = [Field.replace(" ", "") for Field in fieldList if len(Field.replace(" ", "")) > 0]

        # create list of items need to be added or removed from webGui
        add_list = [field for field in fieldList if field not in BCfieldList]
        del_list = [field for field in BCfieldList if field not in fieldList]


        parent = bcObj.getParentGroup()

        # FreeCAD.Console.PrintMessage("self.nodeData = " + str(self.nodeData) + "\n")
        # FreeCAD.Console.PrintMessage("self.nodeData[Templates][BCField] = " + str(self.nodeData["Templates"]["BCField"]) + "\n")

        # create a new bc geometry object
        if len(add_list) > 0:
            for field in add_list:
                bc_field_obj = makeNode(part.Label + "_" + field, bcObj, str(0), copy.deepcopy(parent.Proxy.nodeData["Templates"]["BCField"]))

                bc_field_nodeData = bc_field_obj.Proxy.nodeData
                bc_field_nodeData["WebGui"]["Schema"]["title"] = field + " - " + part.Label
                bc_field_nodeData["WebGui"]["Schema"]["description"] = "Defined " + field + " Boundary condition for the part."
                bc_field_obj.Proxy.nodeData = bc_field_nodeData

        # remove fields from webGui
        for field in del_list:
            for bcField in bcObj.Group:
                if field in bcField.Label:
                    bcObj.Document.removeObject(bcField.Name)


# =============================================================================
# _BCFieldNode
# =============================================================================
class _BCFieldNode(_WebGuiNode):
    def __init__(self, obj, nodeId, nodeData, name):
        super().__init__(obj, nodeId, nodeData, name)
        self.iconColor = "red"

    def getIconColor(self, obj):
        webGui = obj.Proxy.nodeData["WebGui"]
        formData = webGui["formData"]
        color = "red"

        if len(webGui["formData"]) == 0:
            self.iconColor = "red"
            return 'red'
        else:
            typeBC = formData["typeBC"]
            if typeBC == "notSet":
                self.iconColor = "red"
                return 'red'
            else:
                color = self.compareSchemeFormData(webGui)

        self.iconColor = color
        return color

    def compareSchemeFormData(self,webGui):
        schema = webGui["Schema"]
        formData = copy.deepcopy(webGui["formData"])

        # take the properties keys from the schemes - in case there will be more properties but typeBC
        scheme_list = list(schema["properties"].keys())

        if "typeBC" not in formData:
            return 'red'

        typeBC = formData["typeBC"]
        # take the properties keys from the dependencies
        dependencies = schema["dependencies"]
        for depend in dependencies["typeBC"]["oneOf"]:
            if depend["properties"]["typeBC"]["enum"][0] == typeBC:
                depend_list = list(depend["properties"].keys())
                lenDependList = len(depend_list)
                scheme_list += depend_list

        # remove duplication from list
        scheme_list = list(dict.fromkeys(scheme_list))

        # remove typeBC from both scheme_list and formData
        scheme_list.remove("typeBC")
        formData.pop("typeBC")

        # FreeCAD.Console.PrintMessage("compareSchemeFormData: scheme_list = " + str(scheme_list) + "\n")
        # FreeCAD.Console.PrintMessage("compareSchemeFormData: formData = " + str(list(formData.keys())) + "\n")


        # take only the keys in both formData and scheme
        # (the formData keep all extra properties added from specific typeBC Enum. In case of changing the enum it will display former fill in)
        # diff_scheme = [key for key in scheme_list if key in formData]
        same_formData = [key for key in formData if key in scheme_list]
        # diff_formData = [key for key in formData if key not in scheme_list]

        # FreeCAD.Console.PrintMessage("compareSchemeFormData: same_formData = " + str(same_formData) + "\n")

        if lenDependList == 1:
            return 'green'
        elif len(same_formData) == len(scheme_list):
            return 'green'
        elif len(same_formData) < len(scheme_list):
            return 'yellow'

        FreeCAD.Console.PrintMessage("compareSchemeFormData - got to the last return")

        return 'red'

    def backupNodeData(self, obj):
        super().backupNodeData(obj)


    def onDocumentRestored(self, obj):

        workflowObj = obj.getParentGroup()
        workflowObj.Proxy.nLastNodeId = "-1"

        # parse json data
        self.nodeData = json.loads(obj.NodeDataString)

        # when restored- initilaize properties
        self.initProperties(obj)

        FreeCAD.Console.PrintMessage("Node " + obj.Name + " onDocumentRestored\n")

        if FreeCAD.GuiUp:
            _ViewProviderNodeBC(obj.ViewObject)


# =============================================================================
#      "_ViewProviderNodeBC" class
# =============================================================================
class _ViewProviderNodeBC(_ViewProviderNode):

    def getIcon(self):
        # Define Resource dir end with ','
        ResourceDir = FreeCAD.getResourceDir() if list(FreeCAD.getResourceDir())[
                                                      -1] == '/' else FreeCAD.getResourceDir() + "/"


        obj = FreeCAD.ActiveDocument.getObject(self.NodeObjName)

        color = obj.Proxy.getIconColor(obj)

        # FreeCAD.Console.PrintMessage("_ViewProviderNodeBC.getIcon: self.NodeObjName = " + self.NodeObjName + "; color = "+ color +"\n")

        if color == 'red':
            icon_path = ResourceDir + "Mod/Hermes/Resources/icons/red_ball.png"
        elif color == 'yellow':
            icon_path = ResourceDir + "Mod/Hermes/Resources/icons/yellow_ball.png"
        elif color == 'green':
            icon_path = ResourceDir + "Mod/Hermes/Resources/icons/green_ball.png"
        else:
            icon_path = ResourceDir + "Mod/Hermes/Resources/icons/blue_ball.png"

        # FreeCAD.Console.PrintMessage("_ViewProviderNodeBC - getIcon \n")
        # QtCore.QTimer.singleShot(1000, FreeCAD.ActiveDocument.recompute)

        return icon_path
