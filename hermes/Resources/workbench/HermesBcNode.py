# FreeCAD Part module
# (c) 2001 Juergen Riegel
#
# Part design module

#***************************************************************************
#*   (c) Juergen Riegel (juergen.riegel@web.de) 2002                       *
#*                                                                         *
#*   This file is part of the FreeCAD CAx development system.              *
#*                                                                         *
#*   This program is free software; you can redistribute it and/or modify  *
#*   it under the terms of the GNU Lesser General Public License (LGPL)    *
#*   as published by the Free Software Foundation; either version 2 of     *
#*   the License, or (at your option) any later version.                   *
#*   for detail see the LICENCE text file.                                 *
#*                                                                         *
#*   FreeCAD is distributed in the hope that it will be useful,            *
#*   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
#*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
#*   GNU Library General Public License for more details.                  *
#*                                                                         *
#*   You should have received a copy of the GNU Library General Public     *
#*   License along with FreeCAD; if not, write to the Free Software        *
#*   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
#*   USA                                                                   *
#*                                                                         *
#*   Juergen Riegel 2002                                                   *
#***************************************************************************/

# import FreeCAD modules
import FreeCAD,FreeCADGui, WebGui
import HermesTools
from HermesTools import addObjectProperty
# import the App Test module
import TestApp               #Test as Module name not possible
import sys
from PyQt5 import QtGui,QtCore

import tkinter
from tkinter import filedialog
import os
import os.path

if FreeCAD.GuiUp:
    import FreeCADGui
    from PySide import QtCore

import json
import string
import pydoc
import copy

import HermesGui
import HermesNode
import CfdFaceSelectWidget


# -----------------------------------------------------------------------#
# This enables us to open a dialog on the left with a click of a button #
# -----------------------------------------------------------------------#

# *****************************************************************************
# -----------**************************************************----------------
#                          #CBCDialogPanel start
# -----------**************************************************----------------
# *****************************************************************************

# Path To bc UI
path_to_bc_ui = FreeCAD.getResourceDir() + "Mod/Hermes/Resources/ui/bcdialog.ui"


class CBCDialogPanel:

    def __init__(self, obj):
        # Create widget from ui file
        self.form = FreeCADGui.PySideUic.loadUi(path_to_bc_ui)

        # Connect Widgets' Buttons
        # self.form.m_pOpenB.clicked.connect(self.browseJsonFile)

        #        self.BCObjName=obj.Name

        # Face list selection panel - modifies obj.References passed to it
        self.faceSelector = CfdFaceSelectWidget.CfdFaceSelectWidget(self.form.m_pFaceSelectWidget,
                                                                    obj, True, False)

    def addBC(self, bcType):
        # add  bcType to options at BC dialog
        self.form.m_pBCTypeCB.addItem(bcType)

    def setCurrentBC(self, BCName):
        # update the current value in the comboBox
        self.form.m_pBCTypeCB.setCurrentText(BCName)

    def setCallingObject(self, callingObjName):
        # get obj Name, so in def 'accept' can call the obj
        self.callingObjName = callingObjName

    def readOnlytype(self):
        # update the 'type' list to 'read only' - unChangeable
        self.form.m_pBCTypeCB.setEnabled(0)

    def accept(self):
        # Happen when Close Dialog
        # get the curren BC type name from Dialog
        BCtype = self.form.m_pBCTypeCB.currentText()

        # calling the nodeObj from name
        callingObject = FreeCAD.ActiveDocument.getObject(self.callingObjName)

        # calling the function that create the new BC Object
        callingObject.Proxy.bcDialogClosed(callingObject, BCtype)

        # close the Dialog in FreeCAD
        FreeCADGui.Control.closeDialog()
        self.faceSelector.closing()

    def reject(self):
        self.faceSelector.closing()
        return True


# *****************************************************************************
# -----------**************************************************----------------
#                          #CBCDialogPanel end
# -----------**************************************************----------------
# *****************************************************************************


#
# *****************************************************************************
# -----------**************************************************----------------
#                                   #BC module start
# -----------**************************************************----------------
# *****************************************************************************

