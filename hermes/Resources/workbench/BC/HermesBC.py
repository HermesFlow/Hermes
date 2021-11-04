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
from ..HermesNode import _WebGuiNode, _ViewProviderNode
from .. import HermesNode
from ..HermesTools import addObjectProperty

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
                bc_part_obj = HermesNode.makeNode(bc_part_name, obj, str(0), copy.deepcopy(self.nodeData["Templates"]["BCGeometry"]))
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
                bc_field_obj = HermesNode.makeNode(part.Label + "_" + field, bcObj, str(0), copy.deepcopy(parent.Proxy.nodeData["Templates"]["BCField"]))

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