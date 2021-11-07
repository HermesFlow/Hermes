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
# from BC.HermesBC import _ViewProviderNodeBC

# ********************************************************************
def makeNode(name, workflowObj, nodeId, nodeData):
    """ Create a Hermes Node object """

    # Group object with option to have children
    obj = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroupPython", name)

    #    # Object can not have children
    #    obj = FreeCAD.ActiveDocument.addObject("App::FeaturePython", name)

    # add Nodeobj(obj) as child of workflowObj
    workflowObj.addObject(obj)

    # ----------------dynamic find class--------------------
    nodecls = None
    # find the class of the node from the its type
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
            # FreeCAD.Console.PrintMessage("module_name = " + module_name + "\n")
            # FreeCAD.Console.PrintMessage("class_name = " + class_name + "\n")
            nodecls = getattr(importlib.import_module(module_name), class_name)
        except Exception:  # if error detected to write
            FreeCAD.Console.PrintError("Error locating class" + class_name + "\n")


    # call to the class
    if nodecls is not None:
        nodecls(obj, nodeId, nodeData, name)

        obj.Proxy.initializeFromJson(obj)

        if FreeCAD.GuiUp:
            if "BC" in nodeData["Type"]:
                BC_view = pydoc.locate("hermes.Resources.workbench.BC.HermesBC._ViewProviderNodeBC")
                BC_view(obj.ViewObject)
            else:
                _ViewProviderNode(obj.ViewObject)

        FreeCAD.ActiveDocument.recompute()
    else:
        FreeCAD.Console.PrintWarning("Could not locate node name = " + name + ": ")
        FreeCAD.Console.PrintWarning("nodeData['Type'] = " + nodeData["Type"] + "\n")

    return obj