def makeBCNode(name, TypeList, BCNodeData, Nodeobj):
    """ Create a Hermes BC object """

    #    # Object with option to have children
    #    obj = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroupPython", name)

    # Object can not have children
    obj = FreeCAD.ActiveDocument.addObject("App::FeaturePython", name)
    #print ("HermesBCNode make BC node\n")


    # add BCNodeobj(obj) as child of Nodeobj
    Nodeobj.addObject(obj)

    # initialize propeties and so at the new BC obj
    _HermesBC(obj, TypeList, BCNodeData)

    if FreeCAD.GuiUp:
        _ViewProviderBC(obj.ViewObject)
    return obj

# ======================================================================
class _CommandHermesBcNodeSelection:
    """ CFD physics selection command definition """

    def GetResources(self):
        icon_path = FreeCAD.getResourceDir() + "Mod/Hermes/Resources/icons/BCNode2.png"
        return {'Pixmap': icon_path,
                'MenuText': QtCore.QT_TRANSLATE_NOOP("Hermes_BC_Node", "Hermes BC Node"),
                'ToolTip': QtCore.QT_TRANSLATE_NOOP("Hermes_BC_Node", "Creates new Hermes BC Node")}

    def IsActive(self):
        return HermesTools.getActiveHermes() is not None

    def Activated(self):
        FreeCAD.ActiveDocument.openTransaction("Choose appropriate BC Node")
        isPresent = False
        members = HermesTools.getActiveHermes().Group
        for i in members:
            if isinstance(i.Proxy, _CfdPhysicsModel):
                FreeCADGui.activeDocument().setEdit(i.Name)
                isPresent = True

        # Allow to re-create if deleted
        if not isPresent:
            FreeCADGui.doCommand("")
            FreeCADGui.addModule("HermesBcNode")
            FreeCADGui.addModule("HermesTools")
            FreeCADGui.doCommand(
                "HermesTools.getActiveHermes().addObject(HermesBcNode.makeBCNode())")
            FreeCADGui.ActiveDocument.setEdit(FreeCAD.ActiveDocument.ActiveObject.Name)


if FreeCAD.GuiUp:
    FreeCADGui.addCommand('Hermes_BcNode', _CommandHermesBcNodeSelection())

# ======================================================================


