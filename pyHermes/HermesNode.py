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

#-----------------------------------------------------------------------#
# This enables us to open a dialog on the left with a click of a button #
#-----------------------------------------------------------------------#

# =============================================================================
# Wizard Left-over (start)
# =============================================================================
#Path To Wizard UI
#path_to_wizard_ui = FreeCAD.getResourceDir() + "Mod/Hermes/Resources/ui/wizard.ui"
#path_to_bc_wizard_ui = FreeCAD.getResourceDir() + "Mod/Hermes/Resources/ui/bcdialog.ui"



# Json Wizard Dialog
class CJsonWizardPanel:
    
        
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^__init__ start ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    def __init__(self):           
        #Create widget from ui file
        self.form = FreeCADGui.PySideUic.loadUi(path_to_wizard_ui)
        
        self.jsonObject = ''

        #Connect Widgets' Buttons
        #self.form.m_pOpenB.clicked.connect(self.browseJsonFile)
        self.form.m_pSaveB.clicked.connect(self.saveJsonFile)
        #self.form.m_pList.currentRowChanged.connect(self.rowChanged)
#^^^^^^^^^^^^^^^^^^^^^^^^^^^__init__ end^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    
    def setJsonObject(self, jsonObject):
        self.jsonObject = jsonObject
        
#^^^^^^^^^^^^^^^^^^^^^^^^^^ saveJsonFile start ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^       
    def saveJsonFile(self):
        #Open Tk window
        root = tkinter.Tk()

        #Hide Tkinter window
        root.withdraw()

        #Get current working directory
        sCurrDir = os.getcwd()

        #Open FileBrowser
        sSaveFileName = filedialog.asksaveasfilename(parent=root, initialdir=sCurrDir, title='Please select a file to save workflows json into')

        #Nothing Selected
        if len(sSaveFileName) <= 0:
            return
        
        #TODO: save jsonString to file
        
        #save file to the selected place
        with open(sSaveFileName, "w") as write_file:
            json.dump(self.jsonObject, write_file)
            
        return
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^ saveJsonFile end ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^       
        
        #Extract nodes from json as if we have just read it
 #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ accept start ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^       
    def accept(self):
        #Close Dialog
        FreeCADGui.Control.closeDialog()        
 #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ accept end ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^       
# =============================================================================
# Wizard Left-over (end)
# =============================================================================


def makeNode(name, workflowObj, nodeId):
    """ Create a Hermes Node object """
    obj = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroupPython", name)
#    obj = FreeCAD.ActiveDocument.addObject("App::FeaturePython", name)

    _HermesNode(obj, workflowObj, nodeId)

    if FreeCAD.GuiUp:
        _ViewProviderNode(obj.ViewObject)
    return obj

# =============================================================================
# #CommandNode Class
# =============================================================================
class _CommandHermesNode:
    """ HermesNode command definition """

    def GetResources(self):
        icon_path = FreeCAD.getResourceDir() + "Mod/Hermes/Resources/icons/hermes.png"
        return {'Pixmap': icon_path,
                'MenuText': QtCore.QT_TRANSLATE_NOOP("Hermes_Workflow", "Hermes Workflow"),
                'ToolTip': QtCore.QT_TRANSLATE_NOOP("Hermes_Workflow", "Creates new Hermes Workflow")}

    def IsActive(self):
#        return CfdTools.getActiveAnalysis() is not None
        return FreeCAD.ActiveDocument is not None

    def Activated(self):
#        FreeCAD.ActiveDocument.openTransaction("Choose appropriate Node model")
#        isPresent = False
#        members = CfdTools.getActiveAnalysis().Group
#        for i in members:
#            if isinstance(i.Proxy, _CfdPhysicsModel):
#                FreeCADGui.activeDocument().setEdit(i.Name)
#                isPresent = True
        

        # Allow to re-create if deleted
