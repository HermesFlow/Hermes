# FreeCAD Part module
# (c) 2001 Juergen Riegel
#
# Part design module

# ***************************************************************************
# *   (c) Juergen Riegel (juergen.riegel@web.de) 2002                       *
# *                                                                         *
# *   This file is part of the FreeCAD CAx development system.              *
# *                                                                         *
# *   This program is free software; you can redistribute it and/or modify  *
# *   it under the terms of the GNU Lesser General Public License (LGPL)    *
# *   as published by the Free Software Foundation; either version 2 of     *
# *   the License, or (at your option) any later version.                   *
# *   for detail see the LICENCE text file.                                 *
# *                                                                         *
# *   FreeCAD is distributed in the hope that it will be useful,            *
# *   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
# *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
# *   GNU Library General Public License for more details.                  *
# *                                                                         *
# *   You should have received a copy of the GNU Library General Public     *
# *   License along with FreeCAD; if not, write to the Free Software        *
# *   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
# *   USA                                                                   *
# *                                                                         *
# *   Juergen Riegel 2002                                                   *
# ***************************************************************************/

# import FreeCAD modules
import FreeCAD, FreeCADGui, WebGui
import HermesTools
from HermesTools import addObjectProperty

import sys
from PyQt5 import QtGui, QtCore

import os
import json
import Part

import HermesNode
from expandJson import expandJson
import HermesPart


