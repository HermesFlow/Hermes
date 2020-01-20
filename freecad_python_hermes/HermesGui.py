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

import json
import string

import CfdFaceSelectWidget
import Part
import copy
import pydoc





#-----------------------------------------------------------------------#
# This enables us to open a dialog on the left with a click of a button #
#-----------------------------------------------------------------------#

# *****************************************************************************
# -----------**************************************************----------------
#                          #CBCDialogPanel start
# -----------**************************************************----------------
# *****************************************************************************

#Path To bc UI
path_to_bc_ui = FreeCAD.getResourceDir() + "Mod/Hermes/Resources/ui/bcdialog.ui"

class CBCDialogPanel:

    def __init__(self,obj):           
        #Create widget from ui file
        self.form = FreeCADGui.PySideUic.loadUi(path_to_bc_ui)
        
        #Connect Widgets' Buttons 
        #self.form.m_pOpenB.clicked.connect(self.browseJsonFile)
        
#        self.BCObjName=obj.Name
        
        # Face list selection panel - modifies obj.References passed to it
        self.faceSelector = CfdFaceSelectWidget.CfdFaceSelectWidget(self.form.m_pFaceSelectWidget,
                                                                    obj, True, False)
    
    def addBC(self, bcType):
        #add  bcType to options at BC dialog
        self.form.m_pBCTypeCB.addItem(bcType)
        
    def setCurrentBC(self, BCName):
        #update the current value in the comboBox
        self.form.m_pBCTypeCB.setCurrentText(BCName)
   
    def setCallingObject(self, callingObjName):
        #get obj Name, so in def 'accept' can call the obj
        self.callingObjName = callingObjName
    
    def readOnlytype(self):
        #update the 'type' list to 'read only' - unChangeable
        self.form.m_pBCTypeCB.setEnabled(0)
        
    def accept(self):
        #Happen when Close Dialog
        #get the curren BC type name from Dialog
        BCtype = self.form.m_pBCTypeCB.currentText()
        
        #calling the nodeObj from name
        callingObject = FreeCAD.ActiveDocument.getObject(self.callingObjName)
        
        #calling the function that create the new BC Object
        callingObject.Proxy.bcDialogClosed(callingObject,BCtype)
        
        #close the Dialog in FreeCAD
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
 
def makeBCNode(name,TypeList,BCNodeData,Nodeobj):
    """ Create a Hermes BC object """
    
#    # Object with option to have children
#    obj = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroupPython", name)
    
    # Object can not have children
    obj = FreeCAD.ActiveDocument.addObject("App::FeaturePython", name)
    
    
    #add BCNodeobj(obj) as child of Nodeobj
    Nodeobj.addObject(obj)
    
    #initialize propeties and so at the new BC obj
    _HermesBC(obj,TypeList,BCNodeData)


    if FreeCAD.GuiUp:
        _ViewProviderBC(obj.ViewObject)
    return obj