# =============================================================================
# Hermes BC class
# =============================================================================
class _HermesBC:
    """ The Hermes BC """

    def __init__(self, obj, TypeList, BCNodeData):

        obj.Proxy = self

        self.TypeList = TypeList
        self.BCNodeData = BCNodeData
        self.initProperties(obj)

    def initProperties(self, obj):

        # ^^^ Constant properties ^^^

        # References property - keeping the faces and part data attached to the BC obj
        addObjectProperty(obj, 'References', [], "App::PropertyPythonObject", "", "Boundary faces")

        # link property - link to other object (beside parent)
        addObjectProperty(obj, "OtherParents", None, "App::PropertyLinkGlobal", "Links", "Link to")

        # Active property- keep if obj has been activated (douuble clicked get active)
        addObjectProperty(obj, "IsActiveBC", False, "App::PropertyBool", "", "Active heraccept object in document")

        # BCNodeDataString property - keep the json BC node data as a string
        addObjectProperty(obj, "BCNodeDataString", "-1", "App::PropertyString", "BCNodeData", "Data of the node", 4)

        # Type property - list of all BC types
        addObjectProperty(obj, "Type", self.TypeList, "App::PropertyEnumeration", "BC Type",
                          "Type of Boundry Condition")
        obj.setEditorMode("Type", 1)  # Make read-only (2 = hidden)

        # Update Values at the properties from BCNodeData
        obj.Type = self.BCNodeData["Type"]
        obj.Label = self.BCNodeData["Name"]  # automatically created with object.
        obj.BCNodeDataString = json.dumps(self.BCNodeData)  # convert from json to string

        #  ^^^^^ Properties from Json  ^^^

        # get BC node List of properties from 'nodeData'
        ListProperties = self.BCNodeData["Properties"]

        # Create each property from the list
        for x in ListProperties:
            # get property'num' object ; num =1,2,3 ...
            propertyNum = ListProperties[x]

            # get needed parameters to create a property
            prop = propertyNum["prop"]
            init_val = propertyNum["init_val"]
            Type = propertyNum["type"]
            Heading = propertyNum["Heading"]
            tooltip = propertyNum["tooltip"]

            # add Object's Property
            addObjectProperty(obj, prop, init_val, Type, Heading, tooltip)

    def UpdateFacesInJson(self, obj):

        # get workflowObj
        Nodeobj = obj.getParentGroup()
        workflowObj = Nodeobj.getParentGroup()

        # get Export path from workflowObj
        dirPath = workflowObj.ExportJSONFile

        # Create basic structure of a part object
        Part_strc = {
            "Name": "",
            "Path": "",
            "faces": []
        }

        # create list the will contain all part Objects
        # add tmp part obj to ListPartObj
        ListPartObj = [];

        # Loop all the References in the object
        for Ref in obj.References:
            # example Refernces structure : obj.References=[('Cube','Face1'),('Cube','Face2')]
            # example Ref structure :Ref=('Cube','Face1')

            # get Name and face from Corrent Reference
            PartName = Ref[0]  # givenPartName
            PartFace = Ref[1]  # face

            # Loop all ListPartObj -
            nPartIndex = -1
            nIndex = 0
            for PartObj in ListPartObj:
                # check if Object exist in list
                if PartName == PartObj['Name']:
                    # save part index in list
                    nPartIndex = nIndex
                    break
                nIndex = nIndex + 1

            # if Part not exists in ListPartObj - create a new part obj and add it to the ListPartObj
            if (nPartIndex == -1):

                # update Part_strc Name
                Part_strc['Name'] = PartName

                # update Part_strc Path
                Part_strc['Path'] = dirPath + '/'

                # update Part_strc face list
                Part_strc['faces'] = [PartFace]

                # add part obj to ListPartObj
                mydata = copy.deepcopy(Part_strc)
                ListPartObj.append(mydata)

            # update face list of the part
            else:
                # add the face to part's face list
                ListPartObj[nPartIndex]['faces'].append(PartFace)

        # Create basic structure of a facelist (string) in the length of ListPartObj
        # structure example:
        # -- "faceList":{
        # --     "Part1":{ },
        # --     "Part2":{ },
        # --     "Part3":{ }
        # --  }

        x = 1
        faceListStr = "{"
        for PartObj in ListPartObj:
            if (x > 1):
                faceListStr += ','
            partStr = '"Part' + str(x) + '":{}'
            faceListStr += partStr
            x = x + 1
        faceListStr += "}"

        # create Hermesworkflow obj to allow caliing def "ExportPart"
        Nodeobj = obj.getParentGroup()
        workflowObj = Nodeobj.getParentGroup()

        # convert structure from string to json
        faceList = json.loads(faceListStr)

        # loop all part objects in ListPartObj
        for y in range(len(ListPartObj)):
            # get PartObj from the ListPartObj
            PartObj = ListPartObj[y]

            # Create Part'Node' ; Node =1,2,3 ...
            PartNode = 'Part' + str(y + 1)

            # update the PartObj data at the current PartNode in faceList
            faceList[PartNode] = PartObj

            workflowObj.Proxy.ExportPart(obj, str(PartObj['Name']))

        # Update faceList attach to the BC at the BCnodeData
        self.BCNodeData["faceList"] = faceList

        # update Label in Json
        self.BCNodeData["Name"] = obj.Label

        # Update BCnodeData  at the BCNodeDataString by converting from json to string
        self.BCNodeDataString = json.dumps(self.BCNodeData)
        return

    def initFacesFromJson(self, obj):

        # get faceList attach to the BC from BCnodeData
        faceList = self.BCNodeData["faceList"]

        # create Hermesworkflow obj to allow caliing def "loadPart"
        Nodeobj = obj.getParentGroup()
        workflowObj = Nodeobj.getParentGroup()

        for x in faceList:
            # get the partnum  from facelist (in case more then 1 part attach to the BC)
            # property'num' ; num =1,2,3 ...
            partnum = faceList[x]

            # get Name and path of the part , and list of faces attach to the part
            PartName = partnum["Name"]
            PartPath = partnum["Path"]
            PartFaces = partnum["faces"]

            # Create full path of the part for Import
            pathPartStr = PartPath + PartName + ".stp"

            # Call 'loadPart' from 'hermesWorkflow' to load part
            givenPartName = workflowObj.Proxy.loadPart(workflowObj, pathPartStr)

            # ToDo: Check if this line is needed
            if len(givenPartName) == 0:
                continue

            # update the Reference(faces) list attach to the the BCObj -
            for face in PartFaces:
                tmp = (givenPartName, face)  # Reference structure
                obj.References.append(tmp)

        return

    def setCurrentPropertyBC(self, obj, ListProperties):
        # update the current value of all properties' BC object
        for x in ListProperties:
            # get property'num' object ; num =1,2,3 ...
            propertyNum = ListProperties[x]

            # get the prop parameter
            prop = propertyNum["prop"]

            # get the prop current_val
            current_val = propertyNum["current_val"]

            # get the current_val at the prop
            setattr(obj, prop, current_val)

    def onDocumentRestored(self, obj):
        # when restored- initilaize properties
        self.initProperties(obj)

        if FreeCAD.GuiUp:
            _ViewProviderBC(obj.ViewObject)

    def doubleClickedBCNode(self, obj):

        # create CBCDialogPanel Object
        bcDialog = CBCDialogPanel(obj)

        # get NodeObj to get nodeData
        NodeObj = obj.getParentGroup()

        # get BC type list from nodeDate - *in case not 'readonly'* have list of BCtypes
        BCTypes = NodeObj.Proxy.nodeData["BCTypes"]
        TypeList = BCTypes["TypeList"]

        # add the Bc types to options at BC dialog
        for types in TypeList:
            bcDialog.addBC(types)

        # update the first value to be showen in the comboBox
        bcDialog.setCurrentBC(obj.Type)

        # set read only BC type
        bcDialog.readOnlytype()

        # add node Object name to the bcDialog name - used when "accept"
        bcDialog.setCallingObject(obj.Name)

        # show the Dialog in FreeCAD
        FreeCADGui.Control.showDialog(bcDialog)

        return

    def bcDialogClosed(self, callingObject, BCtype):
        # todo: is needed?
        pass

    def UpdateBCNodePropertiesData(self, obj):
        # update the properties in the "BCnodeData"
        # use this func before exporting Json

        # get node List of properties
        ListProperties = self.BCNodeData["Properties"]

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
        self.BCNodeData["Properties"] = ListProperties

        # Update BCnodeData  at the BCNodeDataString by converting from json to string
        obj.BCNodeDataString = json.dumps(self.BCNodeData)

        return


# =============================================================================
#      "_ViewProviderNode" class
# =============================================================================
class _ViewProviderBC:
    """ A View Provider for the Hermes BC Node container object. """

    # =============================================================================
    #     General interface for all visual stuff in FreeCAD This class is used to
    #     generate and handle all around visualizing and presenting BC objects from
    #     the FreeCAD App layer to the user.
    # =============================================================================

    def __init__(self, vobj):
        vobj.Proxy = self
        self.BCNodeType = vobj.Object.Type

    def getIcon(self):
        icon_path = FreeCAD.getResourceDir() + "Mod/Hermes/Resources/icons/BCNode2.png"

        return icon_path

    def attach(self, vobj):
        self.ViewObject = vobj
        self.bubbles = None

    def updateData(self, obj, prop):
        # We get here when the object of BC Node changes
        return

    def onChanged(self, obj, prop):
        return

    def doubleClicked(self, vobj):
        vobj.Object.Proxy.doubleClickedBCNode(vobj.Object)
        return

    def __getstate__(self):
        return

    def __setstate__(self, state):
        return None

# *****************************************************************************
# -----------**************************************************----------------
#                                   #BC module end
# -----------**************************************************----------------
# *****************************************************************************
#