# =============================================================================
#     "makeHermesWorkflow" class
# =============================================================================
def makeHermesWorkflow(name):
    """ Create a Hermes Workflow object """

    #    # Object can not have children
    #    obj = FreeCAD.ActiveDocument.addObject("App::FeaturePython", name)

    # Object with option to have children
    obj = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroupPython", name)

    # initialize propeties and so at the Hermes Workflow
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
        self.JsonObjectString = ""
        self.JsonObjectfromFile = []
        self.Templates = []
        self.nLastNodeId = "-1"
        self.partPathListFromJson = []
        self.partNameListFromJson = []
        #        self.partPathExportList=[]
        self.partNameExportList = []
        #        self.ExportPartList=[]
        self.partList = {}

        self.importJsonfromfile = "importJsonfromfile"
        self.getFromTemplate = "Template"

        self.WD_path = ""

    def initProperties(self, obj):

        # ImportJSONFile propert- get the file path of the wanted json file
        addObjectProperty(obj, "ImportJSONFile", "", "App::PropertyFile", "IO", "Browse JSON File")

        # ExportJSONFile property- get the directory path of where we want to export the json file
        addObjectProperty(obj, "ExportJSONFile", "", "App::PropertyPath", "IO", "Path to save JSON File")

        # WorkingDirectory property- get the directory path of where we want to export our files
        addObjectProperty(obj, "WorkingDirectory", "", "App::PropertyPath", "IO", "Path to working directory")

        # JSONString property - keep the json data as a string
        addObjectProperty(obj, "JSONString", "", "App::PropertyString", "", "JSON Stringify", 4)

        #        #link property - link to other object (beside parent)
        #        addObjectProperty(obj, "HermesLink", "", "App::PropertyLink", "", "Link to",4)

        # Active property- keep if obj has been activated (douuble clicked get active)
        addObjectProperty(obj, "IsActiveWorkflow", False, "App::PropertyBool", "",
                          "Active hermes workflow object in document")

        # make some properties to be 'read-only'
        obj.setEditorMode("IsActiveWorkflow", 1)  # Make read-only (2 = hidden)
        obj.setEditorMode("Group", 1)

        # RunWorkflow property - Run the workflow as a basic to luigi if change to true
        addObjectProperty(obj, "RunWorkflow", False, "App::PropertyBool", "Run", "Run the workflow as a basic to luigi")

        # RunLuigi property - Run luigi
        addObjectProperty(obj, "RunLuigi", False, "App::PropertyBool", "Run", "Run luigi")

    def onDocumentRestored(self, obj):

        self.nLastNodeId = "-1"

        # when restored- initilaize properties
        self.initProperties(obj)

        FreeCAD.Console.PrintMessage("onDocumentRestored\n")

        if FreeCAD.GuiUp:
            _ViewProviderHermesWorkflow(obj.ViewObject)

        # parse json data

    #        self.JsonObject = json.loads(obj.JSONString)

    def prepareJsonVar(self, obj, rootVal):

        self.updateJsonBeforeExport(obj)

        if rootVal == "null":
            # "To-Do"-change string into null json
            self.JsonObject["workflow"]["root"] = json.loads("null")
        else:
            self.JsonObject["workflow"]["root"] = rootVal

        self.JsonObjectString = json.dumps(self.JsonObject)

    def saveJson(self, obj, jsonSaveFilePath, FileSaveName):

        # ^^^Export Json-file

        # define the full path of the export file
        jsonSaveFileName = jsonSaveFilePath + '/' + FileSaveName + '.json'

        # get the json want to be export
        dataSave = self.JsonObject

        # save file to the selected place
        with open(jsonSaveFileName, "w") as write_file:
            json.dump(dataSave, write_file, indent=4)  # indent make it readable

        # ^^^Export Part-files

        doc = obj.Document;

        # loop all the objects
        for y in range(len(self.partNameExportList)):
            partObjName = self.partNameExportList[y];
            partObj = doc.getObject(partObjName)

            # Define full path
            # 'stp' file
            fullPath = jsonSaveFilePath + '/' + partObjName + '.stp'
            # 'stl' file
            fullPath = jsonSaveFilePath + '/' + partObjName + '.stp'

            # export all part Object
            Part.export([partObj], u"" + fullPath)

        self.partNameExportList = []

    def readJson(self, obj):
        # get json file full path
        jsonFileName = obj.ImportJSONFile

        # Open JsonFile , Read & parsed, assign to JsonObject
        self.JsonObjectfromFile = expandJson().loadJsonFromfile(jsonFileName)

        # create jsonObject varieble that contain all data, including imported data from files/templates
        self.JsonObject = expandJson().createJsonObject(self.JsonObjectfromFile,jsonFileName)

        # assign the data been import to the JSONString property after dumps
        obj.JSONString = json.dumps(self.JsonObject)
        # FreeCAD.Console.PrintMessage("obj.JSONString="+obj.JSONString+"\n")

        # clear the nodes objects
        for child in obj.Group:
            child.Proxy.RemoveNodeObj(child)
            obj.Document.removeObject(child.Name)

        # clear the part Object from json
        if len(self.partPathListFromJson) != 0:
            for x in self.partNameListFromJson:
                obj.Document.removeObject(x)

                # clear the part lists
                self.partPathListFromJson = []
                self.partNameListFromJson = []

        # create node list
        self.setJson(obj)

        # create node objects based on json data

    def setJson(self, obj):
        # todo: is needed? why not calling directly to 'updateNodeList'
        self.updateNodeList(obj)
        #        self.selectNode(obj,"1")

        return

    def loadPart(self, obj, partPath):

        partIndex = -1

        # check if relative path to Hermes folder
        if partPath.startswith("hermes"):

            # get the path from environment variable
            HermesDirpath = os.getenv('HERMES_2_PATH')

            # update partPath in relative to HermesDirpath
            partPath = HermesDirpath + '/' + partPath

        # update 'pathFile' to full path- absolute
        partPath = os.path.abspath(partPath)


        # check if part has already been created using his path
        if partPath in self.partPathListFromJson:
            # return the index of the part
            partIndex = self.partPathListFromJson.index(partPath)
            return self.partNameListFromJson[partIndex]

        # Create New Part #

        # Current Object List
        currObjectList = obj.Document.findObjects()

        # Curretn Object Amount
        currObjectAmount = len(currObjectList)

        # Load Part
        Part.insert(partPath, obj.Document.Name)

        # Check new object list
        newObjectList = obj.Document.findObjects()

        # Get new object amount
        newObjectAmount = len(newObjectList)

        # add part face and vertices data
        for i in range(newObjectAmount):
            if newObjectList[i].Module == 'Part':
                partName = newObjectList[i].Name
                if partName not in self.partList:
                    self.partList[partName] = HermesPart.HermesPart(partName).getpartDict()


        # Check if new part has been loaded by checking amount of Objects
        if (newObjectAmount == currObjectAmount + 1):

            # add the new part's name and path to proper ListFromJson
            objectName = newObjectList[currObjectAmount].Name
            self.partPathListFromJson.append(partPath)
            self.partNameListFromJson.append(objectName)
            return objectName
        else:
            return ""

    def ExportPart(self, partObjName):

        if partObjName in self.partNameExportList:
            return

        self.partNameExportList.append(partObjName)

    # =============================================================================
    #     def UpdatePartList(self,obj):
    # =============================================================================

    def updateNodeList(self, obj):

        x = 1;
        nodes = self.JsonObject["workflow"]["nodes"]
        for y in nodes:
            # get Node data
            nodeData = nodes[y]

            # get node name
            nodename = y

            # Create node obj
            # makeNode(nodename, obj, str(x), nodeData)
            # FreeCADGui.doCommand("hermes.addObject(HermesNode.makeNode(nodename, obj, str(x), nodeData))")
            HermesNode.makeNode(nodename, obj, str(x), nodeData)

            x = x + 1

        return

    def updateLastNode(self, obj, nNodeId):
        # backup LastNode data

        # loop all children in HermesWorkflow
        for child in obj.Group:

            # find the child object that have the same index as 'nLastNodeId'
            if (child.NodeId == self.nLastNodeId):
                # backup child 'nodeDate'
                child.Proxy.backupNodeData(child)

                # update the node active property to false
                child.IsActiveNode = False

        # Update the new 'nLastNodeId'
        self.nLastNodeId = nNodeId

    def updateJsonBeforeExport(self, obj):

        # loop all children in HermesWorkflow
        for child in obj.Group:
            # back child date
            child.Proxy.backupNodeData(child)

            # back child properties
            child.Proxy.UpdateNodePropertiesData(child)

            # get child updated nodeData
            nodaData = json.loads(child.NodeDataString)

            nodename = child.Proxy.name

            # update the child nodeDate in the JsonObject
            if nodename != 'BlockMesh':
                self.JsonObject["workflow"]["nodes"][nodename]=nodaData


        return

    def RunworkflowCreation(self, obj):

        # save the current work directory before it changed
        currentDirFC = os.getcwd()

        # get the path from environment variable
        HermesDirpath = os.getenv('HERMES_2_PATH')

        # add an Error message in case the environment variable does not exist
        if (HermesDirpath == None):
            FreeCAD.Console.PrintError('Error: HermesGui.py - line 940: The environment variable does not exist!\n')
            return
        current_dir = HermesDirpath

        current_dir = HermesDirpath + '/hermes/'

        # insert the path to sys
        # insert at 1, 0 is the script path (or '' in REPL)
        sys.path.insert(1, current_dir)
        sys.path.insert(1, HermesDirpath)

        # update 'current_dir' to full path- absolute
        current_dir = os.path.abspath(current_dir)

        # update the current work directory
        os.chdir(current_dir)

        # import hermesWorkflow
        from hermes import hermesWorkflow

        # call hermes workflow and keep its result in var
        wf = hermesWorkflow(self.JsonObjectString, self.WD_path, HermesDirpath)

        print(wf)
        print("===================================")

        # save the workflow run result in th WD
        FCtoLuigi_path = self.WD_path + "/FCtoLuigi.py"
        with open(FCtoLuigi_path, "w") as outfile:
            outfile.write(wf.build("luigi"))

        # Create the Luigi command run
        LuigiFile = ''' #!/bin/sh
    
python3 -m luigi --module FCtoLuigi finalnode_xx_0 --local-scheduler 
'''
        # save the file in the working directory
        path = self.WD_path + "/runLuigi.sh"
        with open(path, "w") as fh:
            fh.write(LuigiFile)

        # return the working directory to what it was
        os.chdir(currentDirFC)

    def RunLuigiScript(self):

        import shutil
        import os
        #        os.system("echo HI > /tmp/outputs_path.txt")

        # save the current work directory before it changed
        currentDirFC = os.getcwd()

        # get the path from environment variable
        HermesDirpath = os.getenv('HERMES_2_PATH')
        # print("RunLuigi:HermesDirpath=" + str(HermesDirpath))
        current_dir = HermesDirpath

        # insert the path to sys
        # insert at 1, 0 is the script path (or '' in REPL)
        sys.path.insert(1, current_dir)
        sys.path.insert(1, self.WD_path)
        #
        # update 'current_dir' to full path- absolute
        current_dir = os.path.abspath(current_dir)

        # change directory to the Working directory
        os.chdir(self.WD_path)

        # remove the 'OpenFOAMfiles' in case exist
        shutil.rmtree('OpenFOAMfiles', ignore_errors=True)

        # remove the output folder
        shutil.rmtree(self.WD_path + '/outputs', ignore_errors=True)

        # create a new directory for the LuigiRun output files
        os.mkdir(self.WD_path + "/OpenFOAMfiles")

        # for giving permission
        import stat

        # get the path for the file which run the luigi
        fullPath = self.WD_path + "/runLuigi.sh"

        # give the runLuigi permission of the user
        os.chmod(fullPath, stat.S_IRWXU)

        # run the Luigi batch file
        os.system(fullPath)

        # return the working directory to what it was
        os.chdir(currentDirFC)

    def updateWorkingDirectory(self, path):
        self.WD_path = path