# =============================================================================
# Hermes BC class
# =============================================================================
class _HermesBC:
    """ The Hermes BC """
    def __init__(self,obj,TypeList,BCNodeData):

        obj.Proxy = self
        
        self.TypeList=TypeList
        self.BCNodeData=BCNodeData
        self.initProperties(obj)

    def initProperties(self, obj):
        
      #^^^ Constant properties ^^^  
      
        #References property - keeping the faces and part data attached to the BC obj
        addObjectProperty(obj, 'References', [], "App::PropertyPythonObject", "", "Boundary faces")
      
        #link property - link to other object (beside parent)
        addObjectProperty(obj, "OtherParents", None, "App::PropertyLinkGlobal", "Links", "Link to")
        
        #Active property- keep if obj has been activated (douuble clicked get active)
        addObjectProperty(obj, "IsActiveBC", False, "App::PropertyBool", "", "Active heraccept object in document")        
        
        #BCNodeDataString property - keep the json BC node data as a string
        addObjectProperty(obj, "BCNodeDataString", "-1" , "App::PropertyString", "BCNodeData", "Data of the node",4)
        
      
        #Type property - list of all BC types
        addObjectProperty(obj, "Type", self.TypeList, "App::PropertyEnumeration", "BC Type", "Type of Boundry Condition")
        obj.setEditorMode("Type", 1)  # Make read-only (2 = hidden)
        
        #Update Values at the properties from BCNodeData
        obj.Type=self.BCNodeData["Type"]
        obj.Label=self.BCNodeData["Name"] #automatically created with object.
        obj.BCNodeDataString=json.dumps(self.BCNodeData) # convert from json to string

      #  ^^^^^ Properties from Json  ^^^
      
        #get BC node List of properties from 'nodeData'
        ListProperties=self.BCNodeData["Properties"]
        
        #Create each property from the list
        for x in ListProperties:
            
            #get property'num' object ; num =1,2,3 ...
            propertyNum=ListProperties[x]
            
            #get needed parameters to create a property
            prop=propertyNum["prop"]
            init_val=propertyNum["init_val"]
            Type=propertyNum["type"]
            Heading=propertyNum["Heading"]
            tooltip=propertyNum["tooltip"]
        
            #add Object's Property
            addObjectProperty(obj,prop,init_val,Type,Heading,tooltip)
            
    def UpdateFacesInJson(self, obj):
        
        
        
        #get workflowObj
        Nodeobj=obj.getParentGroup()
        workflowObj=Nodeobj.getParentGroup()
        
        #get Export path from workflowObj
        dirPath=workflowObj.ExportJSONFile

        #Create basic structure of a part object
        Part_strc={
                "Name":"",
                "Path":"",
                "faces":[]
                }
        
        #create list the will contain all part Objects 
        #add tmp part obj to ListPartObj
        ListPartObj=[];

        # Loop all the References in the object
        for Ref in obj.References:
            #example Refernces structure : obj.References=[('Cube','Face1'),('Cube','Face2')]
            #example Ref structure :Ref=('Cube','Face1')

            
            #get Name and face from Corrent Reference
            PartName=Ref[0] #givenPartName
            PartFace=Ref[1] #face
            
            #Loop all ListPartObj - 
            nPartIndex=-1
            nIndex=0
            for PartObj in ListPartObj:
                #check if Object exist in list
                if  PartName == PartObj['Name']:
                    #save part index in list
                    nPartIndex=nIndex
                    break
                nIndex=nIndex+1
         
            #if Part not exists in ListPartObj - create a new part obj and add it to the ListPartObj       
            if (nPartIndex==-1):     
            
                #update Part_strc Name
                Part_strc['Name']=PartName
                
                #update Part_strc Path               
                Part_strc['Path']=dirPath+'/'
                
                #update Part_strc face list
                Part_strc['faces']=[PartFace]
                                
                #add part obj to ListPartObj
                mydata=copy.deepcopy(Part_strc)
                ListPartObj.append(mydata)
                  
            #update face list of the part
            else:
                #add the face to part's face list
                ListPartObj[nPartIndex]['faces'].append(PartFace)
        
        #Create basic structure of a facelist (string) in the length of ListPartObj
        #structure example:
        #-- "faceList":{  
        #--     "Part1":{ },
        #--     "Part2":{ },        
        #--     "Part3":{ }
        #--  }
        
        x=1
        faceListStr = "{"
        for PartObj in ListPartObj:
            if (x > 1):    
                faceListStr += ',' 
            partStr = '"Part' + str(x) + '":{}'
            faceListStr += partStr
            x = x + 1
        faceListStr += "}"
        
        #create Hermesworkflow obj to allow caliing def "ExportPart"
        Nodeobj=obj.getParentGroup()
        workflowObj=Nodeobj.getParentGroup()  
        
        #convert structure from string to json 
        faceList= json.loads(faceListStr)
        
        #loop all part objects in ListPartObj
        for y in range(len(ListPartObj)):
            
            #get PartObj from the ListPartObj
            PartObj=ListPartObj[y]
            
            #Create Part'Node' ; Node =1,2,3 ...
            PartNode = 'Part' + str(y+1)
            
            #update the PartObj data at the current PartNode in faceList
            faceList[PartNode] = PartObj
            
            workflowObj.Proxy.ExportPart(obj,str(PartObj['Name']))
        
        #Update faceList attach to the BC at the BCnodeData
        self.BCNodeData["faceList"]=faceList
        
        # update Label in Json
        self.BCNodeData["Name"]=obj.Label
        
        #Update BCnodeData  at the BCNodeDataString by converting from json to string
        self.BCNodeDataString=json.dumps(self.BCNodeData)
        return
        
    def initFacesFromJson(self, obj):
        
        #get faceList attach to the BC from BCnodeData
        faceList=self.BCNodeData["faceList"]
        
        #create Hermesworkflow obj to allow caliing def "loadPart"
        Nodeobj=obj.getParentGroup()
        workflowObj=Nodeobj.getParentGroup()
        
        for x in faceList:
            #get the partnum  from facelist (in case more then 1 part attach to the BC)
            #property'num' ; num =1,2,3 ...
            partnum=faceList[x]
            
            #get Name and path of the part , and list of faces attach to the part
            PartName=partnum["Name"]
            PartPath=partnum["Path"]
            PartFaces=partnum["faces"]
            
            #Create full path of the part for Import
            pathPartStr= PartPath + PartName +".stp"
            
            #Call 'loadPart' from 'hermesWorkflow' to load part
            givenPartName = workflowObj.Proxy.loadPart(workflowObj,pathPartStr)
            
            #ToDo: Check if this line is needed
            if len(givenPartName) ==0: 
                continue

            #update the Reference(faces) list attach to the the BCObj - 
            for face in PartFaces:
                tmp=(givenPartName,face) # Reference structure
                obj.References.append(tmp)
        
        return

        
    def setCurrentPropertyBC(self, obj,ListProperties):
    #update the current value of all properties' BC object    
        for x in ListProperties:
            
            #get property'num' object ; num =1,2,3 ...
            propertyNum=ListProperties[x]
            
            #get the prop parameter
            prop=propertyNum["prop"]
            
            #get the prop current_val
            current_val = propertyNum["current_val"]
            
            #get the current_val at the prop
            setattr(obj, prop, current_val)


    def onDocumentRestored(self, obj):
        #when restored- initilaize properties
        self.initProperties(obj)
        
        if FreeCAD.GuiUp:
            _ViewProviderBC(obj.ViewObject)
        
    
    def doubleClickedBCNode(self,obj):
        
        #create CBCDialogPanel Object
        bcDialog = CBCDialogPanel(obj)
        
        #get NodeObj to get nodeData
        NodeObj=obj.getParentGroup()
        
        #get BC type list from nodeDate - *in case not 'readonly'* have list of BCtypes
        BCTypes=NodeObj.Proxy.nodeData["BCTypes"]
        TypeList = BCTypes["TypeList"]
        
        #add the Bc types to options at BC dialog
        for types in TypeList:
            bcDialog.addBC(types)
            
        # update the first value to be showen in the comboBox
        bcDialog.setCurrentBC(obj.Type)
         
        #set read only BC type
        bcDialog.readOnlytype()
        
        #add node Object name to the bcDialog name - used when "accept"
        bcDialog.setCallingObject(obj.Name)
        
        #show the Dialog in FreeCAD
        FreeCADGui.Control.showDialog(bcDialog)
        
        return
    
    def bcDialogClosed(self, callingObject,BCtype):
        #todo: is needed?
        pass
    
    def UpdateBCNodePropertiesData(self,obj):
        #update the properties in the "BCnodeData"
        #use this func before exporting Json
        
        #get node List of properties
        ListProperties=self.BCNodeData["Properties"]
        
        for y in ListProperties:
            
            #get property'num' object ; num =1,2,3 ...    
            propertyNum=ListProperties[y]
            
            #get the prop parameter
            prop=propertyNum["prop"]

            #get the Object Property current value from property object
            current_val=getattr(obj, prop)
                                
            #update the value at the propertyNum[prop]
            if type(current_val) is not int and type(current_val) is not float and type(current_val) is not list:
            #In case of 'Quantity property' (velocity,length etc.), 'current_val' need to be export as a string
                propertyNum["current_val"]=str(current_val)

            else:
                propertyNum["current_val"]=current_val

            #update propertyNum in ListProperties
            ListProperties[y]=propertyNum
            
        #update ListProperties in nodeData
        self.BCNodeData["Properties"]=ListProperties
        
        #Update BCnodeData  at the BCNodeDataString by converting from json to string
        obj.BCNodeDataString=json.dumps(self.BCNodeData)

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
        self.BCNodeType=vobj.Object.Type

    def getIcon(self):
        
        icon_path = FreeCAD.getResourceDir() + "Mod/Hermes/Resources/icons/BCNode2.png"

        return icon_path
    

    def attach(self, vobj):
        self.ViewObject = vobj
        self.bubbles = None
        

    def updateData(self, obj, prop):
        #We get here when the object of BC Node changes
        return
        
    def onChanged(self,obj, prop):
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
# 
# 
#
#        
#        
#        
#        
#        
#
        
    
    
    
    
    
    
    
    
    
    
    

 
# *****************************************************************************
# -----------**************************************************----------------
#                                   #Node module start
# -----------**************************************************----------------
# *****************************************************************************
 
def makeNode(name, workflowObj, nodeId,nodeData):
    """ Create a Hermes Node object """
 
    test = pydoc.locate('HermesGui._HermesNode')
    if test is None:
        FreeCAD.Console.PrintMessage("Not found\n")
    
    # Object with option to have children
    obj = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroupPython", name)
    
#    # Object can not have children   
#    obj = FreeCAD.ActiveDocument.addObject("App::FeaturePython", name)
    
    #add Nodeobj(obj) as child of workflowObj
    workflowObj.addObject(obj)
    
    #----------------dynamic find class--------------------
      
    #find the class of the node from the its type
    nodecls=pydoc.locate("HermesGui."+nodeData["TypeFC"])
    
#    # if the class is not exist, create a new class
#    if nodecls is None:
#        nodecls = pydoc.locate("HermesGui.%s" % nodeData["TypeFC"])
    
    #call to the class
    if nodecls is not None:
        nodecls(obj, nodeId,nodeData,name)  
    
     #----------------static find class------------------
