
# import FreeCAD modules
import FreeCAD, FreeCADGui
import HermesTools
from HermesTools import addObjectProperty

# python modules
import sys
from PyQt5 import QtCore
import os
import json
import Part

# Hemes modules
import HermesNode
# from hermes.Resources.workbench.openFOAM2.mesh import HermesPart
from openFOAM2.mesh import HermesPart
# from openFOAM2.mesh import HermesGeometryDefinerEntity

# add hermes to paths
HermesDirpath = os.getenv('HERMES_2_PATH')
# add an Error message in case the environment variable does not exist
if (HermesDirpath == None):
    FreeCAD.Console.PrintError('Error: HermesGui.py - The Hermes environment variable does not exist!\n')
sys.path.insert(1, HermesDirpath)

from hermes.workflow.expandWorkflow import expandWorkflow

# ###################### Temporary hack while the hermes is not in the pythonpath
# sys.path.append("/mnt/build")
# ######################
# from hermes.Resources.nodeTemplates.old.templateCenter import templateCenter

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

        self.JsonObject = None
        self.JsonObjectString = ""
        self.Templates = None
        self.partPathListFromJson = []
        self.partNameListFromJson = []
        #        self.partPathExportList=[]
        self.partNameExportList = []
        #        self.ExportPartList=[]
        self.partList = {}

        self.importJsonfromfile = "importJsonfromfile"
        self.getFromTemplate = "Template"

        self.WD_path = ""

        # get the path from environment variable
        self.HermesDirpath = os.getenv('HERMES_2_PATH')

        # add an Error message in case the environment variable does not exist
        if (self.HermesDirpath == None):
            FreeCAD.Console.PrintError('Error: HermesGui.py - The Hermes environment variable does not exist!\n')
            return


    def initProperties(self, obj):
        ''' defined the properties of the Hermes Workflow '''

        # ImportJSONFile propert- get the file path of the wanted json file
        addObjectProperty(obj, "ImportJSONFile", "", "App::PropertyFile", "IO", "Browse JSON File")

        # ExportGUIJSONFile property- get the directory path of where we want to export the json file
        addObjectProperty(obj, "ExportGUIJSONFile", "", "App::PropertyPath", "IO", "Path to save JSON File")

        # ExportExecuteJSONFile property- get the directory path of where we want to export the json file
        addObjectProperty(obj, "ExportExecuteJSONFile", "", "App::PropertyPath", "IO", "Path to save JSON File")


        # WorkingDirectory property- get the directory path of where we want to export our files
        addObjectProperty(obj, "WorkingDirectory", "", "App::PropertyPath", "IO", "Path to working directory")

        # JSONString property - keep the json data as a string
        addObjectProperty(obj, "JSONString", "", "App::PropertyString", "", "JSON Stringify", 4)

        # Solved Fields property
        addObjectProperty(obj, "SolvedFields", ["U", "P"], "App::PropertyStringList", "JSON", "Solved Fields")
        # Aux Fields property
        addObjectProperty(obj, "AuxFields", [], "App::PropertyStringList", "JSON", "Aux Fields")

        #        #link property - link to other object (beside parent)
        #        addObjectProperty(obj, "HermesLink", "", "App::PropertyLink", "", "Link to",4)

        # Active property- keep if obj has been activated (douuble clicked get active)
        addObjectProperty(obj, "IsActiveObj", False, "App::PropertyBool", "",
                          "Active hermes workflow object in document")

        # make some properties to be 'read-only'
        obj.setEditorMode("IsActiveObj", 1)  # Make read-only (2 = hidden)
        obj.setEditorMode("Group", 1)

        # RunWorkflow property - Run the workflow as a basic to luigi if change to true
        addObjectProperty(obj, "RunWorkflow", False, "App::PropertyBool", "Run", "Run the workflow as a basic to luigi")

        # RunLuigi property - Run luigi
        addObjectProperty(obj, "RunLuigi", False, "App::PropertyBool", "Run", "Run luigi")

    def onDocumentRestored(self, obj):

        '''
            When a FreeCAD document is restored (opened after been saving
            as a FreeCAD file), it updates the following things in the Node
        '''

        # when restored- initilaize properties
        self.initProperties(obj)

        FreeCAD.Console.PrintMessage("onDocumentRestored\n")

        if FreeCAD.GuiUp:
            _ViewProviderHermesWorkflow(obj.ViewObject)

        # parse json data
    #        self.JsonObject = json.loads(obj.JSONString)

    def prepareJsonVar(self, obj, rootVal):
        '''
            - update the json var with data from FreeCAD nodes
            - update the root node
        '''
        self.updateJsonBeforeExport(obj)

        if rootVal == "null":
            # "To-Do"-change string into null json
            self.JsonObject["workflow"]["root"] = json.loads("null")
        else:
            self.JsonObject["workflow"]["root"] = rootVal

        self.JsonObjectString = json.dumps(self.JsonObject)

    def prepareExecuteJsonVar(self, obj, rootVal):
        self.prepareJsonVar(obj, rootVal)

        import copy
        executeJson = copy.deepcopy(self.JsonObject)
        for node in executeJson["workflow"]["nodes"]:
            if "GUI" in executeJson["workflow"]["nodes"][node]:
                executeJson["workflow"]["nodes"][node].pop("GUI")

        return executeJson


    # def saveJson(self, obj, jsonSaveFilePath, FileSaveName):
    def saveJson(self, obj, jsonSaveFileName, exportJson):
        """
            Saves the current workflow to JSON.

        :param obj:
        :param jsonSaveFilePath:
        :param FileSaveName:
        :return:
        """

        # ^^^Export Json-file

        # define the full path of the export file
        # jsonSaveFileName = jsonSaveFilePath + '/' + FileSaveName + '.json'

        # get the json want to be export
        # dataSave = self.JsonObject

        # save file to the selected place
        with open(jsonSaveFileName, "w") as write_file:
            json.dump(exportJson, write_file, indent=4)  # indent make it readable

        # ^^^Export Part-files

        # # export FreeCAD parts
        # doc = obj.Document
        #
        # # loop all the objects
        # for y in range(len(self.partNameExportList)):
        #
        #     partObjName = self.partNameExportList[y]
        #     partObj = doc.getObject(partObjName)
        #
        #     # Define full path
        #     # 'stp' file
        #     fullPath=os.path.join(jsonSaveFilePath,f"{partObjName}.stp")
        #     # fullPath = jsonSaveFilePath + '/' + partObjName + '.stp'
        #
        #     # 'stl' file
        #     # fullPath_stl = jsonSaveFilePath + '/' + partObjName + '.stl'
        #
        #     # export all part Object
        #     Part.export([partObj], u"" + fullPath)
        #
        # self.partNameExportList = []

    def readJson(self, obj):
        '''
            1. gets JSON file, expand it (in case of refrences to data),
               and save into json var.
            2. clear all parts and nodes from FreeCAD
            3. set the data from the JSON into FreeCAD
        '''
        # get json file full path
        jsonFilePath = obj.ImportJSONFile

        # create jsonObject varieble that contain all data, including imported data from files/templates
        self.JsonObject = expandWorkflow().expand(jsonFilePath)
        if self.JsonObject is None:
            return

        # assign the data been import to the JSONString property after dumps
        obj.JSONString = json.dumps(self.JsonObject)
        # FreeCAD.Console.PrintMessage("obj.JSONString="+obj.JSONString+"\n")

        # clear the nodes objects
        for child in obj.Group:
            if child is not None:
                child.Proxy.RemoveNodeObj(child)
            obj.Document.removeObject(child.Name)

        # clear the part Object from json
        if len(self.partPathListFromJson) != 0:
            for x in self.partNameListFromJson:
                partObj = FreeCAD.ActiveDocument.getObject(x)
                if partObj is not None:
                    obj.Document.removeObject(x)

                # clear the part lists
                self.partPathListFromJson = []
                self.partNameListFromJson = []


        if "SolvedFields" in self.JsonObject["workflow"]:
            setattr(obj, "SolvedFields", self.JsonObject["workflow"]["SolvedFields"].split())
        if "AuxFields" in self.JsonObject["workflow"]:
            setattr(obj, "AuxFields", self.JsonObject["workflow"]["AuxFields"].split())

        # create node list
        self.setJson(obj)

        # create node objects based on json data

    def setJson(self, obj):
        ''' set the JSON into FreeCAD '''
        # todo: is needed? why not calling directly to 'updateNodeList'
        self.updateNodeList(obj)
        #        self.selectNode(obj,"1")

        return

    def loadPart(self, obj, partPath):
        '''
            not in use at moment
            Allow upload part to FreeCAD from dir
        '''

        partIndex = -1
        os.chdir(self.WD_path)

        if partPath.startswith("hermes"):
            # check if relative path to Hermes folder
            partPath = os.path.join(self.HermesDirpath, partPath)
        else:
            # update 'pathFile' to full path- absolute - relative to working dir
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
        '''
            not in use at moment
            Exports part to FreeCAD to dir
        '''

        if partObjName in self.partNameExportList:
            return

        self.partNameExportList.append(partObjName)

    # =============================================================================
    #     def UpdatePartList(self,obj):
    # =============================================================================

    def updateNodeList(self, obj):
        ''' creates nodes from JSON in FreeCAD '''
        x = 1
        nodes = self.JsonObject["workflow"]["nodes"]
        for node in nodes:

            if "GUI" in nodes[node]:
                # get Node data
                nodeData = nodes[node]["GUI"]
            else:
                #get template path
                templatePath = nodes[node]["Template"]
                #import node template
                nodeData = expandWorkflow.importJsonDataFromTemplate(templatePath)
                #copy the data from input parameters? or later after node exist

            # FreeCAD.Console.PrintMessage("nodeData = " + str(nodeData) + "\n")
            # FreeCAD.Console.PrintMessage("==================\n")

            # get node name
            nodename = node


            # Create node obj
            # makeNode(nodename, obj, str(x), nodeData)
            # FreeCADGui.doCommand("hermes.addObject(HermesNode.makeNode(nodename, obj, str(x), nodeData))")
            nodeObj = HermesNode.makeNode(nodename, obj, str(x), nodeData)

            initParams = nodes[node]["Execution"]["input_parameters"]
            if initParams:
                nodeObj.Proxy.executeToGui(nodeObj, initParams)

            x = x + 1

        return

    # def updateLastNode(self, obj, nNodeId):


    def updateLastNode(self, obj):
        '''
            backup LastNode data
            find the node that is activated and update it json from FreeCAD.
            change to not active
        '''

        # loop all objects in the document
        objsFC = FreeCAD.ActiveDocument.Objects
        a = [o for o in objsFC if o != obj and o.Module == 'App' and o.IsActiveObj]

        for o in a:
            # FreeCAD.Console.PrintMessage("updateLastNode obj " + o.Name + "\n")

            # backup obj 'nodeDate'
            o.Proxy.backupNodeData(o)

            # update the node active property to false
            o.IsActiveObj = False

            # recompute all needed objects
            FreeCAD.ActiveDocument.recompute()
            parent = o.getParentGroup()
            if parent != obj:
                self.recomputeParents(obj, o.getParentGroup())



    def recomputeParents(self,HermesWorkflow, parent):
        '''
            update the display of the parents of the nodes
        '''
        if parent == HermesWorkflow:
            return
        else:
            # sign the parent to the updates list items for recompute
            parent.touch()
            # parent.purgeTouched()

            self.recomputeParents(HermesWorkflow, parent.getParentGroup())

            return

    def updateJsonBeforeExport(self, obj):
        '''
            update the main JSON var
            loop all nodes and update each node data in the main JSON var
        '''

        self.JsonObject["workflow"]["SolvedFields"] = " ".join(getattr(obj, "SolvedFields"))
        self.JsonObject["workflow"]["AuxFields"] = " ".join(getattr(obj, "AuxFields"))


        # loop all children in HermesWorkflow
        for child in obj.Group:
            # back child date
            child.Proxy.backupNodeData(child)

            # back child properties
            child.Proxy.UpdateNodePropertiesData(child)

            # get child updated nodeData
            nodaData = json.loads(child.NodeDataString)

            nodename = child.Proxy.name

            # # update the child nodeDate in the JsonObject
            self.JsonObject["workflow"]["nodes"][nodename]["GUI"] = nodaData

            # if "BlockMesh" in nodename:
            # if "BoundaryCondition" not in nodename:
            ch_jinja = child.Proxy.guiToExecute(child)
            if ch_jinja is not None:
                self.JsonObject["workflow"]["nodes"][nodename]["Execution"]["input_parameters"] = ch_jinja


        return

    def RunworkflowCreation(self, obj):
        '''
            Run the workflow script -
            send the JSON and creates the file that needed to run luigi
        '''

        # save the current work directory before it changed
        currentDirFC = os.getcwd()

        current_dir = self.HermesDirpath + '/hermes/'

        # insert the path to sys
        # insert at 1, 0 is the script path (or '' in REPL)
        sys.path.insert(1, current_dir)
        sys.path.insert(1, self.HermesDirpath)

        # update 'current_dir' to full path- absolute
        current_dir = os.path.abspath(current_dir)

        # update the current work directory
        os.chdir(current_dir)

        # import hermesWorkflow
        # from hermes import hermesWorkflow
        from hermes import workflow

        # call hermes workflow and keep its result in var
        # wf = hermesWorkflow(self.JsonObjectString, self.WD_path, self.HermesDirpath)
        wf = workflow(self.JsonObjectString, self.WD_path, self.HermesDirpath)

        newWorkflow = "FCtoLgi.py"
        builder = "luigi"
        build = wf.build(builder)
        with open(newWorkflow, "w") as file:
            file.write(build)

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
        '''
            Run Luigi script -
            take the exports from run workflow and run luigi
        '''
        import shutil
        import os
        #        os.system("echo HI > /tmp/outputs_path.txt")

        # save the current work directory before it changed
        currentDirFC = os.getcwd()

        # define current dir
        current_dir = self.HermesDirpath

        if (len(self.WD_path) == 0) or (len(current_dir) == 0):
            return

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

    def updateFields(self, fieldList, HermesObj):
        '''
            when the field list of the problem is changed, it
            updates the field nodes in BoundaryCondition, FvSchemes,
            FvSolution
        '''

        for child in HermesObj.Group:
            if "FvSchemes" in child.Type:
                child.Proxy.updateNodeFields(fieldList, child)
            if "FvSolution" in child.Type:
                child.Proxy.updateNodeFields(fieldList, child)
            if "BCNode" in child.Type: # BoundaryCondition type
                child.Proxy.updateNodeFields(fieldList, child)
                child.Proxy.updateInternalField(fieldList + HermesObj.AuxFields, child)

            # if Name/Label is different - so better use Type is constant
            # if child.Name in ["BoundaryCondition", "FvSchemes", "FvSolution"]:
            #     child.Proxy.updateNodeFields(fieldList, child)


    def updateAuxFields(self, fieldList, HermesObj):
        '''
            when the field list of the problem is changed, it
            updates the field nodes in BoundaryCondition, FvSchemes,
            FvSolution
        '''
        for child in HermesObj.Group:
            # BoundaryCondition type
            if "BCNode" in child.Type:
                child.Proxy.updateAuxNodeFields(fieldList, child)
                child.Proxy.updateInternalField(fieldList + HermesObj.SolvedFields, child)


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
        # FreeCADGui.addModule("HermesGeometryDefinerNode")

        # FreeCADGui.addModule("HermesSnappyHexMesh")



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
        """
            We get here when the object of HermesWorkflow changes
            For this moment, we consider only the JSONFile parameter
        """
        fname = "_handle_%s" % str(prop)

        if hasattr(self, fname):
            getattr(self, fname)(obj)

    def _handle_ImportJSONFile(self, obj):
        '''
            take the path of the JSON and send to function that import it
        '''
        if len(str(obj.ImportJSONFile)) > 0:
            # seperate file and dir, and define dir as workingDir
            Dirpath = os.path.dirname(obj.ImportJSONFile)
            # update workind directory to self of hermes class
            obj.Proxy.updateWorkingDirectory(Dirpath)
            # update workind directory to the hermes obj
            obj.WorkingDirectory = Dirpath
            obj.Proxy.readJson(obj)
            obj.ImportJSONFile = ''

    def _handle_ExportGUIJSONFile(self, obj):
        '''
            take the path and
            - update JSON
            - Export JSON to the path choosen
        '''
        if len(str(obj.ExportGUIJSONFile)) > 0:
            obj.Proxy.prepareJsonVar(obj, "null")
            # define the full path of the export file
            jsonSaveFileName = obj.ExportGUIJSONFile + '/' + obj.Label + '_GUI.json'
            obj.Proxy.saveJson(obj, jsonSaveFileName,  obj.Proxy.JsonObject)
            obj.ExportGUIJSONFile = ''

    def _handle_ExportExecuteJSONFile(self, obj):
        '''
            take the path and
            - update JSON
            - Export JSON to the path choosen
        '''
        if len(str(obj.ExportExecuteJSONFile)) > 0:
            executeJson = obj.Proxy.prepareExecuteJsonVar(obj, "null")
            # define the full path of the export file
            jsonSaveFileName = obj.ExportExecuteJSONFile + '/' + obj.Label + '_Execute.json'
            obj.Proxy.saveJson(obj, jsonSaveFileName, executeJson)
            obj.ExportExecuteJSONFile = ''

    def _handle_RunWorkflow(self, obj):
        ''' update the JSON and call the function that run the workflow'''
        if obj.Proxy.JsonObject is not None:
            if obj.RunWorkflow:
                obj.Proxy.prepareJsonVar(obj, "null")
                obj.Proxy.RunworkflowCreation(obj)

    def _handle_RunLuigi(self, obj):
        if obj.RunLuigi:
            obj.Proxy.RunLuigiScript()

    def _handle_WorkingDirectory(self, obj):
        if len(str(obj.WorkingDirectory)) > 0:
            obj.Proxy.updateWorkingDirectory(obj.WorkingDirectory)

    def _handle_SolvedFields(self, obj):
        ''' updated the fields in the doc'''
        obj.Proxy.updateFields(obj.SolvedFields, obj)

    def _handle_AuxFields(self, obj):
        ''' updated the fields in the doc'''
        # obj.Proxy.updateFields(obj.AuxFields, obj)
        obj.Proxy.updateAuxFields(obj.AuxFields, obj)


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