# =============================================================================
#     "_CommandCreateHermesWorkflow" class
# =============================================================================
class _CommandCreateHermesWorkflow:
    "Create new hermes workflow object"

    def __init__(self):
        pass

    def GetResources(self):
        ResourceDir = FreeCAD.getResourceDir() if list(FreeCAD.getResourceDir())[-1] == '/' else FreeCAD.getResourceDir() + "/"
        icon_path = ResourceDir + "Mod/Hermes/Resources/icons/hermes.png"
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
        FreeCADGui.doCommand("HermesTools.setActiveHermes(hermes)")

        ''' Objects ordered according to expected workflow '''
        # return

        # Add HermesNode object when HermesGui container is created
        FreeCADGui.addModule("HermesNode")
        # FreeCADGui.doCommand("hermes.addObject(HermesNode.makeNode())")

        # Add HermesGENode object when HermesGui container is created
        FreeCADGui.addModule("HermesGeometryDefinerNode")

        # Add fluid properties object when CfdAnalysis container is created
        # FreeCADGui.addModule("CfdFluidMaterial")
        # FreeCADGui.doCommand("analysis.addObject(CfdFluidMaterial.makeCfdFluidMaterial('FluidProperties'))")


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
        ResourceDir = FreeCAD.getResourceDir() if list(FreeCAD.getResourceDir())[-1] == '/' else FreeCAD.getResourceDir() + "/"
        icon_path = ResourceDir + "Mod/Hermes/Resources/icons/hermes.png"
        return icon_path

    def attach(self, vobj):
        self.ViewObject = vobj
        self.bubbles = None

    def updateData(self, obj, prop):
        # We get here when the object of HermesWorkflow changes
        # For this moment, we consider only the JSONFile parameter

        # Check if the JSONFile parameter changed and its not empty path
        if (str(prop) == 'ImportJSONFile' and len(str(obj.ImportJSONFile)) > 0):
            obj.Proxy.readJson(obj)
            # seperate file and dir, and define dir as workingDir
            Dirpath = os.path.dirname(obj.ImportJSONFile)
            # update workind directory to self of hermes class
            obj.Proxy.updateWorkingDirectory(Dirpath)
            # update workind directory to the hermes obj
            obj.WorkingDirectory = Dirpath
            obj.ImportJSONFile = ''
        if (str(prop) == 'ExportJSONFile' and len(str(obj.ExportJSONFile)) > 0):
            obj.Proxy.prepareJsonVar(obj, "null")
            obj.Proxy.saveJson(obj, obj.ExportJSONFile, obj.Label)
            obj.ExportJSONFile = ''
        if (str(prop) == 'RunWorkflow' and (obj.RunWorkflow)):
            obj.Proxy.prepareJsonVar(obj, "null")
            obj.Proxy.RunworkflowCreation(obj)

        if (str(prop) == 'RunLuigi' and (obj.RunLuigi)):
            obj.Proxy.RunLuigiScript()

        if (str(prop) == 'WorkingDirectory' and len(str(obj.WorkingDirectory)) > 0):
            obj.Proxy.updateWorkingDirectory(obj.WorkingDirectory)

    def onChanged(self, vobj, prop):
        # self.makePartTransparent(vobj)
        # CfdTools.setCompSolid(vobj)
        return

    def doubleClicked(self, vobj):

        # update Hermes active
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


# ---------------------------------------------------------------------------
# Adds the commands to the FreeCAD command manager
# ---------------------------------------------------------------------------
FreeCADGui.addCommand('CreateWorkflow', _CommandCreateHermesWorkflow())
