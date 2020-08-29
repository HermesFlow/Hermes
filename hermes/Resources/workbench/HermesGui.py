
# import FreeCAD modules
import FreeCAD,FreeCADGui, WebGui
import HermesTools
from HermesTools import addObjectProperty
import sys
from PyQt5 import QtGui,QtCore
import os
import json
import Part
import HermesNode

###################### Temporary hack while the hermes is not in the pythonpath
import sys
sys.path.append("/mnt/build")
######################
from hermes.Resources.nodeTemplates.templateCenter import templateCenter


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
        
        self.JsonObject = None
        self.JsonObjectString=""
        self.JsonObjectfromFile = []
        self.Templates=None
        self.nLastNodeId="-1"
        self.partPathListFromJson=[]
        self.partNameListFromJson=[]
#        self.partPathExportList=[]
        self.partNameExportList=[]
#        self.ExportPartList=[]
        self.cwd=""
        
        self.importJsonfromfile="importJsonfromfile"
        self.getFromTemplate="Template"
        
        self.WD_path=""

    def initProperties(self, obj):

        #ImportJSONFile propert- get the file path of the wanted json file
        addObjectProperty(obj, "ImportJSONFile", "", "App::PropertyFile", "IO", "Browse JSON File")
        
        #ExportJSONFile property- get the directory path of where we want to export the json file
        addObjectProperty(obj, "ExportJSONFile", "", "App::PropertyPath", "IO", "Path to save JSON File")
        
        #WorkingDirectory property- get the directory path of where we want to export our files
        addObjectProperty(obj, "WorkingDirectory", "", "App::PropertyPath", "IO", "Path to working directory")
           
        
        #JSONString property - keep the json data as a string
        addObjectProperty(obj, "JSONString", "", "App::PropertyString", "", "JSON Stringify",4)
        
#        #link property - link to other object (beside parent)
#        addObjectProperty(obj, "HermesLink", "", "App::PropertyLink", "", "Link to",4)

        #Active property- keep if obj has been activated (douuble clicked get active)        
        addObjectProperty(obj, "IsActiveWorkflow", False, "App::PropertyBool", "", "Active hermes workflow object in document")       
        
        #make some properties to be 'read-only'
        obj.setEditorMode("IsActiveWorkflow", 1)  # Make read-only (2 = hidden)
        obj.setEditorMode("Group", 1)
        
        #RunWorkflow property - Run the workflow as a basic to luigi if change to true
        addObjectProperty(obj, "RunWorkflow", False, "App::PropertyBool", "Run", "Run the workflow as a basic to luigi")
        
        #RunLuigi property - Run luigi
        addObjectProperty(obj, "RunLuigi", False, "App::PropertyBool", "Run", "Run luigi")
        

    def onDocumentRestored(self, obj):
        
        self.nLastNodeId="-1"
        
        #when restored- initilaize properties
        self.initProperties(obj)
        
        FreeCAD.Console.PrintMessage("onDocumentRestored\n")
        
        if FreeCAD.GuiUp:
            _ViewProviderHermesWorkflow(obj.ViewObject)
            
        #parse json data        
#        self.JsonObject = json.loads(obj.JSONString)
        
    def prepareJsonVar(self,obj,rootVal):
        
        self.updateJsonBeforeExport(obj)
        
        if rootVal=="null":
            #"To-Do"-change string into null json
            self.JsonObject["workflow"]["root"]=json.loads("null")
        else:
            self.JsonObject["workflow"]["root"]=rootVal
            
        self.JsonObjectString=json.dumps(self.JsonObject)
        
        

              
    def saveJson(self,obj,jsonSaveFilePath,FileSaveName):
        """
            Saves the current workflow to JSON.

        :param obj:
        :param jsonSaveFilePath:
        :param FileSaveName:
        :return:
        """

        # ^^^Export Json-file
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
            fullPath=os.path.join(jsonSaveFilePath,f"{partObjName}.stp")
                
            # export all part Object
            Part.export([partObj],u""+fullPath)
            
        self.partNameExportList=[]
        
        
    def readJson(self, obj):        
        #get json file full path 
        jsonFileName = obj.ImportJSONFile
        self.cwd=os.path.dirname(jsonFileName)
        
        #Open JsonFile , Read & parsed, assign to JsonObject
        with open(jsonFileName, 'r') as myfile:
            self.JsonObjectfromFile = json.load(myfile)

        #create jsonObject varieble that contain all data, including imported data from files/templates
        self.createJsonObject()
        
        #assign the data been import to the JSONString property after dumps
        obj.JSONString=json.dumps(self.JsonObject)
        #FreeCAD.Console.PrintMessage("obj.JSONString="+obj.JSONString+"\n")

        
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
        if "Templates" in self.JsonObjectfromFile["workflow"]:
            
            #Create the Template Json Object - import files if needed
            # add the default template file.
            self.Templates = templateCenter(self.JsonObjectfromFile["workflow"]["Templates"])


        #Create JsonObject will contain all the imported date from file/template
        self.JsonObject=self.JsonObjectfromFile
        workflow=self.JsonObject["workflow"]
        
        #get the List of nodes , and the 'nodes' from jsonObject 
        nodeList=workflow["nodeList"]
        nodes=workflow["nodes"]
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
#        self.JsonObject["nodes"]=new_nodes
        workflow["nodes"]= new_nodes
        self.JsonObject["workflow"]=workflow
    
    def getImportedJson(self,jsonObjStruct):
                
         #check if jsonObjStruct is a dictionary
        if type(jsonObjStruct) is not dict:
            return
        
        
        # insert the current jsonStruct to the UpdateJson that will be return after modify