#        if not isPresent:
#            FreeCADGui.doCommand("")
#            FreeCADGui.addModule("CfdPhysicsSelection")
#            FreeCADGui.addModule("CfdTools")
#            FreeCADGui.doCommand(
#                "CfdTools.getActiveAnalysis().addObject(CfdPhysicsSelection.makeCfdPhysicsSelection())")
#            FreeCADGui.ActiveDocument.setEdit(FreeCAD.ActiveDocument.ActiveObject.Name)
        pass


#if FreeCAD.GuiUp:
#    FreeCADGui.addCommand('Cfd_PhysicsModel', _CommandCfdPhysicsSelection())
        
    
# =============================================================================
# Hermes Node class
# =============================================================================
class _HermesNode:
    """ The Hermes Node """
    def __init__(self, obj, workflowObj, SnodeId):
        obj.Proxy = self
        self.Type = "HermesNode"
        self.nodeId = SnodeId
        self.workflowObjName = workflowObj.Name
#        obj.NodeId = SnodeId
        self.initProperties(obj)
#        self.obj = obj
        
        

    def initProperties(self, obj):
        addObjectProperty(obj, "Type", ['Global', 'Script'], "App::PropertyEnumeration", "Node Type", "Type of node")
        addObjectProperty(obj, "NodeId", "-1", "App::PropertyString", "Node Id", "Id of node",4) # the '4' hide the property
        
        #link to other object property
        workflowObj=FreeCAD.ActiveDocument.getObject(self.workflowObjName)
        addObjectProperty(obj, "OtherParents", None, "App::PropertyLinkGlobal", "Links", "Link to")


        obj.NodeId = self.nodeId

        #addObjectProperty(obj, "NodeCount", "", "App::PropertyPath", "", "Path to workflow JSON File")
        #addObjectProperty(obj, "IsActiveWorkflow", False, "App::PropertyBool", "", "Active hermes workflow object in document")        
        obj.setEditorMode("Type", 1)  # Make read-only (2 = hidden)
#        obj.setEditorMode("NodeId", 2)  #(2 = hidden)
        
        #get workflowObj by name
        workflowObj=FreeCAD.ActiveDocument.getObject(self.workflowObjName)

        #create name of wanted node(str)
        node = 'node' + obj.NodeId
        
        #get node data
        nodeData = workflowObj.Proxy.JsonObject[node]
        #get node List of properties
        ListProperties=nodeData["Properties"]
        
        for x in ListProperties:
            propertyNum=ListProperties[x]
            
            prop=propertyNum["prop"]
            init_val=propertyNum["init_val"]
            Type=propertyNum["type"]
            Heading=propertyNum["Heading"]
            tooltip=propertyNum["tooltip"]
            #get current value from Json
            current_val = propertyNum["current_val"]
            
            #add Object Property
            addObjectProperty(obj,prop,init_val,Type,Heading,tooltip) 
            #Update the Object Property current value from json
            setattr(obj, prop, current_val)
            

    def onDocumentRestored(self, obj):
        self.initProperties(obj)
        
    def changeLabel(self):
#        FreeCAD.Console.PrintMessage("\nChange Label\n") 
        return
    
    def doubleClickedNode(self,obj):
        workflowObj=FreeCAD.ActiveDocument.getObject(self.workflowObjName)
#        workflowObj.Proxy.selectNode(obj,obj.NodeId)
        workflowObj.Proxy.selectNode(workflowObj,obj.NodeId)

        #FreeCAD.Console.PrintMessage("\ndoubleClicked\n")
        return
    
# =============================================================================
#      "_ViewProviderNode" class
# =============================================================================
class _ViewProviderNode:
    """ A View Provider for the Hermes Node container object. """
    def __init__(self, vobj):
        vobj.Proxy = self


    def getIcon(self):
        icon_path = FreeCAD.getResourceDir() + "Mod/Hermes/Resources/icons/hermes.png"
        return icon_path

    def attach(self, vobj):
        self.ViewObject = vobj