# =============================================================================
#     if nodeData["TypeFC"]=="webGui":
#         _WebGuiNode(obj, nodeId,nodeData,name)  
#     elif nodeData["TypeFC"]=="BC":
#         _BCFactory(obj, nodeId,nodeData,name)
#     else:
#         _HermesNode(obj, nodeId,nodeData,name)
# =============================================================================
            
        obj.Proxy.initializeFromJson(obj)

        if FreeCAD.GuiUp:
            _ViewProviderNode(obj.ViewObject)
    return obj

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
    def __init__(self, obj, nodeId,nodeData,name):

        obj.Proxy = self
        self.nodeId = nodeId
        self.nodeData=nodeData
        self.name=name
        self.initProperties(obj)
        
        
    def initializeFromJson(self, obj):

        #get list of properties from nodeData          
        NodeProperties = self.nodeData["Properties"]
        
        #update the current value of all properties in  node object 
        for x in NodeProperties:
            
            #get property'num' object ; num =1,2,3 ...
            propertyNum=NodeProperties[x]
            
            #get the prop parameter
            prop=propertyNum["prop"]
            
            #get the prop current_val
            current_val = propertyNum["current_val"]
            
            
            #get the current_val at the prop
            setattr(obj, prop, current_val)
        
        # additional properties RunOsCommand node
        if self.name=="RunOsCommand":
            
            #get the choosen methon
            method=getattr(obj,"ChooseMethod")
            
            #make read only the property that hasnt been choosen
            if method=="Commands list":
                obj.setEditorMode("batchFile", 1)  # Make read-only
            elif method=="batchFile":
                obj.setEditorMode("Commands", 1)  # Make read-only
                
        

    def initProperties(self, obj):
             
      #^^^ Constant properties ^^^  
      
        #References property - keeping the faces and part data attached to the BC obj
        addObjectProperty(obj, 'References', [], "App::PropertyPythonObject", "", "Boundary faces")

        # Node Id
        #Todo- is necessary?
        addObjectProperty(obj, "NodeId", "-1", "App::PropertyString", "Node Id", "Id of node",4) # the '4' hide the property
        
        #Type of the Object - (web/BC)
        addObjectProperty(obj, "Type", "-1" , "App::PropertyString", "Node Type", "Type of node")
        obj.setEditorMode("Type", 1)  # Make read-only (2 = hidden)
        
        #Is Avtive property- Boolean -keep if obj has been activated (douuble clicked get active)
        addObjectProperty(obj, "IsActiveNode", False, "App::PropertyBool", "", "Active Node object in document") 
        obj.setEditorMode("IsActiveNode", 1)  # Make read-only (2 = hidden)
        
        #link property - link to other object (beside parent)
        addObjectProperty(obj, "linkToOtherObjects", [], "App::PropertyLinkList", "Links", "Link to")
        
        #NodeDataString property - keep the json  node data as a string        
        addObjectProperty(obj, "NodeDataString", "-1" , "App::PropertyString", "NodeData", "Data of the node",4)
        
        #Exportile property- get the directory path of where we want to export our files
        addObjectProperty(obj, "ExportNodeJSONFile", "", "App::PropertyPath", "IO", "Path to save Node JSON File")
        
       
                

        

        #Update Values at the properties from nodeData
        obj.NodeId = self.nodeId
        nodeType=self.nodeData["TypeFC"]
        obj.Type=nodeType
        obj.Label=self.name #automatically created with object.
        obj.setEditorMode("Label", 1)  # Make read-only 
        obj.NodeDataString=json.dumps(self.nodeData) # convert from json to string


      #^^^^^ Properties from Json  ^^^

        #get Web node List of properties
        ListProperties=self.nodeData["Properties"]
        
        #Create each property from the list
        for x in ListProperties:
            
            #get property'num' ; num =1,2,3 ...
            propertyNum=ListProperties[x]
            
            #get needed parameters to create a property
            prop=propertyNum["prop"]
            init_val=propertyNum["init_val"]
            Type=propertyNum["type"]
            Heading=propertyNum["Heading"]
            tooltip=propertyNum["tooltip"]
            
            
            #add Object's Property
            addObjectProperty(obj,prop,init_val,Type,Heading,tooltip) 
            
            
        
    def onDocumentRestored(self, obj):
        
        workflowObj=obj.getParentGroup()
        workflowObj.Proxy.nLastNodeId="-1"
        
        #parse json data        
        self.nodeData = json.loads(obj.NodeDataString)
        
        #when restored- initilaize properties
        self.initProperties(obj)
                
        FreeCAD.Console.PrintMessage("Node onDocumentRestored\n")
        
        if FreeCAD.GuiUp:
            _ViewProviderNode(obj.ViewObject)
            

    
    #just an example - not used    
    def changeLabel(self):
#        FreeCAD.Console.PrintMessage("\nChange Label\n") 
        return
    
    def doubleClickedNode(self,obj):
        
        #get "workflowObj" from been parent of the node obj
        workflowObj=obj.getParentGroup()
        
        #backup last node and update "nLastNodeId" in Hermes workflow
        workflowObj.Proxy.updateLastNode(workflowObj,obj.NodeId)
        
        #update is active
        obj.IsActiveNode=True

        return
    
    def backupNodeData(self, obj):
        pass

        
    
    def UpdateNodePropertiesData(self,obj):
        #update the properties in the "nodeData"
        #use this func before exporting Json
        
        #get node List of properties
        ListProperties=self.nodeData["Properties"]
        
        for y in ListProperties:
            
            #get property'num' object ; num =1,2,3 ...
            propertyNum=ListProperties[y]
            
            #get the prop parameter
            prop=propertyNum["prop"]

            #get the Object Property current value from property object
            current_val=getattr(obj, prop)
                                
            #update the value at the propertyNum[prop]
            if type(current_val) is not int and type(current_val) is not float and type(current_val) is not list:
            #In case of 'Quantity property' (velocity,length etc.), 'current_val' need to be export as a string
                propertyNum["current_val"]=str(current_val)

            else:
                propertyNum["current_val"]=current_val

            #update propertyNum in ListProperties
            ListProperties[y]=propertyNum

        #update ListProperties in nodeData
        self.nodeData["Properties"]=ListProperties
        
        #Update nodeData  at the NodeDataString by converting from json to string
        obj.NodeDataString=json.dumps(self.nodeData)

        return
    
    def RemoveNodeObj(self,obj):
        #remove NodeObj Children
        #use when importing new json file
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
        if self.NodeObjType == "_WebGuiNode":
            icon_path = FreeCAD.getResourceDir() + "Mod/Hermes/Resources/icons/Web.png"
        elif self.NodeObjType == "_BCFactory":
            icon_path = FreeCAD.getResourceDir() + "Mod/Hermes/Resources/icons/BCfactory.png"
        else:
            icon_path = FreeCAD.getResourceDir() + "Mod/Hermes/Resources/icons/NewNode.png"


        return icon_path

    def attach(self, vobj):
        self.ViewObject = vobj
#        self.Object = vobj.Object
        self.bubbles = None

    def updateData(self, obj, prop):
        #We get here when the object of Node changes
        
        #Check if the JSONFile parameter changed and its not empty path
# =============================================================================
#         #not in use, just an example
#         if (str(prop) == 'Label' and len(str(obj.Label)) > 0):
#             obj.Proxy.changeLabel()
#             return
# =============================================================================
        
        if (str(prop) == 'ExportNodeJSONFile' and len(str(obj.ExportNodeJSONFile)) > 0):
            #get "workflowObj" from been parent of the node obj
            workflowObj=obj.getParentGroup()
            workflowObj.Proxy.saveJson(workflowObj,obj.ExportNodeJSONFile,obj.Name,obj.Label)
            obj.ExportNodeJSONFile = ''
        
        #----------------------------------------------------------------------------------
        
        # edit properties RunOsCommand node
        if str(prop)=="ChooseMethod" and obj.Name=="RunOsCommand":
            
            #get the choosen methon
            method=getattr(obj,"ChooseMethod")
            
            #make read only the property that hasnt been choosen, and read/write the one been choose
            if method=="Commands list":
                obj.setEditorMode("batchFile", 1)  # Make read-only
                obj.setEditorMode("Commands", 0)  # read/write

                
            elif method=="batchFile":
                obj.setEditorMode("Commands", 1)  # Make read-only
                obj.setEditorMode("batchFile", 0)  # read/write

        

