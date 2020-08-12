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

import os
import json


class expandJson():
    """ this class is taking a json with reference
      to other files , end inject the data from those other
      files into that json """

    def __init__(self):
        self.JsonObject = {}
        self.getFromTemplate = "Template"
        self.importJsonfromfile = "importJsonfromfile"

        self.cwd = ""
        self.WD_path = ""

    def createJsonObject(self,JsonObjectfromFile,jsonFilePath):

        # define the current working directory - where the json file has been uploaded
        self.cwd = os.path.dirname(jsonFilePath)

        # check if there is a reference to templates file in JsonObjectfromFile
        if "Templates" in JsonObjectfromFile["workflow"]:
            # Create the Template Json Object - import files if needed
            self.Templates = self.getImportedJson(JsonObjectfromFile["workflow"]["Templates"])

            # FreeCAD.Console.PrintMessage("Templates="+str(self.Templates)+"\n")
            # FreeCAD.Console.PrintMessage("###################################\n")

        # Create JsonObject will contain all the imported date from file/template

        self.JsonObject = JsonObjectfromFile.copy()
        workflow = self.JsonObject["workflow"]

        # get the List of nodes , and the 'nodes' from jsonObject
        nodeList = workflow["nodeList"]
        nodes = workflow["nodes"]
        new_nodes = {}

        # to-do:check option of get the node list from a file
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
        #        self.JsonObject["nodes"]=new_nodes
        workflow["nodes"] = new_nodes
        self.JsonObject["workflow"] = workflow

        return self.JsonObject

    def getImportedJson(self, jsonObjStruct):

        # check if jsonObjStruct is a dictionary
        if type(jsonObjStruct) is not dict:
            return

        # insert the current jsonStruct to the UpdateJson that will be return after modify
        #        UpdatedJsonStruct=jsonObjStruct.copy()
        UpdatedJsonStruct = {}

        # to know if it is the first iteration
        i = 0

        # loop all the keys,values
        for subStructKey, subtructVal in jsonObjStruct.items():

            # zero open data vars
            openKeyData = {}
            openImportData = {}

            # in case of import data from file
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


            # in case of import data from Template
            elif subStructKey == self.getFromTemplate:
                #
                # # check if there are list of files that need to be imported, or just 1:
                # # list- saved as a dictionary
                # # 1 file - saved as keys and values
                # # *if*- check if the first value is a dict
                # print("subtructVal = " + str(subtructVal))
                # if type(list(subtructVal.values())[0]) is dict:
                #
                #     for templateKey, templateVal in subtructVal.items():
                #         # call the function that open data
                #         openImportData = self.importJsonDataFromTemplate(templateVal)
                #
                #         if i > 0:
                #             # not the first iteration -> overide the data
                #             UpdatedJsonStruct = self.overidaDataFunc(openImportData, UpdatedJsonStruct)
                #         else:
                #             # first iteration -> define the UpdatedJsonStruct as the open data
                #             UpdatedJsonStruct = openImportData.copy()
                #
                #         i = i + 1
                # else:

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


                # dont apply on values that are not dict - (str/int/doubke etc.)
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

        #        FreeCAD.Console.PrintMessage("===============Before===============\n")
        #        FreeCAD.Console.PrintMessage("UpdatedJsonStruct="+str(UpdatedJsonStruct)+"\n")

        #        if type(overideData) is dict:
        # loop all the overide data
        for dataKey, dataVal in overideData.items():

            #            FreeCAD.Console.PrintMessage("=====================================\n")
            #            FreeCAD.Console.PrintMessage("dataKey="+str(dataKey)+"\n")
            #            FreeCAD.Console.PrintMessage("dataVal="+str(dataVal)+"\n")

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
                        UpdatedJsonStruct[dataKey] = self.overidaDataFunc(dataVal, UpdatedJsonStruct[dataKey])

                        # ================================================================================
                        # # compare the dataVal and structure in dataKey, and update only necessary fields
                        #
                        # # get list of all the intersections of dataVal & UpdatedJsonStruct[dataKey]
                        # duptList = UpdatedJsonStruct[dataKey].keys() & dataVal.keys()
                        #
                        # diffList = dataVal.keys() - UpdatedJsonStruct[dataKey].keys()
                        #
                        # # update the UpdatedJsonStruct where there are intersection
                        # for dupt in duptList:
                        #     pathDst = str(dataKey) + '.' + str(dupt)
                        #     self.InjectJson(UpdatedJsonStruct, dataVal[dupt], pathDst)
                        #     # InjectJson(       Dst       ,     Src     ,pathDst):
                        #
                        # for diff in diffList:
                        #     pathDst = str(dataKey) + '.' + str(diff)
                        #     self.InjectJson(UpdatedJsonStruct, dataVal[diff], pathDst)
                        #     # InjectJson(       Dst       ,     Src     ,pathDst):
                        # ================================================================================


                #                            UpdatedJsonStruct[diff]=dataVal[diff]

                # type is 'list'
                elif type(dataVal) is list:

                    # check if 'dataKey' in the structure is empty
                    if len(UpdatedJsonStruct[dataKey]) == 0:

                        # take all the data in dataVal and insert to 'dataKey' place in the structure
                        UpdatedJsonStruct[dataKey] = dataVal

                    # check it item already exist in structure, if not  add it.
                    else:

                        # loop all items in the list
                        for i in range(len(dataVal)):

                            # if item not in structure list
                            if not (dataVal[i] in UpdatedJsonStruct[dataKey]):
                                # add the item from overide data
                                UpdatedJsonStruct[dataKey].append(dataVal[i])

                # any other type (int,boolean..)
                else:
                    # update its data from overide
                    UpdatedJsonStruct[dataKey] = dataVal


            # dataKey not exist in UpdatedJsonStruct
            else:

                # add to the dictionary
                UpdatedJsonStruct[dataKey] = dataVal

        if self.getFromTemplate in UpdatedJsonStruct:
            UpdatedJsonStruct.pop(self.getFromTemplate)
        if self.importJsonfromfile in UpdatedJsonStruct:
            UpdatedJsonStruct.pop(self.importJsonfromfile)

        #        FreeCAD.Console.PrintMessage("=====================================\n")
        #        FreeCAD.Console.PrintMessage("overideData="+str(overideData)+"\n")
        #        FreeCAD.Console.PrintMessage("===============After===============\n")
        #        FreeCAD.Console.PrintMessage("UpdatedJsonStruct="+str(UpdatedJsonStruct)+"\n")

        return UpdatedJsonStruct


    def importJsonDataFromTemplate(self, importTemplate):

        UpdatedJsonStruct = {}

        # get the Hermes path
        HermesDirpath = os.getenv('HERMES_2_PATH')
        import sys
        # insert the path to sys
        # insert at 1, 0 is the script path (or '' in REPL)
        sys.path.insert(1, HermesDirpath)

        # get and initial class _templateCenter
        from hermes.Resources.nodeTemplates.templateCenter import templateCenter
        paths = None
        self._templateCenter = templateCenter(paths)

        # get template data
        UpdatedJsonStruct = self._templateCenter.getTemplate(importTemplate)

        # call 'getImportedJson' in case there are nested files that need to be imported
        UpdatedJsonStruct = self.getImportedJson(UpdatedJsonStruct)

        # # ------------ inject template from dict of Templates ------
        # # find the path from the template to wanted data
        # pathDst = importTemplate["TypeFC"]
        #
        # # create a split list of the path
        # splitPathlist = pathDst.split(".")
        #
        # # if the length og the list is bigger than 1 -> use InjectJson
        # if len(splitPathlist) > 1:
        #     UpdatedJsonStruct = self.InjectJson(UpdatedJsonStruct, self.Templates, pathDst)
        #     # InjectJson(       Dst       ,     Src      ,pathDst):
        # else:
        #     # load and recieve the json object directly from Template
        #     UpdatedJsonStruct = self.Templates[importTemplate["TypeFC"]]

        # # -----------------allow take part of a template ----------------
        # # check if there is only a specific field that need to be imported from Template
        # if "field" in importTemplate:
        #
        #     # empty data structure - so only relevent data will be returned
        #     UpdatedJsonStruct = {}
        #
        #     # empty var
        #     fieldData = self.Templates[importTemplate["TypeFC"]]
        #
        #     # loop all 'field' list
        #     for entryPath in importTemplate["field"]:
        #
        #         if (len(entryPath) == 0):
        #             continue
        #
        #         # split the entry
        #         splitEntryPath = entryPath.split(".")
        #
        #         # get the entry path wanted data
        #         for entry in splitEntryPath:
        #             fieldData = fieldData[entry]
        #
        #         # add to the UpdatedJsonStruct
        #         UpdatedJsonStruct.update(fieldData)
        #
        # #        else:
        # #            UpdatedJsonStruct=self.Templates[importTemplate["TypeFC"]]

        return UpdatedJsonStruct

    def importJsonDataFromFile(self, importFileData):
        # ----Step 1 : Remember Current Directory----

        # define current directory - saved during the recursion
        current_dir = self.cwd
        # update the current work directory
        os.chdir(current_dir)
        # ----------------------------------------------------

        #        FreeCAD.Console.PrintMessage("cwd="+os.getcwd()+"\n")

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

    #

    # to-do:make list of al possible upload files

    # done: load files from differenet hirarchy in json - also possible load only a field/list of fields from file
    def InjectJson(self, Dst, Src, pathDst):
        # get the destiny Json var, source Json data ->update the source in the destiny
        # for example:In case data has been upload from a file, and want the update only 1 entry

        # split the path into list
        splitPathlist = pathDst.split(".")
        # FreeCAD.Console.PrintMessage("splitPathlist="+str(splitPathlist)+"\n")

        # if Dst is not empty
        if len(Dst) > 0:

            # reverse the order of the list
            splitPathlist.reverse()

            # Intialize the "data" var with the "Src" data
            data = Src.copy() if Src is dict else Src

            # loop all the path list
            for x in range(len(splitPathlist) - 1):
                # if it is not the last element of the list
                if x != len(splitPathlist) - 1:
                    # take the structure containing the data
                    structKey = splitPathlist[x + 1]
                    struct = Dst[structKey]

                    # update the data in the structure - splitPathlist[x]-> the key in the strucrure
                    struct[splitPathlist[x]] = data

                    # update the struct dat in the "data" var - enable to update the data in hierarchy structure
                    data = struct

            # update the Dst json struct with the data
            # splitPathlist[-1] - the last element of the reverse path list-the highest location in the path hierarchy
            Dst[splitPathlist[-1]] = data

        else:

            struct = Src.copy()

            # loop all the path list
            for x in range(len(splitPathlist)):
                # find the current structKey
                structKey = splitPathlist[x]

                # update struct with the structKey data
                struct = struct[structKey]

            # update the Dst json struct with the struct value
            Dst = struct

        # return the update Dst json structure
        return Dst

    def loadJsonFromfile(self, filePath, entryInFile=""):

        # Open JsonFile & Read
        with open(filePath, 'r') as myfile:
            data = myfile.read()

        # parse data and return it
        dataParsed = json.loads(data)

        # No split the 'entryInFile' and get the data from that path
        if (len(entryInFile) == 0):
            return dataParsed

        # split the
        splitEntryList = entryInFile.split(".")
        for entry in splitEntryList:
            dataParsed = dataParsed[entry]

        return dataParsed