#        self.Object = vobj.Object
        self.bubbles = None
        

    def updateData(self, obj, prop):
        #We get here when the object of HermesWorkflow changes
        #For this moment, we consider only the JSONFile parameter
        
        #Check if the JSONFile parameter changed and its not empty path
        if (str(prop) == 'Label' and len(str(obj.Label)) > 0):
            obj.Proxy.changeLabel()
            return
        
#        FreeCAD.Console.PrintMessage('Prop:' + str(prop) + '\n')
#        FreeCAD.getDocument("Unnamed").getObject("Temp001")
        

#    def onChanged(self,obj, vobj, prop):
    def onChanged(self,obj, prop):

        if (str(prop) == 'Label' and len(str(obj.Label)) > 0):
            obj.Proxy.changeLabel()
            return
#        return

    def doubleClicked(self, vobj):
        vobj.Object.Proxy.doubleClickedNode(vobj.Object)
        

    def __getstate__(self):
        
#        FreeCAD.Console.PrintMessage("n/__getstate__Node/n") 
        return None

    def __setstate__(self, state):
#        FreeCAD.Console.PrintMessage("n/__setstate__Node/n") 
        return None


#---------------------------------------------------------------------------
# =============================================================================
#      "TestCmd" class   
# =============================================================================
class TestCmd: 
    """Opens a Qt dialog with all inserted unit tests"""
    def Activated(self):
        import QtUnitGui
        QtUnitGui.addTest("TestApp.All")
        QtUnitGui.setTest("TestApp.All")
        QtUnitGui.addTest("BaseTests")
        QtUnitGui.addTest("UnitTests")
        QtUnitGui.addTest("Document")
        QtUnitGui.addTest("UnicodeTests")
        QtUnitGui.addTest("MeshTestsApp")
        QtUnitGui.addTest("TestFem")
        QtUnitGui.addTest("TestSketcherApp")
        QtUnitGui.addTest("TestPartApp")
        QtUnitGui.addTest("TestPartDesignApp")
        QtUnitGui.addTest("TestPartDesignGui")
        QtUnitGui.addTest("TestPathApp")
        QtUnitGui.addTest("TestSpreadsheet")
        QtUnitGui.addTest("TestDraft")
        QtUnitGui.addTest("TestArch")
        QtUnitGui.addTest("TestTechDrawApp")
        QtUnitGui.addTest("Workbench")
        QtUnitGui.addTest("Menu")
        QtUnitGui.addTest("Menu.MenuDeleteCases")
        QtUnitGui.addTest("Menu.MenuCreateCases")

    def GetResources(self):
        return {'MenuText': 'Self-test...', 'ToolTip': 'Runs a self-test to check if the application works properly'}

#---------------------------------------------------------------------------
class TestAllCmd: 
    "Test all commando object"
    def Activated(self):
        import QtUnitGui
        QtUnitGui.addTest("TestApp.All")
        QtUnitGui.setTest("TestApp.All")

    def GetResources(self):
        return {'Pixmap'  : 'Std_Tool1', 'MenuText': 'Test all', 'ToolTip': 'Runs all tests at once (can take very long!)'}

#---------------------------------------------------------------------------
class TestDocCmd: 
    "Document test commando object"
    def Activated(self):
        import QtUnitGui
        QtUnitGui.addTest("Document")
        QtUnitGui.setTest("Document")

    def GetResources(self):
        return {'Pixmap'  : 'Std_Tool1', 'MenuText': 'Test Document', 'ToolTip' : 'Test the document (creation, save, load and destruction)'}

#---------------------------------------------------------------------------
class TestAllTextCmd: 
    "Test all commando object"
    def Activated(self):
        import unittest, TestApp
        unittest.TextTestRunner(stream=sys.stdout,verbosity=2).run(unittest.defaultTestLoader.loadTestsFromName("TestApp.All"))

    def GetResources(self):
        return {'Pixmap'  : 'Std_Tool1', 'MenuText': 'Test all', 'ToolTip' : 'Runs all tests at once (can take very long!)'}