#    def onChanged(self,obj, vobj, prop):
    def onChanged(self,obj, prop):
        #not it use, just an example
        if (str(prop) == 'Label' and len(str(obj.Label)) > 0):
            obj.Proxy.changeLabel()
            return
        


    def doubleClicked(self, vobj):
        vobj.Object.Proxy.doubleClickedNode(vobj.Object)        

    def __getstate__(self):
            
        #Create NodeObj using Object name
        NodeObj=FreeCAD.ActiveDocument.getObject(self.NodeObjName)
        
        #if node has been active - backup
        if NodeObj.IsActiveNode:
            NodeObj.Proxy.backupNodeData(NodeObj)
        
        #get the last updated NodeDataString
        getNodeString = NodeObj.NodeDataString
        
        #return an array with NodeObj name and the updated NodeDataString - 
        # it will be recieved by "__setstate__" when opening the project
        return [self.NodeObjName, getNodeString]
        

    def __setstate__(self, state):
                
#    #state - recieved from 'getstate', while saving the project "Hermesworkflow"
#        type :array ,including 2 variebelles, 
#             state[0]= Name of the Node Object
#             state[1]= nodeDataString - the last uppdated Json string before saving.
        
        NodeObjName = state[0]
        nodeDataString = state[1]
        
        #get Object using OBject name
        NodeObj=FreeCAD.ActiveDocument.getObject(NodeObjName)
        
        #update the nodeDataString at the NodeObj
        NodeObj.NodeDataString = nodeDataString
        
        return None
    
# =============================================================================
# #_WebGuiNode
# =============================================================================
class _WebGuiNode(_HermesNode):
#    super().funcName(var1,var,2..) - allow to use the function of the Parent, 
#    and add current class functionalites
    
    def __init__(self,obj,nodeId,nodeData,name):
        super().__init__(obj,nodeId,nodeData,name)

    def doubleClickedNode(self,obj):
        super().doubleClickedNode(obj)
        
        self.selectNode(obj)
        

        
    def selectNode(self,obj):
        
        #get node WebGui- Scheme,uiScheme,FormData
        nodeWebGUI=self.nodeData["WebGui"]
        
        #Check if webGui is empty
        if not((len(nodeWebGUI)==0)):
            

            #define web address & pararmeters
            path = FreeCAD.getResourceDir() + 'Mod/Hermes/Resources/jsonReactWebGui.html?parameters='
            address='file:///'+path
        
            #str JSON 'nodeWebGUI' using "dumps"
            parameters=json.dumps(nodeWebGUI)

            #open the jsonReact html page using the following command
            browser = WebGui.openSingleBrowser(address+parameters)
            sRegName = '0,' + self.name;
            browser.registerHandler(sRegName)
            
        
        return  

    def process(self, data):
        UpdateWebGUI = data;
#        FreeCAD.Console.PrintMessage("WebGUI Process Data\n" + str(data)) 
        
        if (0==len(UpdateWebGUI)):
            return

        #parse the 'UpdateWebGUI'
        UpdateWebGUIJson= json.loads(UpdateWebGUI)
        
        #update in our global json data the updated parsed 'WebGUI'
        #first update the node
        self.nodeData["WebGui"]=UpdateWebGUIJson

#        formData=UpdateWebGUIJson["formData"]
#        FreeCAD.Console.PrintMessage("----------------------------------------------------------------\n") 
#        FreeCAD.Console.PrintMessage("backup--nodedata.webgui['formData']="+str(formData)+"\n") 
        

        
 
    def backupNodeData(self,obj): 
        #backup the data of the last node pressed
        super().backupNodeData(obj)
        
        
        #then Update nodeData  at the NodeDataString by converting from json to string
        obj.NodeDataString=json.dumps(self.nodeData)
        

        
# =============================================================================
# #_BCFactory
# =============================================================================
class _BCFactory(_HermesNode):
#    super().funcName(var1,var,2..) - allow to use the function of the Parent, 
#    and add current class functionalites
   
    def __init__(self,obj, nodeId,nodeData,name):
        super().__init__(obj, nodeId,nodeData,name)

    def initializeFromJson(self, obj):
        super().initializeFromJson(obj)
       
        #get BCtypes section from json
        BCTypes=self.nodeData["BCTypes"]
        
        # get the list of available Bc types from BCtypes section
        TypeList=BCTypes["TypeList"]
        
        # get the list of BC that has been saved
        BCList=self.nodeData["BCList"]       
         
        #Loop all the BC that has been saved
        for y in BCList:
            
            #get BC'num' object ; num =1,2,3 ...
            BCnum=BCList[y]
             
            #get Name,Type and Properties of the BC
            BCName = BCnum["Name"]
            BCType = BCnum["Type"]
            
            #Create the BC node       
            BCNodeObj=makeBCNode('BCtemp',TypeList,BCnum,obj)

            #get the BC properties, and update their current value
            BCProperties=BCnum["Properties"]
            BCNodeObj.Proxy.setCurrentPropertyBC(BCNodeObj,BCProperties)
            
            #Update the faces attach to the BC (alsp create the parts)
            BCNodeObj.Proxy.initFacesFromJson(BCNodeObj)
            
            #get Bc Name and update his Label property
            BCName = BCnum["Name"]
            BCNodeObj.Label=BCName
            
            #get Bc type and update his Type property
            BCType = BCnum["Type"] 
            BCNodeObj.Type=BCType
            
        
    def doubleClickedNode(self,obj):
        super().doubleClickedNode(obj)
        
        #create CBCDialogPanel Object
        bcDialog = CBCDialogPanel(obj)
        
        #get BCtypes section from json
        BCTypes=self.nodeData["BCTypes"]
        
        # get the list of available Bc types from BCtypes section
        TypeList = BCTypes["TypeList"]
        
        #add the Bc types to options at BC dialog
        for types in TypeList:
            bcDialog.addBC(types)
        
        # update the first value to be showen in the comboBox
        bcDialog.setCurrentBC(types[0])
        
        #add node Object name to the bcDialog name
        bcDialog.setCallingObject(obj.Name)
        
        #show the Dialog in FreeCAD
        FreeCADGui.Control.showDialog(bcDialog)
        
     
    def backupNodeData(self,obj):
        super().backupNodeData(obj)
        #Update faceList in BCList section to each BC node
        for child in obj.Group:
            child.Proxy.UpdateFacesInJson(child)
        pass
    
        
    def UpdateNodePropertiesData(self,obj):
        super().UpdateNodePropertiesData(obj)
        
        #in case amount of BC has been changed
        #Create basic structure of a BCList (string) in the length of Children's obj amount
        #structure example:
        #-- "BCList":{  
        #--     "BC1":{ },
        #--     "BC2":{ },        
        #--     "BC3":{ }
        #--  }
        x=1
        BCListStr = "{"
        for child in obj.Group:
            if (x > 1):
                BCListStr += ','
            childStr = '"BC' + str(x) + '":{}'
            BCListStr += childStr
            x = x + 1
        BCListStr += "}"
            
        
        #convert structure from string to json 
        BCList= json.loads(BCListStr)
        
        #loop all BC objects in Nodeobj
        x = 1
        for child in obj.Group:
            
            #update current properties value of the BC-child
            child.Proxy.UpdateBCNodePropertiesData(child)
            
            #get BC-child nodeDate from BCNodeDataString property
            BCnodeData=json.loads(child.BCNodeDataString)
            
            #get BC'node' object ; node =1,2,3 ...            
            BCnode = 'BC' + str(x)
            
            #update the BC-child nodeDate in the BCList section
            BCList[BCnode] = BCnodeData
            
            x=x+1
        
        #update the BCList section data in nodeData
        self.nodeData['BCList']=BCList
            
        #Update nodeData  at the NodeDataString by converting from json to string    
        obj.NodeDataString=json.dumps(self.nodeData)

        #update properties of the current node(before updated only the children) 
        super().UpdateNodePropertiesData(obj)
        return
            
  
    def bcDialogClosed(self,obj,BCtype):
        #call when created new BC node
        
        #Create basic structure of a BCNodeData
        BCNodeData={
                "Name":"",
                "Type":"",
                "Properties":{}
                }
        
        #get the BC Type available from Json, and their list of properties
        BCTypes=self.nodeData["BCTypes"]
        TypeList=BCTypes["TypeList"]
        TypeProperties = BCTypes["TypeProperties"]
        
        #take the properties of the choosen BCtype from dialog
        BCJsonType = TypeProperties[BCtype]
        BCProperties=BCJsonType["Properties"]
        
        #update values in BCNodeData structure
        BCNodeData["Name"]=BCtype #meaningful name is thr type
        BCNodeData["Type"]=BCtype
        BCNodeData["Properties"]=BCProperties
        
        #Create the BCObject 
        BCNodeObj=makeBCNode('BCtemp',TypeList,BCNodeData,obj)

        #get the References from the parent node to the the new BC child
        BCNodeObj.References=obj.References
        
        #Empty the parent node References for further use
        obj.References=[]   

        return
    


    