#        UpdatedJsonStruct=jsonObjStruct.copy()
        UpdatedJsonStruct= {}

        
        #to know if it is the first iteration
        firstIteration = True
       
        #loop all the keys,values
        for subStructKey,subtructVal in jsonObjStruct.items():
            
            #zero open data vars
            openKeyData={}
            openImportData={}
            
            #in case of import data from file
            if (subStructKey==self.importJsonfromfile) or (subStructKey==self.getFromTemplate):
                
                #check if there are list of files that need to be imported, or just 1:
                # list- saved as a dictionary
                # 1 file - saved as keys and values
                # *if*- check if the first value is a dict
                if isinstance(list(subtructVal.values())[0],dict):
                    for fileKey,fileVal in subtructVal.items():
                        #call the function that open data
                        openImportData=self.importJsonDataFromFile(fileVal)

#                        FreeCAD.Console.PrintMessage("=====================================\n")
#                        FreeCAD.Console.PrintMessage("openImportData="+str(openImportData)+"\n")
#                        FreeCAD.Console.PrintMessage("=====================================\n")

                        UpdatedJsonStruct=self.overidaDataFunc(openImportData,UpdatedJsonStruct) if firstIteration\
                            else openImportData.copy()

                else:
                
                    #call the function that open data
#                    openImportData=self.checkListOfFiles(subtructVal,'File')
                    openImportData=self.importJsonDataFromFile(subtructVal)

                    UpdatedJsonStruct = self.overidaDataFunc(openImportData, UpdatedJsonStruct) if firstIteration \
                        else openImportData.copy()
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

            firstIteration = False

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
        
        #to do - get a path to exact place in Template

        UpdatedJsonStruct={}
       
        # find the path from the template to wanted data
        pathDst=importTemplate["type"]

        # create a split list of the path
        splitPathlist = pathDst.split(".")

        # if the length og the list is bigger than 1 -> use InjectJson
        if len(splitPathlist)>1:
            UpdatedJsonStruct=self.InjectJson(UpdatedJsonStruct,self.Templates,pathDst)
                                  #InjectJson(       Dst       ,     Src      ,pathDst):
        else:
            #load and recieve the json object directly from Template
            UpdatedJsonStruct=self.Templates[importTemplate["type"]]
        
        
        #check if there is only a specific field that need to be imported from Template
        if "field" in importTemplate:
            
            #empty data structure - so only relevent data will be returned
            UpdatedJsonStruct={}
            
            # empty var
            fieldData=self.Templates[importTemplate["type"]]
                    
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
#            UpdatedJsonStruct=self.Templates[importTemplate["type"]]

        return UpdatedJsonStruct
    
    def importJsonDataFromFile(self,importFileData):        
        #----Step 1 : Remember Current Directory----
        
        #define current directory - saved during the recursion
        current_dir=self.cwd
        #update the current work directory
        os.chdir(current_dir)
        #----------------------------------------------------
        
