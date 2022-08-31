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
# from hermes.Resources.workbench.HermesNode import WebGuiNode
from ....workbench.HermesNode import WebGuiNode, HermesNode
from ....workbench import HermesNode

# =============================================================================
# FvSolution
# =============================================================================
class FvSolution(WebGuiNode):
    def __init__(self, obj, nodeId, nodeData, name):
        super().__init__(obj, nodeId, nodeData, name)

    def initializeFromJson(self, obj):
        '''
            initialized like any other webGui node
            add fields nodes from Hermes node list
        '''
        super().initializeFromJson(obj)

        rootParent = self.getRootParent(obj.getParentGroup())
        for field in rootParent.SolvedFields:
            fv_name = "fvSol_" + field
            nodeData = copy.deepcopy(self.nodeData["fields"]["template_webGui"])
            nodeData["WebGui"]["Schema"]["title"] = fv_name
            fvSolField_obj = HermesNode.makeNode(fv_name, obj, str(0), nodeData)

    def backupNodeData(self, obj):
        ''' update the data from FreeCAD(node and children) to json, '''
        super().backupNodeData(obj)

        # need to back up the child data in the main fv
        for child in obj.Group:
            field = child.Name.replace("fvSol_", "")
            self.nodeData["fields"]["items"][field] = child.Proxy.nodeData

    def guiToExecute(self, obj):
        ''' convert the json data to "inputParameters" structure '''

        solverProperties = copy.deepcopy(self.nodeData["WebGui"]["formData"])

        fields = {}
        residualControl = {}
        relaxationFactors = dict(fields={}, equations={})
        for child in obj.Group:
            field = child.Name.replace("fvSol_", "")
            ch_fd = copy.deepcopy(child.Proxy.nodeData["WebGui"]["formData"])
            if "relaxationFactors" in ch_fd:
                if "fields" in ch_fd["relaxationFactors"]:
                    relaxationFactors["fields"][field] = ch_fd["relaxationFactors"]["fields"]
                if "equations" in ch_fd["relaxationFactors"]:
                    relaxationFactors["equations"][field] = ch_fd["relaxationFactors"]["equations"]
                ch_fd.pop("relaxationFactors")

            if "residualControl" in ch_fd:
                residualControl[field] = ch_fd["residualControl"]
                ch_fd.pop("residualControl")
                solverProperties["residualControl"] = residualControl


            fields[field] = ch_fd


        return dict(fields=fields, solverProperties=solverProperties, relaxationFactors=relaxationFactors)

    def executeToGui(self, obj, parameters):
        ''' import the "input_parameters" data into the json obj data '''
        fields = copy.deepcopy(parameters["fields"])
        solverProperties = copy.deepcopy(parameters["solverProperties"])
        relaxationFactors = copy.deepcopy(parameters["relaxationFactors"])


        for child in obj.Group:
            ch_fd = dict()

            field = child.Name.replace("fvSol_", "")
            if field in fields:
                ch_fd = fields[field]
                if len(relaxationFactors) > 0:
                    ch_rlx_fctr = dict(fields=None, equations=None)
                    ch_rlx_fctr["fields"] = relaxationFactors["fields"][field]
                    ch_rlx_fctr["equations"] = relaxationFactors["equations"][field]
                    ch_fd["relaxationFactors"] = copy.deepcopy(ch_rlx_fctr)
                if "residualControl" in solverProperties:
                    ch_fd["residualControl"] = solverProperties["residualControl"][field]

            child.Proxy.nodeData["WebGui"]["formData"] = copy.deepcopy(ch_fd)
            child.Proxy.selectNode(child)

        solverProperties.pop("residualControl")
        self.nodeData["WebGui"]["formData"] = solverProperties
        self.selectNode(obj)


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
                fv_name = "fvSol_" + field
                nodeData = copy.deepcopy(self.nodeData["fields"]["template_webGui"])
                nodeData["WebGui"]["Schema"]["title"] = fv_name
                fvSolField_obj = HermesNode.makeNode(fv_name, obj, str(0), nodeData)

        # remove fields from webGui
        for field in del_list:
            for objField in obj.Group:
                if field in objField.Label:
                    obj.Document.removeObject(objField.Name)