# *****************************************************************************
# -----------**************************************************----------------
#                                   #Node module end
# -----------**************************************************----------------
# *****************************************************************************
#
#        
#        
#        
#        
#        
# 
#        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

# =============================================================================
#     "makeHermesWorkflow" class
# =============================================================================
def makeHermesWorkflow(name):
    """ Create a Hermes Workflow object """
    
#    # Object can not have children   
#    obj = FreeCAD.ActiveDocument.addObject("App::FeaturePython", name)

    # Object with option to have children
    obj = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroupPython", name)
    
    #initialize propeties and so at the Hermes Workflow
    _HermesWorkflow(obj)

    if FreeCAD.GuiUp:
        _ViewProviderHermesWorkflow(obj.ViewObject)
    return obj

# =============================================================================
#  "_HermesWorkflow" class
# =============================================================================
class _HermesWorkflow:
    """ The Hermes Workflow group """
    def __init__(self, obj):
        obj.Proxy = self
        self.Type = "HermesWorkflow"
        self.initProperties(obj)
        
        self.JsonObject = []
        self.JsonObjectfromFile = []
        self.Templates=[]
        self.nLastNodeId="-1"
        self.partPathListFromJson=[]
        self.partNameListFromJson=[]
#        self.partPathExportList=[]
        self.partNameExportList=[]
#        self.ExportPartList=[]
        self.cwd=""
        
        self.importJsonfromfile="importJsonfromfile"
        self.getFromTemplate="Template"

    def initProperties(self, obj):
        
        #ImportJSONFile propert- get the file path of the wanted json file
        addObjectProperty(obj, "ImportJSONFile", "", "App::PropertyFile", "IO", "Browse JSON File")
        
        #ExportJSONFile property- get the directory path of where we want to export our files
        addObjectProperty(obj, "ExportJSONFile", "", "App::PropertyPath", "IO", "Path to save JSON File")
        
        
        #JSONString property - keep the json data as a string
        addObjectProperty(obj, "JSONString", "", "App::PropertyString", "", "JSON Stringify",4)
        
#        #link property - link to other object (beside parent)
#        addObjectProperty(obj, "HermesLink", "", "App::PropertyLink", "", "Link to",4)

        #Active property- keep if obj has been activated (douuble clicked get active)        
        addObjectProperty(obj, "IsActiveWorkflow", False, "App::PropertyBool", "", "Active hermes workflow object in document")       
        
        #make some properties to be 'read-only'
        obj.setEditorMode("IsActiveWorkflow", 1)  # Make read-only (2 = hidden)
        obj.setEditorMode("Group", 1)
        

    def onDocumentRestored(self, obj):
        
        self.nLastNodeId="-1"
        
        #when restored- initilaize properties
        self.initProperties(obj)
        
        FreeCAD.Console.PrintMessage("onDocumentRestored\n")
        
        if FreeCAD.GuiUp:
            _ViewProviderHermesWorkflow(obj.ViewObject)
            
        #parse json data        
#        self.JsonObject = json.loads(obj.JSONString)

              
    def saveJson(self, obj,jsonSaveFilePath,rootVal,FileSaveName):
        
      #^^^Export Json-file
        
        #update JsonString before export
        self.updateJsonBeforeExport(obj)
        
        if rootVal=="null":
            #"To-Do"-change string into null json
            self.JsonObject["root"]=json.loads("null")
        else:
            self.JsonObject["root"]=rootVal
        
#        #get the path of directory want to export
#        jsonSaveFilePath = obj.ExportJSONFile
        
        #get the name of the workflow to set it as the name of json file been export
#        workflowName=obj.Name
        
        
        #define the full path of the export file
        jsonSaveFileName=jsonSaveFilePath+'/'+FileSaveName+'.json'
         
        #get the json want to be export
        dataSave=self.JsonObject 
        
        #save file to the selected place
        with open(jsonSaveFileName, "w") as write_file:
            json.dump(dataSave, write_file, indent=4) #indent make it readable
            
      #^^^Export Part-files
        

        
        doc=obj.Document;
        
        #loop all the objects
        for y in range(len(self.partNameExportList)):
            
            partObjName=self.partNameExportList[y];
            partObj=doc.getObject(partObjName)
               
            #Define full path
            #'stp' file
            fullPath=jsonSaveFilePath+'/' + partObjName + '.stp'
            #'stl' file
            fullPath=jsonSaveFilePath+'/' + partObjName + '.stp'
                
            # export all part Object
            Part.export([partObj],u""+fullPath)
            
        self.partNameExportList=[]
        
        
    def readJson(self, obj):        
        #get json file full path 
        jsonFileName = obj.ImportJSONFile
        self.cwd=os.path.dirname(jsonFileName)
        
        #Open JsonFile , Read & parsed, assign to JsonObject
        self.JsonObjectfromFile=self.loadJsonFromfile(jsonFileName)
        
#        tempJson = self.loadJsonFromfile("/home/noga/Noga/FreeCad/jsonFiles/json.json", "node1.Properties")
#        FreeCAD.Console.PrintMessage("\n")        
#        FreeCAD.Console.PrintMessage(tempJson)
        
        
        #create jsonObject varieble that contain all data, including imported data from files/templates
        self.createJsonObject()
#        self.JsonObject=self.JsonObjectfromFile.copy()
#        FreeCAD.Console.PrintMessage(self.JsonObject)
        
        #assign the data been import to the JSONString property after dumps
        obj.JSONString=json.dumps(self.JsonObject)

        
        #clear the nodes objects
        for child in obj.Group: 
            child.Proxy.RemoveNodeObj(child)
            obj.Document.removeObject(child.Name)
        
        #clear the part Object from json
        if len (self.partPathListFromJson) != 0:
            for x in self.partNameListFromJson:
                obj.Document.removeObject(x)
                
                #clear the part lists
                self.partPathListFromJson=[]
                self.partNameListFromJson=[]
            
        #create node list 
        self.setJson(obj)
        
        #create node objects based on json data
    def createJsonObject(self):
        
        #check if there is a reference to templates file in JsonObjectfromFile
        if "Templates" in self.JsonObjectfromFile:
            
            #Create the Template Json Object - import files if needed
            self.Templates=self.getImportedJson(self.JsonObjectfromFile["Templates"])
            