#---------------------------------------------------------------------------
class TestDocTextCmd: 
    "Document test commando object"
    def Activated(self):
        TestApp.TestText("Document")

    def GetResources(self):
        return {'Pixmap'  : 'Std_Tool1', 'MenuText': 'Test Document', 'ToolTip' : 'Test the document (creation, save, load and destruction)'}

#---------------------------------------------------------------------------
class TestBaseTextCmd: 
    "Base test commando object"
    def Activated(self):
        TestApp.TestText("BaseTests")

    def GetResources(self):
        return {'Pixmap'  : 'Std_Tool1', 'MenuText': 'Test base', 'ToolTip' : 'Test the basic functions of FreeCAD'}

#---------------------------------------------------------------------------
class TestWorkbenchCmd: 
    "Workbench test"
    def Activated(self):
        i=0
        while (i<20):
            FreeCADGui.activateWorkbench("MeshWorkbench")
            FreeCADGui.updateGui()
            FreeCADGui.activateWorkbench("NoneWorkbench")
            FreeCADGui.updateGui()
            FreeCADGui.activateWorkbench("PartWorkbench")
            FreeCADGui.updateGui()
            print(i)
            i=i+1
        FreeCADGui.activateWorkbench("TestWorkbench")

    def GetResources(self):
        return {'Pixmap'  : 'Std_Tool1', 'MenuText': 'Test workbench', 'ToolTip' : 'Test the switching of workbenches in FreeCAD'}

#---------------------------------------------------------------------------
class TestCreateMenuCmd: 
    "Base test commando object"
    def Activated(self):
        TestApp.TestText("Menu.MenuCreateCases")

    def GetResources(self):
        return {'Pixmap'  : 'Std_Tool1', 'MenuText': 'Add menu', 'ToolTip' : 'Test the menu stuff of FreeCAD'}

#---------------------------------------------------------------------------
class TestDeleteMenuCmd: 
    "Base test commando object"
    def Activated(self):
        TestApp.TestText("Menu.MenuDeleteCases")

    def GetResources(self):
        return {'Pixmap'  : 'Std_Tool1', 'MenuText': 'Remove menu', 'ToolTip' : 'Test the menu stuff of FreeCAD'}

#---------------------------------------------------------------------------
class TestInsertFeatureCmd: 
    "Base test commando object"
    def Activated(self):
        if FreeCAD.activeDocument() != None:
            FreeCAD.activeDocument().addObject("App::FeatureTest")
        else:
            FreeCAD.PrintMessage("No active document.\n")

    def GetResources(self):
        return {'Pixmap'  : 'Std_Tool1', 'MenuText': 'Insert a TestFeauture', 'ToolTip' : 'Insert a TestFeature in the active Document'}

#---------------------------------------------------------------------------
# Adds the commands to the FreeCAD command manager
#---------------------------------------------------------------------------
FreeCADGui.addCommand('CreateWorkflow'        , _CommandCreateHermesWorkflow())
FreeCADGui.addCommand('Test_Test'        ,TestCmd())
FreeCADGui.addCommand('Test_TestAllText' ,TestAllTextCmd())
FreeCADGui.addCommand('Test_TestDocText' ,TestDocTextCmd())
FreeCADGui.addCommand('Test_TestBaseText',TestBaseTextCmd())
FreeCADGui.addCommand('Test_TestAll'     ,TestAllCmd())
FreeCADGui.addCommand('Test_TestDoc'     ,TestDocCmd())
FreeCADGui.addCommand('Test_TestWork'    ,TestWorkbenchCmd())
FreeCADGui.addCommand('Test_TestCreateMenu'    ,TestCreateMenuCmd())
FreeCADGui.addCommand('Test_TestDeleteMenu'    ,TestDeleteMenuCmd())
FreeCADGui.addCommand('Test_InsertFeature'    ,TestInsertFeatureCmd())

#jsonWizard1 = CJsonWizardPanel()
#FreeCADGui.Control.showDialog(jsonWizard1)
#Path To Wizard UI

#FreeCADGui.getMainWindow().setCentralWidget(FreeCADGui.PySideUic.loadUi(path_to_ui))


