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
# from hermes.Resources.workbench.HermesNode import _WebGuiNode
from ...HermesNode import _WebGuiNode, _HermesNode
from ... import HermesNode


# =============================================================================
# FvSchemes
# =============================================================================
class FvSchemes(_WebGuiNode):
    def __init__(self, obj, nodeId, nodeData, name):
        super().__init__(obj, nodeId, nodeData, name)

    def initializeFromJson(self, obj):
        '''
            initialized like any other webGui node
            add fields nodes from Hermes node list
        '''
        super().initializeFromJson(obj)

        rootParent = self.getRootParent(obj.getParentGroup())
        for field in rootParent.CalculatedFields:
            fv_name = "fvSch_" + field
            nodeData = copy.deepcopy(self.nodeData["fields"]["template_webGui"])
            nodeData["WebGui"]["Schema"]["title"] = fv_name
            fvSchField_obj = HermesNode.makeNode(fv_name, obj, str(0), nodeData)

    def backupNodeData(self, obj):
        ''' update the data from FreeCAD(node and children) to json '''
        super().backupNodeData(obj)

        # need to back up the child data in the main fv
        for child in obj.Group:
            field = child.Name.replace("fvSch_", "")
            self.nodeData["fields"]["items"][field] = child.Proxy.nodeData

    def jsonToJinja(self, obj):
        ''' convert the json data to "inputParameters" structure '''

        default = copy.deepcopy(self.nodeData["WebGui"]["formData"])

        fields = {}
        for child in obj.Group:
            field = child.Name.replace("fvSch_", "")
            ch_fd = copy.deepcopy(child.Proxy.nodeData["WebGui"]["formData"])
            fields[field] = ch_fd


        return dict(fields=fields, default=default)

    def updateNodeFields(self, fieldList, obj):
        '''
            update the children nodes with the field of the problem
            - take the list of field from HermesNode
            - take the list of children nodes
            - compare between the lists, and add/remove nodes
        '''

        ObjfieldList = list()
        for objField in obj.Group:
            # get the field from obj label
            field = objField.Label.split('_')[-1]

            # remove spaces
            field.replace(" ", "")

            if len(field) > 0:
                ObjfieldList.append(field)

        # remove spaces from Hermes field list
        fieldList = [Field.replace(" ", "") for Field in fieldList if len(Field.replace(" ", "")) > 0]

        # create list of items need to be added or removed from webGui
        add_list = [field for field in fieldList if field not in ObjfieldList]
        del_list = [field for field in ObjfieldList if field not in fieldList]



        # FreeCAD.Console.PrintMessage("self.nodeData = " + str(self.nodeData) + "\n")
        # FreeCAD.Console.PrintMessage("self.nodeData[Templates][objField] = " + str(self.nodeData["Templates"]["objField"]) + "\n")

        # create a new field object
        if len(add_list) > 0:
            for field in add_list:
                fv_name = "fvSch_" + field
                nodeData = copy.deepcopy(self.nodeData["fields"]["template_webGui"])
                nodeData["WebGui"]["Schema"]["title"] = fv_name
                fvSchField_obj = HermesNode.makeNode(fv_name, obj, str(0), nodeData)

        # remove fields from webGui
        for field in del_list:
            for objField in obj.Group:
                if field in objField.Label:
                    obj.Document.removeObject(objField.Name)