#            FreeCAD.Console.PrintMessage("Templates="+str(self.Templates)+"\n")
#            FreeCAD.Console.PrintMessage("###################################\n")

            

        #Create JsonObject will contain all the imported date from file/template
        self.JsonObject=self.JsonObjectfromFile
        
        #get the List of nodes , and the 'nodes' from jsonObject 
        nodeList=self.JsonObject["nodeList"]
        nodes=self.JsonObject["nodes"]
        new_nodes={}
        
        #to-do:check option of get the node list from a file
        #Loop the node List, and import external data
        for node in nodeList:
            
            #check if the node from list is in the dictionary list
            if node in nodes:
            
                #get the current node
                currentNode=nodes[node]
            
                #update the data in the nodes from file/templates to concrete data
                updatedCurrentNode=self.getImportedJson(currentNode)
            
                #add the data into 'new_nodes'
                new_nodes[node]=updatedCurrentNode

            
        #update the data in JsonObject to be the new dictionary new_nodes
        self.JsonObject["nodes"]=new_nodes

    
    def getImportedJson(self,jsonObjStruct):
                
         #check if jsonObjStruct is a dictionary
        if type(jsonObjStruct) is not dict:
            return
        
        
        # insert the current jsonStruct to the UpdateJson that will be return after modify
#        UpdatedJsonStruct=jsonObjStruct.copy()
        UpdatedJsonStruct= {}

        
        #to know if it is the first iteration
        i=0
       
        #loop all the keys,values
        for subStructKey,subtructVal in jsonObjStruct.items():
            
            #zero open data vars
            openKeyData={}
            openImportData={}
            
            #in case of import data from file
            if subStructKey==self.importJsonfromfile:
                
                #check if there are list of files that need to be imported, or just 1:
                # list- saved as a dictionary
                # 1 file - saved as keys and values
                # *if*- check if the first value is a dict
                if type(list(subtructVal.values())[0]) is dict:

                    for fileKey,fileVal in subtructVal.items():
                        #call the function that open data
                        openImportData=self.importJsonDataFromFile(fileVal)
                        
#                        FreeCAD.Console.PrintMessage("=====================================\n")
#                        FreeCAD.Console.PrintMessage("openImportData="+str(openImportData)+"\n")
#                        FreeCAD.Console.PrintMessage("=====================================\n")
                        
                        if i>0:
                            #not the first iteration -> overide the data
                            UpdatedJsonStruct=self.overidaDataFunc(openImportData,UpdatedJsonStruct)
                        else:
                            #first iteration -> define the UpdatedJsonStruct as the open data 
                            UpdatedJsonStruct=openImportData.copy()
                        
                        i=i+1
                else:
                
                    #call the function that open data
#                    openImportData=self.checkListOfFiles(subtructVal,'File')
                    openImportData=self.importJsonDataFromFile(subtructVal)
                
                
                    if i>0:
                        #not the first iteration -> overide the data
                        UpdatedJsonStruct=self.overidaDataFunc(openImportData,UpdatedJsonStruct)
                    
                    else:                    
                        #first iteration -> define the UpdatedJsonStruct as the open data 
                        UpdatedJsonStruct=openImportData.copy()


            #in case of import data from Template         
            elif subStructKey==self.getFromTemplate:
                
                #check if there are list of files that need to be imported, or just 1:
                # list- saved as a dictionary
                # 1 file - saved as keys and values
                # *if*- check if the first value is a dict
                if type(list(subtructVal.values())[0]) is dict:

                    for templateKey,templateVal in subtructVal.items():
                        #call the function that open data
                        openImportData=self.importJsonDataFromTemplate(templateVal)
                        
                        if i>0:
                            #not the first iteration -> overide the data
                            UpdatedJsonStruct=self.overidaDataFunc(openImportData,UpdatedJsonStruct)
                        else:
                            #first iteration -> define the UpdatedJsonStruct as the open data 
                            UpdatedJsonStruct=openImportData.copy()
                        
                        i=i+1
                else:
                
                    #call the function that open data
#                    openImportData=self.checkListOfFiles(subtructVal,'Template') 
                    openImportData=self.importJsonDataFromTemplate(subtructVal)
                    
                    
                    if i>0:
                        #not the first iteration -> overide the data
                        UpdatedJsonStruct=self.overidaDataFunc(openImportData,UpdatedJsonStruct)
                    else:
                        #first iteration -> define the UpdatedJsonStruct as the open data 
                        UpdatedJsonStruct=openImportData.copy()
        
            # No imported data from path or Template
            else:
                
                #check if the json substruct is list(in case its items are objects)
                if type(subtructVal) is list:
                            
                    #create an identaty list , that will be updated
                    UpdatedJsonList=subtructVal.copy()
                    
                    # loop all the list items
                    for ind in range(len(subtructVal)):

                        #check each item if its type is a dictionary -
                        if type(subtructVal[ind]) is dict:

                            # call 'getImportedJson' in case there are nested files that need to be imported 
                            UpdatedListItem=self.getImportedJson(subtructVal[ind])

                            #update the updateItem in the main Updated json List
                            UpdatedJsonList[ind]=UpdatedListItem
                
                    #update the list in the json structure
                    UpdatedJsonStruct[subStructKey]=UpdatedJsonList


                #dont apply on values that are not dict - (str/int/doubke etc.) 
                elif type(subtructVal) is dict:
                           
                    # call 'getImportedJson' in case there are nested files that need to be imported 
                    openKeyData=self.getImportedJson(subtructVal)
                    
                    if subStructKey in UpdatedJsonStruct:
                        #not the first iteration -> overide the data                        
                        UpdatedJsonStruct[subStructKey]=self.overidaDataFunc(openKeyData,UpdatedJsonStruct[subStructKey])

                    else:
                        #first iteration -> define the UpdatedJsonStruct as the open data                         
                        UpdatedJsonStruct[subStructKey]=openKeyData.copy()
                
                #any other type-
                #   =if exist - update the dat
                #   =no exist - add it to the structure
                else:
                    UpdatedJsonStruct[subStructKey]=jsonObjStruct[subStructKey]
                    
            i=i+1
            
                        
        return UpdatedJsonStruct
    
    
    def overidaDataFunc(self,overideData,UpdatedJsonStruct):
        
        
#        FreeCAD.Console.PrintMessage("===============Before===============\n")
#        FreeCAD.Console.PrintMessage("UpdatedJsonStruct="+str(UpdatedJsonStruct)+"\n")
 
        
#        if type(overideData) is dict:
        #loop all the overide data
        for dataKey,dataVal in overideData.items():
            
#            FreeCAD.Console.PrintMessage("=====================================\n")
#            FreeCAD.Console.PrintMessage("dataKey="+str(dataKey)+"\n")
#            FreeCAD.Console.PrintMessage("dataVal="+str(dataVal)+"\n")
                
            #check for each key, if exsist in UpdatedJsonStruct
            if dataKey in UpdatedJsonStruct:
                                
                #type is dictionary
                if type(dataVal) is dict:
              
                    #check if 'dataKey' in the structure is empty
                    if len(UpdatedJsonStruct[dataKey])==0:
                        
                        #take all the data in dataVal and insert to 'dataKey' place in the structure
                        UpdatedJsonStruct[dataKey]=dataVal
                
                    #compare the dataVal and structure in dataKey, and update only necessary fields
                    else:
                        

                        #get list of all the intersections of dataVal & UpdatedJsonStruct[dataKey]
                        duptList= UpdatedJsonStruct[dataKey].keys() & dataVal.keys()
                        
                        diffList= dataVal.keys()-UpdatedJsonStruct[dataKey].keys() 

                        

                        
                        #update the UpdatedJsonStruct where there are intersection
                        for dupt in duptList:
                            
                            pathDst=str(dataKey) + '.'+ str(dupt)
                            self.InjectJson(UpdatedJsonStruct,dataVal[dupt],pathDst)
                                #InjectJson(       Dst       ,     Src     ,pathDst): 
                        

                        for diff in diffList:
                            
                            pathDst=str(dataKey) + '.'+ str(diff)
                            self.InjectJson(UpdatedJsonStruct,dataVal[diff],pathDst)
                                #InjectJson(       Dst       ,     Src     ,pathDst):
                                