#        FreeCAD.Console.PrintMessage("cwd="+os.getcwd()+"\n") 

        #update 'pathFile' to full path- absolute
        pathFile=os.path.abspath(importFileData["path"])

        with open(importFileData["path"],'r') as myfile:
            jsonFile = json.load(myfile)

                
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

                entryData = jsonFile

                # split the
                for entry in entry.split("."):
                    entryData = entryData[entry]

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

            with open(pathFile, 'r') as myfile:
                UpdatedJsonStruct = json.load(myfile)

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
        #FreeCAD.Console.PrintMessage("splitPathlist="+str(splitPathlist)+"\n")


        # if Dst is not empty
        if len(Dst)>0:

            #reverse the order of the list
            splitPathlist.reverse()

            #Intialize the "data" var with the "Src" data
            data=Src.copy()

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

        else:

            struct=Src.copy()

            #loop all the path list
            for x in range(len(splitPathlist)):
                
                #find the current structKey
                structKey=splitPathlist[x]

                # update struct with the structKey data
                struct=struct[structKey]

            #update the Dst json struct with the struct value
            Dst=struct

   
        #return the update Dst json structure
        return Dst

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
        nodes=self.JsonObject["workflow"]["nodes"]
        for y in nodes:
            
            #get Node data
            nodeData=nodes[y]
            
            #get node name
            nodename=y     
            
            #Create node obj
            # makeNode(nodename, obj, str(x), nodeData)
            # FreeCADGui.doCommand("hermes.addObject(HermesNode.makeNode(nodename, obj, str(x), nodeData))")
            HermesNode.makeNode(nodename, obj, str(x), nodeData)


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
        if self.JsonObject is not None:

            nodes=self.JsonObject["workflow"]["nodes"]
             # loop all children in HermesWorkflow
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

            # update the child nodeDate in the JsonObject
            self.JsonObject["workflow"]["nodes"]=nodes


    def RunworkflowCreation(self,obj):
       
        # save the current work directory before it changed
        currentDirFC=os.getcwd()

        # get the path from environment variable
        HermesDirpath = os.getenv('HERMES_2_PATH')

        # add an Error message in case the environment variable does not exist
        if (HermesDirpath == None):
            FreeCAD.Console.PrintError('Error: HermesGui.py - line 940: The environment variable does not exist!\n')
            return
        current_dir = HermesDirpath

        current_dir=HermesDirpath+'/hermes/'

        #insert the path to sys
        # insert at 1, 0 is the script path (or '' in REPL)
        sys.path.insert(1, current_dir)
        sys.path.insert(1, HermesDirpath)
        
        #update 'current_dir' to full path- absolute
        current_dir=os.path.abspath(current_dir)
        
        #update the current work directory
        os.chdir(current_dir)  

        #import hermesWorkflow
        from hermes import hermesWorkflow

        # call hermes workflow and keep its result in var
        wf = hermesWorkflow(self.JsonObjectString,self.WD_path,HermesDirpath)

        print(wf)
        print("===================================")

        # save the workflow run result in th WD
        FCtoLuigi_path = self.WD_path + "/FCtoLuigi.py"
        with open(FCtoLuigi_path, "w") as outfile:
            outfile.write(wf.build("luigi"))

        # Create the Luigi command run
        LuigiFile=''' #!/bin/sh
    
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
        currentDirFC=os.getcwd()

        # get the path from environment variable
        HermesDirpath = os.getenv('HERMES_2_PATH')
        #print("RunLuigi:HermesDirpath=" + str(HermesDirpath))
        current_dir=HermesDirpath

        # insert the path to sys
        # insert at 1, 0 is the script path (or '' in REPL)
        sys.path.insert(1, current_dir)
        sys.path.insert(1, self.WD_path)
#        
        #update 'current_dir' to full path- absolute
        current_dir=os.path.abspath(current_dir)

        # change directory to the Working directory
        if (self.WD_path != ''):
            os.chdir(self.WD_path)

            # remove the 'OpenFOAMfiles' in case exist
            shutil.rmtree('OpenFOAMfiles', ignore_errors=True)

            # remove the output folder
            shutil.rmtree(self.WD_path+'/outputs', ignore_errors=True)

            # create a new directory for the LuigiRun output files
            os.mkdir(self.WD_path+"/OpenFOAMfiles")

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
    
    def updateWorkingDirectory(self,path):
        self.WD_path=path

        
        

      
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
        FreeCADGui.doCommand("HermesTools.setActiveHermes(hermes)")
        
        ''' Objects ordered according to expected workflow '''
        #return

        # Add HermesNode object when HermesGui container is created
        FreeCADGui.addModule("HermesNode")
        #FreeCADGui.doCommand("hermes.addObject(HermesNode.makeNode())")

        # Add HermesBcNode object when HermesGui container is created
        FreeCADGui.addModule("HermesBcNode")

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
        """
            We get here when the object of HermesWorkflow changes
            For this moment, we consider only the JSONFile parameter

        :param obj:

        :param prop:

        :return:
        """

        fname = "_handle_%s" % str(prop)

        if hasattr(self,fname):
            getattr(self,fname)(obj)

    def _handle_ImportJSONFile(self,obj):
        if len(str(obj.ImportJSONFile)) > 0:
            obj.Proxy.readJson(obj)
            # seperate file and dir, and define dir as workingDir
            Dirpath=os.path.dirname(obj.ImportJSONFile)
            # update workind directory to self of hermes class
            obj.Proxy.updateWorkingDirectory(Dirpath)
            # update workind directory to the hermes obj
            obj.WorkingDirectory=Dirpath
            obj.ImportJSONFile = ''

    def _handle_ExportJSONFile(self,obj):
        if len(str(obj.ExportJSONFile)) > 0:
            obj.Proxy.prepareJsonVar(obj, "null")
            obj.Proxy.saveJson(obj, obj.ExportJSONFile, obj.Label)
            obj.ExportJSONFile = ''

    def _handle_RunWorkflow(self,obj):
        if obj.Proxy.JsonObject is not None:
            obj.Proxy.prepareJsonVar(obj, "null")
            obj.Proxy.RunworkflowCreation(obj)

    def _handle_RunLuigi(self,obj):
        obj.Proxy.RunLuigiScript()

    def _handle_WorkingDirectory(self,obj):
        if len(str(obj.WorkingDirectory)) > 0:
            obj.Proxy.updateWorkingDirectory(obj.WorkingDirectory)


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