# **********************************************************************
class _CommandHermesNodeSelection:
    """ Hermes Node selection command definition """

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

    def __init__(self, obj, nodeId, nodeData, name):
        obj.Proxy = self
        self.nodeId = nodeId
        self.nodeData = nodeData
        self.name = name
        self.initProperties(obj)

    def initializeFromJson(self, obj):
        '''
            Takes the properties from JSON and update its value
             at the FreeCAD object
        '''

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
        '''
            Creates the properties of the FreeCAD object
            static properties  - basic properties for each node
            dynamic properties - special properties defined at the JSON file
        '''

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
        '''
            When a FreeCAD document is restored (opened after been saving
            as a FreeCAD file), it updates the following things in the Node
        '''

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
        '''
            Activated when doubleClick on node
            - updates its data
            - turn the node Active
        '''

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
        '''
            Update the properties from FreeCAD node into the JSON
        '''
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
        '''
            remove NodeObj Children
            use when importing new json file
        '''
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
        '''
            Defines the icon in the combo tree
        '''
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
        '''
            When a FreeCAD object's property has been update,
            it checks if any thing else need to be handle, and do so
        '''

        # We get here when the object of Node changes
        fname = "_handle_%s" % str(prop)

        if hasattr(self, fname):
            getattr(self, fname)(obj)

    def _handle_ExportNodeJSONFile(self, obj):
        ''' update the data into JSON var, then export it '''
        if len(str(obj.ExportNodeJSONFile)) > 0:
            # get "workflowObj" from been parent of the node obj
            workflowObj = obj.getParentGroup()
            workflowObj.Proxy.prepareJsonVar(workflowObj, obj.Name)
            workflowObj.Proxy.saveJson(workflowObj, obj.ExportNodeJSONFile, obj.Label)
            obj.ExportNodeJSONFile = ''

    def _handle_RunNodeWorkflow(self, obj):
        ''' update the data into JSON , then run workflow'''
        if obj.RunNodeWorkflow:
            workflowObj = obj.getParentGroup()
            workflowObj.Proxy.prepareJsonVar(workflowObj, obj.Name)
            workflowObj.Proxy.RunworkflowCreation(workflowObj)

    def _handle_RunNodeLuigi(self, obj):
        ''' make sure workflow is updated and run luigi '''
        if obj.RunNodeLuigi and obj.RunNodeWorkflow:
            workflowObj = obj.getParentGroup()
            workflowObj.Proxy.RunLuigiScript()

    def _handle_ChooseMethod(self, obj):
        '''
            update the method RunOsCommand works
            - command list
            - batchfile
        '''
        if obj.Name == "RunOsCommand":
            # get the choosen methon
            method = getattr(obj, "ChooseMethod")

            # make read only the property that hasnt been choosen, and read/write the one been choose
            if method == "Commands list":
                obj.setEditorMode("batchFile", 1)  # Make read-only
                obj.setEditorMode("Commands", 0)  # read/write

            elif method == "batchFile":
                obj.setEditorMode("Commands", 1)  # Make read-only
                obj.setEditorMode("batchFile", 0)  # read/write

    def _handle_partLink(self, obj):
        '''
            update the partLink property of BlockMesh(and its References)
        '''
        if obj.Label == 'BlockMesh':
            # in case its initialized from Json stage, avoid overide data
            if obj.Proxy.initBMflag and (not obj.Proxy.BMcount):
                return

            print("viewProvider, updateData")
            # get the part object using prop
            partobj = getattr(obj, "partLink")

            # set the BlockMesh partlink  at each child
            for child in obj.Group:
                setattr(child, "partLink", partobj)
                setattr(child, "References", [])

            # also update part name in peoperties
            if partobj is None:
                setattr(obj, "partName", "")
            else:
                setattr(obj, "partName", partobj.Name)

            obj.Proxy.BMcount += 1


    def onChanged(self, vobj, prop):

        # not in use, just an example
        if (str(prop) == 'Label' and len(str(vobj.Label)) > 0):
            vobj.Proxy.changeLabel()
            return

    def doubleClicked(self, vobj):
        '''
            Activated when doubleClicking on the node
            - call to the object handle doubleclicking function
            - recompute in small delay for FreeCAD display
        '''
        vobj.Object.Proxy.doubleClickedNode(vobj.Object)

        # delay recompute of all objects, and return the touch to the current object
        QtCore.QTimer.singleShot(350, FreeCAD.ActiveDocument.recompute)
        QtCore.QTimer.singleShot(350, vobj.Object.touch)

    def __getstate__(self):
        '''
            Activate when saving the document as FreeCAD file
            saving the project "Hermesworkflow" in array ,including 2 variebelles,
                state[0]= Name of the Node Object
                state[1]= nodeDataString - the last uppdated Json string before saving.
        '''

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
    '''
        handle the webGui nodes
    '''

    def __init__(self, obj, nodeId, nodeData, name):
        super().__init__(obj, nodeId, nodeData, name)

    def doubleClickedNode(self, obj):
        super().doubleClickedNode(obj)
        self.selectNode(obj)

    def selectNode(self, obj):
        '''
            send the data from node webGui data, to the jsonRecat -
            'jsonReactWebGui.html' file. The a browser is opened in FreeCAD
            and dislay the data
        '''

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
        '''
            get the updated data from 'jsonReactWebGui.html', and save
            it to the node webGui.formData
        '''

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
        '''
            backup the data from FreeCAD object to its JSON
        '''
        # backup the data of the last node pressed
        super().backupNodeData(obj)

        # then Update nodeData  at the NodeDataString by converting from json to string
        obj.NodeDataString = json.dumps(self.nodeData)

    def jsonToJinja(self, obj):
        '''
            update the Execution.input_parameters JSON data
        '''
        if obj.Name == "ControlDict":
            return dict(values="{WebGui.formData}")
        elif "formData" in self.nodeData["WebGui"]:
            return self.nodeData["WebGui"]["formData"]
        else:
            return None

    def print_formData(self):
        '''
            help funtion -> prints the formData of the node
        '''
        formData = self.nodeData["WebGui"]["formData"]
        FreeCAD.Console.PrintMessage("----------------------------------------------------------------\n")
        FreeCAD.Console.PrintMessage("print_formData of node " + self.name +"\n")
        FreeCAD.Console.PrintMessage("['formData']="+str(formData)+"\n")
        FreeCAD.Console.PrintMessage("----------------------------------------------------------------\n")