#                            UpdatedJsonStruct[diff]=dataVal[diff]

                
                #type is 'list'
                elif type(dataVal) is list:
                    
                    #check if 'dataKey' in the structure is empty
                    if len(UpdatedJsonStruct[dataKey])==0:
                        
                        #take all the data in dataVal and insert to 'dataKey' place in the structure
                        UpdatedJsonStruct[dataKey]=dataVal
                    
                    #check it item already exist in structure, if not  add it.
                    else:
                        
                        #loop all items in the list
                        for i in range(len(dataVal)):
                            
                            #if item not in structure list
                            if not(dataVal[i] in UpdatedJsonStruct[dataKey]):
                                
                               #add the item from overide data 
                               UpdatedJsonStruct[dataKey].append(dataVal[i])
                
                #any other type (int,boolean..)
                else:
                    #update its data from overide
                    UpdatedJsonStruct[dataKey]=dataVal
            
            
            #dataKey not exist in UpdatedJsonStruct
            else:
                
                #add to the dictionary
                UpdatedJsonStruct[dataKey]=dataVal

                
        if self.getFromTemplate in UpdatedJsonStruct:
            UpdatedJsonStruct.pop(self.getFromTemplate)
        if self.importJsonfromfile in UpdatedJsonStruct:
            UpdatedJsonStruct.pop(self.importJsonfromfile)

            
#        FreeCAD.Console.PrintMessage("=====================================\n")
#        FreeCAD.Console.PrintMessage("overideData="+str(overideData)+"\n")
#        FreeCAD.Console.PrintMessage("===============After===============\n")
#        FreeCAD.Console.PrintMessage("UpdatedJsonStruct="+str(UpdatedJsonStruct)+"\n") 
        
        return UpdatedJsonStruct
        
        
        
    def checkListOfFiles(self,importData,importFrom):
            
            
            #check if there are list of files that need to be imported, or just 1:
            # list- saved as a dictionary
            # 1 file - saved as keys and values
            # *if*- check if the first value is a dict
            if type(list(importData.values())[0]) is dict:
                    
                #intialized UpdatedJsonStruct
                UpdatedJsonStruct={}
                    
                #loop all files
                for fileKey,fileVal in importData.items():
                    
                    if importFrom == 'File':
                        #update the imported files into UpdatedJsonStruct
                        UpdatedJsonStruct.update(self.importJsonDataFromFile(fileVal))
                    else:
                        UpdatedJsonStruct.update(self.importJsonDataFromTemplate(fileVal))
                            
                
            else:
                if importFrom == 'File':
                    #update the 1 file data into UpdatedJsonStruct
                    UpdatedJsonStruct=self.importJsonDataFromFile(importData)
                else:
                    UpdatedJsonStruct=self.importJsonDataFromTemplate(importData)
                
            return UpdatedJsonStruct
        
    def importJsonDataFromTemplate(self,importTemplate): 
        
        
        #load and recieve the json object from file
        UpdatedJsonStruct=self.Templates[importTemplate["TypeFC"]]
        
        
        #check if there is only a specific field that need to be imported from Template
        if "field" in importTemplate:
            
            #empty data structure - so only relevent data will be returned
            UpdatedJsonStruct={}
            
            # empty var
            fieldData=self.Templates[importTemplate["TypeFC"]]
                    
            # loop all 'field' list 
            for entryPath in importTemplate["field"]:
                
                if (len(entryPath)==0):
                    continue
                
                #split the entry
                splitEntryPath = entryPath.split(".")
                
                #get the entry path wanted data
                for entry in splitEntryPath:
                    fieldData = fieldData[entry]
                
                        
                #add to the UpdatedJsonStruct
                UpdatedJsonStruct.update(fieldData)
                
#        else:
#            UpdatedJsonStruct=self.Templates[importTemplate["TypeFC"]]

                
                
        

        
        return UpdatedJsonStruct
    
    def importJsonDataFromFile(self,importFileData):        
        #----Step 1 : Remember Current Directory----
        
        #define current directory - saved during the recursion
        current_dir=self.cwd
        #update the current work directory
        os.chdir(current_dir)
        #----------------------------------------------------
        
#        FreeCAD.Console.PrintMessage("cwd="+os.getcwd()+"\n") 

        
        #get the path of the file
        pathFile=importFileData["path"]

        #update 'pathFile' to full path- absolute
        pathFile=os.path.abspath(pathFile)

                
        #check if there is only a specific field that need to be imported from file
        if "field" in importFileData:
        
            # empty var
            UpdatedJsonStruct={}
                    
            # loop all 'field' list 
            for entry in importFileData["field"]:
                
#                FreeCAD.Console.PrintMessage("importFileData="+str(importFileData)+"\n")
                #todo - till now only field been taken were dictionaries ,
                #       check possbility of taking ecnries that are not dict-
                #       take the data, create dict struct="key:value", and inject it
                                               
                #get the entry data from the file
                entryData=self.loadJsonFromfile(pathFile,entry)
                
#                FreeCAD.Console.PrintMessage("entryData="+str(entryData)+"\n")
#                FreeCAD.Console.PrintMessage("UpdatedJsonStruct="+str(UpdatedJsonStruct)+"\n")
                        
                #add to the UpdatedJsonStruct
                UpdatedJsonStruct.update(entryData)
                
                #----Step 2 : Change CWD to pathFile Directory----
                
                #get the current full path of the directory's file
                dirname = os.path.dirname(pathFile)                

                #update the current work directory at 'os' and at 'cwd' var
                os.chdir(dirname)
                self.cwd=dirname
                #----------------------------------------------------

                
                # call 'getImportedJson' in case there are nested files that need to be imported 
                UpdatedJsonStruct=self.getImportedJson(UpdatedJsonStruct)

        else:   
 
            #load and recieve the json object from file
            UpdatedJsonStruct=self.loadJsonFromfile(pathFile) 
            
            #----Step 2 : Change CWD to pathFile Directory----
            
            #get the current full path of the directory's file
            dirname = os.path.dirname(pathFile)
                
            #update the current work directory at 'os' and at 'cwd' var
            os.chdir(dirname)
            self.cwd=dirname
            #----------------------------------------------------

                    
                    
            # call 'getImportedJson' in case there are nested files that need to be imported 
            UpdatedJsonStruct=self.getImportedJson(UpdatedJsonStruct)        
            
        
        #---Step 3: Return to previous working directory---
        
        #update the current work directory at 'os' and at 'cwd' var
        os.chdir(current_dir)
        self.cwd=dirname=current_dir
        #----------------------------------------------------

        
        return UpdatedJsonStruct
#            

        

    #to-do:make list of al possible uload files
    
    #done: load files from differenet hirarchy in json - also possible load only a field/list of fields from file
    def InjectJson(self,Dst,Src,pathDst):
        # get the destiny Json var, source Json data ->update the source in the destiny
        #for example:In case data has been upload from a file, and want the update only 1 entry
    
        #split the path into list
        splitPathlist = pathDst.split(".")
        
        #reverse the order of the list
        splitPathlist.reverse()
        
        #Intialize the "data" var with the "Src" data
        data=Src
        
        #loop all the path list
        for x in range(len(splitPathlist)-1):
            #if it is not the last element of the list
            if x != len(splitPathlist)-1:
                
                #take the structure containing the data
                structKey=splitPathlist[x+1]
                struct=Dst[structKey]
                
                #update the data in the structure - splitPathlist[x]-> the key in the strucrure
                struct[splitPathlist[x]]=data

                #update the struct dat in the "data" var - enable to update the data in hierarchy structure
                data=struct
        
        #update the Dst json struct with the data
        #splitPathlist[-1] - the last element of the reverse path list-the highest location in the path hierarchy
        Dst[splitPathlist[-1]]=data   
        
        #return the update Dst json structure
        return Dst
                
        
    
    def loadJsonFromfile(self,filePath, entryInFile = ""):
        
