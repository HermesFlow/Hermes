"""
    Expands the templates in a file to a detaile pipeline file.
    Allow the addition of outer parameter to overwrite existing values of the pipeline.

    Note:
        Check if we want to use jsonpath.
"""
from ..Resources.nodeTemplates.templateCenter import templateCenter
import json
import os
import collections.abc

class expandWorkflow:
    """ this class is taking a json with reference
      to other files , end inject the data from those other
      files into that json """

    def updateMap(self,d, u):
        for k, v in u.items():
            if isinstance(v, collections.abc.Mapping):
                d[k] = self.updateMap(d.get(k, {}), v)
            else:
                d[k] = v
        return d


    @property
    def templateCenter(self):
        return self._templateCenter

    def __init__(self):
        self.getFromTemplate = "Template"
        self.importJsonfromfile = "importJsonfromfile"

        paths = None
        self._templateCenter = templateCenter(paths)


        self.cwd = ""
        self.WD_path = ""

    def expand(self, templateJSON, parameters={}):
        """
        Expands a workflow by imbedding the template node to the workflow.

        Parameters
        -----------

            templateJSON: str, dict
                        The path of the workflow json, a json str or a json obj

            parameters : dict
                        A dictionary that can overwrite the template defaults.
                        Adds the values to the dictionary if necessary

        Returns
        --------
            Dict.
        """

        if isinstance(templateJSON,str):
            if os.path.exists(templateJSON):
                with open(templateJSON, 'r') as myfile:
                    JsonObjectfromFile  = json.load(myfile)
            else:
                JsonObjectfromFile = json.loads(templateJSON)

            # define the current working directory - where the json file has been uploaded
            self.cwd = os.path.dirname(templateJSON)
        else:
            JsonObjectfromFile = templateJSON

            # define the current working directory as the current directory.
            self.cwd = os.getcwd()


        # Create JsonObject will contain all the imported date from file/template
        JsonObject = JsonObjectfromFile.copy()
        workflow = JsonObject["workflow"]

        # get the List of nodes , and the 'nodes' from jsonObject
        nodeList = workflow["nodeList"]
        nodes = workflow["nodes"]
        new_nodes = {}

        # Loop the node List, and import external data
        for node in nodeList:

            # check if the node from list is in the dictionary list
            if node in nodes:
                # get the current node
                currentNode = nodes[node]

                # update the data in the nodes from file/templates to concrete data
                updatedCurrentNode = self.getImportedJson(currentNode)

                # add the data into 'new_nodes'
                new_nodes[node] = updatedCurrentNode

        # update the data in JsonObject to be the new dictionary new_nodes
        workflow["nodes"] = new_nodes
        JsonObject["workflow"] = workflow

        ret = self.updateMap(JsonObject,parameters)

        return ret

    def getImportedJson(self, jsonObjStruct):

        # check if jsonObjStruct is a dictionary
        if type(jsonObjStruct) is not dict:
            return

        # insert the current jsonStruct to the UpdateJson that will be return after modify
        UpdatedJsonStruct = {}

        # to know if it is the first iteration
        i = 0

        # loop all the keys,values
        for subStructKey, subtructVal in jsonObjStruct.items():

            # zero open data vars
            openKeyData = {}
            openImportData = {}

            # in case import data from <file>
            if subStructKey == self.importJsonfromfile:

                # check if there are list of files that need to be imported, or just 1:
                # list- saved as a dictionary
                # 1 file - saved as keys and values
                # *if*- check if the first value is a dict
                if type(list(subtructVal.values())[0]) is dict:

                    for fileKey, fileVal in subtructVal.items():
                        # call the function that open data
                        openImportData = self.importJsonDataFromFile(fileVal)

                        if i > 0:
                            # not the first iteration -> overide the data
                            UpdatedJsonStruct = self.overidaDataFunc(openImportData, UpdatedJsonStruct)
                        else:
                            # first iteration -> define the UpdatedJsonStruct as the open data
                            UpdatedJsonStruct = openImportData.copy()

                        i = i + 1
                else:

                    # call the function that open data
                    openImportData = self.importJsonDataFromFile(subtructVal)

                    if i > 0:
                        # not the first iteration -> overide the data
                        UpdatedJsonStruct = self.overidaDataFunc(openImportData, UpdatedJsonStruct)

                    else:
                        # first iteration -> define the UpdatedJsonStruct as the open data
                        UpdatedJsonStruct = openImportData.copy()


            # in case import data from <Template>
            elif subStructKey == self.getFromTemplate:

                # call the function that open data
                openImportData = self.importJsonDataFromTemplate(subtructVal)

                if i > 0:
                    # not the first iteration -> overide the data
                    UpdatedJsonStruct = self.overidaDataFunc(openImportData, UpdatedJsonStruct)
                else:
                    # first iteration -> define the UpdatedJsonStruct as the open data
                    UpdatedJsonStruct = openImportData.copy()

            # No imported data from path or Template
            else:

                # check if the json substruct is list(in case its items are objects)
                if type(subtructVal) is list:

                    # create an identaty list , that will be updated
                    UpdatedJsonList = subtructVal.copy()

                    # loop all the list items
                    for ind in range(len(subtructVal)):

                        # check each item if its type is a dictionary -
                        if type(subtructVal[ind]) is dict:
                            # call 'getImportedJson' in case there are nested files that need to be imported
                            UpdatedListItem = self.getImportedJson(subtructVal[ind])

                            # update the updateItem in the main Updated json List
                            UpdatedJsonList[ind] = UpdatedListItem

                    # update the list in the json structure
                    UpdatedJsonStruct[subStructKey] = UpdatedJsonList



                # dont apply on values that are not dict - (str/int/double etc.)
                elif type(subtructVal) is dict:


                    # call 'getImportedJson' in case there are nested files that need to be imported
                    openKeyData = self.getImportedJson(subtructVal)

                    if subStructKey in UpdatedJsonStruct:
                        # not the first iteration -> overide the data
                        UpdatedJsonStruct[subStructKey] = self.overidaDataFunc(openKeyData,
                                                                               UpdatedJsonStruct[subStructKey])

                    else:
                        # first iteration -> define the UpdatedJsonStruct as the open data
                        UpdatedJsonStruct[subStructKey] = openKeyData.copy()

                # any other type-
                #   =if exist - update the dat
                #   =no exist - add it to the structure
                else:
                    UpdatedJsonStruct[subStructKey] = jsonObjStruct[subStructKey]

            i = i + 1

        return UpdatedJsonStruct

    def overidaDataFunc(self, overideData, UpdatedJsonStruct):

        # loop all the overide data

        for dataKey, dataVal in overideData.items():

            # check for each key, if exsist in UpdatedJsonStruct
            if dataKey in UpdatedJsonStruct:
                # type is dictionary
                if type(dataVal) is dict:

                    # check if 'dataKey' in the structure is empty
                    if len(UpdatedJsonStruct[dataKey]) == 0:

                        # take all the data in dataVal and insert to 'dataKey' place in the structure
                        UpdatedJsonStruct[dataKey] = dataVal

                    else:
                        # recursion of override on the dict
                        if isinstance(UpdatedJsonStruct[dataKey],dict):
                            UpdatedJsonStruct[dataKey] = self.overidaDataFunc(dataVal, UpdatedJsonStruct[dataKey])
                        else:
                            UpdatedJsonStruct[dataKey] = dataVal

                # type is any other data type.
                else:
                    UpdatedJsonStruct[dataKey] = dataVal

            # dataKey not exist in UpdatedJsonStruct
            else:
                # add to the dictionary
                UpdatedJsonStruct[dataKey] = dataVal

        # remove self.getFromTemplate and self.importJsonfromfile from UpdatedJsonStruct
        if self.getFromTemplate in UpdatedJsonStruct:
            UpdatedJsonStruct.pop(self.getFromTemplate)
        if self.importJsonfromfile in UpdatedJsonStruct:
            UpdatedJsonStruct.pop(self.importJsonfromfile)

        return UpdatedJsonStruct


    def importJsonDataFromTemplate(self, importTemplate):

        UpdatedJsonStruct = {}

        # # get the Hermes path
        # HermesDirpath = os.getenv('HERMES_2_PATH')
        # import sys
        # # insert the path to sys
        # # insert at 1, 0 is the script path (or '' in REPL)
        # sys.path.insert(1, HermesDirpath)
        #
        # # get and initial class _templateCenter
        # from hermes.Resources.nodeTemplates.templateCenter import templateCenter

        paths = None
        self._templateCenter = templateCenter(paths)

        # get template data
        UpdatedJsonStruct = self._templateCenter.getTemplate(importTemplate)

        # call 'getImportedJson' in case there are nested files that need to be imported
        UpdatedJsonStruct = self.getImportedJson(UpdatedJsonStruct)

        return UpdatedJsonStruct

    def importJsonDataFromFile(self, importFileData):
        # ----Step 1 : Remember Current Directory----

        # define current directory - saved during the recursion
        current_dir = self.cwd
        # update the current work directory
        os.chdir(current_dir)
        # ----------------------------------------------------

        # get the path of the file
        pathFile = importFileData["path"]

        # update 'pathFile' to full path- absolute
        pathFile = os.path.abspath(pathFile)

        # check if there is only a specific field that need to be imported from file
        if "field" in importFileData:

            # empty var
            UpdatedJsonStruct = {}

            # loop all 'field' list
            for entry in importFileData["field"]:
                # todo - till now only field been taken were dictionaries ,
                #       check possbility of taking ecnries that are not dict-
                #       take the data, create dict struct="key:value", and inject it

                # get the entry data from the file
                entryData = self.loadJsonFromfile(pathFile, entry)

                # add to the UpdatedJsonStruct
                UpdatedJsonStruct.update(entryData)

                # ----Step 2 : Change CWD to pathFile Directory----

                # get the current full path of the directory's file
                dirname = os.path.dirname(pathFile)

                # update the current work directory at 'os' and at 'cwd' var
                os.chdir(dirname)
                self.cwd = dirname
                # ----------------------------------------------------

                # call 'getImportedJson' in case there are nested files that need to be imported
                UpdatedJsonStruct = self.getImportedJson(UpdatedJsonStruct)

        else:

            # load and recieve the json object from file
            UpdatedJsonStruct = self.loadJsonFromfile(pathFile)

            # ----Step 2 : Change CWD to pathFile Directory----

            # get the current full path of the directory's file
            dirname = os.path.dirname(pathFile)

            # update the current work directory at 'os' and at 'cwd' var
            os.chdir(dirname)
            self.cwd = dirname
            # ----------------------------------------------------

            # call 'getImportedJson' in case there are nested files that need to be imported
            UpdatedJsonStruct = self.getImportedJson(UpdatedJsonStruct)

            # ---Step 3: Return to previous working directory---

        # update the current work directory at 'os' and at 'cwd' var
        os.chdir(current_dir)
        self.cwd = dirname = current_dir
        # ----------------------------------------------------

        return UpdatedJsonStruct



    def loadJsonFromfile(self, filePath, entryInFile=""):

        # Open JsonFile & Read
        with open(filePath, 'r') as myfile:
            dataParsed = json.load(myfile)


        # No split the 'entryInFile' and get the data from that path
        if (len(entryInFile) == 0):
            return dataParsed

        # split the
        splitEntryList = entryInFile.split(".")
        for entry in splitEntryList:
            dataParsed = dataParsed[entry]

        return dataParsed