#            cwd = os.getcwd()
#            FreeCAD.Console.PrintMessage("cwd="+cwd+"\n")
            
            
            #Open JsonFile & Read
            with open(filePath, 'r') as myfile:
                data=myfile.read()
                

               
    		#parse data and return it
            dataParsed = json.loads(data)
            
            #No split the 'entryInFile' and get the data from that path
            if (len(entryInFile) == 0):
                return dataParsed
            
            #split the
            splitEntryList = entryInFile.split(".")
            for entry in splitEntryList:
                dataParsed = dataParsed[entry]
                        
            return dataParsed
            
    
    def setJson(self, obj):
        #todo: is needed? why not calling directly to 'updateNodeList'
        self.updateNodeList(obj)
#        self.selectNode(obj,"1")
        
        return
    
    def loadPart(self, obj, partPath):
      
        partIndex = -1
        
        #update 'pathFile' to full path- absolute
        partPath=os.path.abspath(partPath)
        
        #check if part has already been created using his path
        if partPath in self.partPathListFromJson:
            #return the index of the part
            partIndex=self.partPathListFromJson.index(partPath)
            return self.partNameListFromJson[partIndex]
        
        
        # Create New Part #
        
        #Current Object List
        currObjectList = obj.Document.findObjects()
        
        #Curretn Object Amount
        currObjectAmount = len(currObjectList)
        
        #Load Part
        Part.insert(partPath,obj.Document.Name)
        
        #Check new object list
        newObjectList = obj.Document.findObjects()
        
        #Get new object amount
        newObjectAmount = len(newObjectList)
        
        #Check if new part has been loaded by checking amount of Objects
        if (newObjectAmount == currObjectAmount + 1):
            
            #add the new part's name and path to proper ListFromJson
            objectName = newObjectList[currObjectAmount].Name
            self.partPathListFromJson.append(partPath)
            self.partNameListFromJson.append(objectName)
            return objectName
        else:
            return ""
    
    def ExportPart(self,obj,partObjName):
        
        if partObjName in self.partNameExportList:
            return
         
        self.partNameExportList.append(partObjName)
        
        
        
        
# =============================================================================
#     def UpdatePartList(self,obj):
# =============================================================================
        
    
    def updateNodeList(self, obj):


        x=1; 
        nodes=self.JsonObject["nodes"]
        for y in nodes:
            
            #get Node data
            nodeData=nodes[y]
            
            #get node name
            nodename=y     
            
            #Create node obj
            makeNode(nodename, obj, str(x), nodeData)
            x=x+1
   
        return
    
    def updateLastNode(self,obj,nNodeId):
        #backup LastNode data
        
        #loop all children in HermesWorkflow
        for child in obj.Group:
            
            #find the child object that have the same index as 'nLastNodeId'
            if (child.NodeId == self.nLastNodeId):
                
                #backup child 'nodeDate'
                child.Proxy.backupNodeData(child)
                
                #update the node active property to false
                child.IsActiveNode=False
         
        # Update the new 'nLastNodeId'
        self.nLastNodeId=nNodeId

        
    def updateJsonBeforeExport(self,obj):
        
        nodes=self.JsonObject["nodes"]
         #loop all children in HermesWorkflow
        for child in obj.Group:
            
            #back child date
            child.Proxy.backupNodeData(child)
            
            #back child properties
            child.Proxy.UpdateNodePropertiesData(child)
            
            #get child updated nodeData 
            nodaData=json.loads(child.NodeDataString)
            

            nodename=child.Proxy.name
            
#            node = 'node' + child.NodeId
            nodes[nodename]=nodaData
            
        #update the child nodeDate in the JsonObject
        self.JsonObject["nodes"]=nodes

        return
         
      
# =============================================================================
#     "_CommandCreateHermesWorkflow" class
# =============================================================================
class _CommandCreateHermesWorkflow:
    "Create new hermes workflow object"
    def __init__(self):
        pass

    def GetResources(self):
        icon_path = FreeCAD.getResourceDir() + "Mod/Hermes/Resources/icons/hermes.png"
        return {'Pixmap': icon_path,
                'MenuText': QtCore.QT_TRANSLATE_NOOP("Hermes_Workflow", "Hermes Workflow"),
                'ToolTip': QtCore.QT_TRANSLATE_NOOP("Hermes_Workflow", "Creates new Hermes Workflow")}

    def IsActive(self):
        return FreeCAD.ActiveDocument is not None

    def Activated(self):
        FreeCAD.ActiveDocument.openTransaction("Create Hermes Workflow")
        FreeCADGui.doCommand("")
        FreeCADGui.addModule("HermesGui")
        FreeCADGui.addModule("HermesTools")
        FreeCADGui.doCommand("hermes = HermesGui.makeHermesWorkflow('HermesWorkflow1')")
#        return
        FreeCADGui.doCommand("HermesTools.setActiveHermes(hermes)")
        
        #''' Objects ordered according to expected workflow '''
        return

        # Add HermesNode object when HermesGui container is created
        FreeCADGui.addModule("HermesNode")
#        FreeCADGui.doCommand("analysis.addObject(CfdPhysicsSelection.makeCfdPhysicsSelection())")

        # Add fluid properties object when CfdAnalysis container is created
        #FreeCADGui.addModule("CfdFluidMaterial")
        #FreeCADGui.doCommand("analysis.addObject(CfdFluidMaterial.makeCfdFluidMaterial('FluidProperties'))")


# =============================================================================
# "_ViewProviderHermesWorkflow" class
# =============================================================================
class _ViewProviderHermesWorkflow:
    
    """ A View Provider for the Hermes Workflow container object. """
# =============================================================================
#     General interface for all visual stuff in FreeCAD This class is used to 
#     generate and handle all around visualizing and presenting objects from 
#     the FreeCAD App layer to the user.
# =============================================================================
    
    def __init__(self, vobj):
        vobj.Proxy = self
        self.workflowObjName = vobj.Object.Name  

    def getIcon(self):
        icon_path = FreeCAD.getResourceDir() + "Mod/Hermes/Resources/icons/hermes.png"
        return icon_path

    def attach(self, vobj):
        self.ViewObject = vobj
        self.bubbles = None
        

    def updateData(self, obj, prop):
        #We get here when the object of HermesWorkflow changes
        #For this moment, we consider only the JSONFile parameter
        
        #Check if the JSONFile parameter changed and its not empty path
        if (str(prop) == 'ImportJSONFile' and len(str(obj.ImportJSONFile)) > 0):
            obj.Proxy.readJson(obj)
            obj.ImportJSONFile = ''
        if (str(prop) == 'ExportJSONFile' and len(str(obj.ExportJSONFile)) > 0):
            obj.Proxy.saveJson(obj,obj.ExportJSONFile,"null",obj.Label)
            obj.ExportJSONFile = ''

            return
        

    def onChanged(self, vobj, prop):
        #self.makePartTransparent(vobj)
        #CfdTools.setCompSolid(vobj)
        return

    def doubleClicked(self, vobj):
        
        #update Hermes active
        if not HermesTools.getActiveHermes() == vobj.Object:
            if FreeCADGui.activeWorkbench().name() != 'Hermes':
                FreeCADGui.activateWorkbench("Hermes")
            HermesTools.setActiveHermes(vobj.Object)
            return True
        return True
    

    def __getstate__(self):
        return None

    def __setstate__(self, state): 
        return None


#---------------------------------------------------------------------------
# Adds the commands to the FreeCAD command manager
#---------------------------------------------------------------------------
FreeCADGui.addCommand('CreateWorkflow'        , _CommandCreateHermesWorkflow())





