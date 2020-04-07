#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 13 09:48:45 2019

@author: noga
"""

import json
from jinja2 import FileSystemLoader, Environment
import os

# =========================================================

def list2dict(listVar):
    dictVar = {}
    # loop all items in the list
    i=1
    for item in listVar:
        # 2 keys in each item- name and properties
        keys = list(item.keys())
        # find the key contain the name
        if "Name" in keys[0]:
            nameKey = keys[0]
            nameVal = keys[1]
            print("nameKey="+nameKey + " ; nameVal="+nameVal)
            # the name set as key in geometryDict, and the properties as the value of that key
            dictVar[item[nameKey]] = item[nameVal]
        elif "Name" in keys[1]:
            nameKey = keys[1]
            nameVal = keys[0]
            # the name set as key in geometryDict, and the properties as the value of that key
            dictVar[item[nameKey]] = item[nameVal]
        else:
            nameKey = "f"+str(i)
            nameVal = item
            i=i+1
            # the name set as key in geometryDict, and the properties as the value of that key
            dictVar[nameKey] = nameVal


    return dictVar

# =========================================================

def getNestedProperties(ParentDict,nestedKey):
    # nested keys (inside a temporary dict, insdide the Parent dictionary) will be
    # updated in the Parent dictionary , then the temporary dict will be removed

    #if it's empty -> just remove it
    if len(ParentDict[nestedKey]) == 0:
        ParentDict.pop(nestedKey)
    else:
        # do as been mention above
        for key, value in ParentDict[nestedKey].items():
            ParentDict[key] = value
        ParentDict.pop(nestedKey)

    # return the updated dictionary
    return ParentDict

# =========================================================

def fvSolOFfunc(jsonData,saveDir):

    # get the path uses before
    import sys
    sysPathList=sys.path

    #find the path of Hermes folder
    HermesDirpath = os.getenv('HERMES_2_PATH')  
    workingDir=HermesDirpath+"/hermes/Resources/executers/CreateDictFiles/"

    # read FoamFile
    with open(workingDir+'fvSolutionDir/templates/FoamFileDict.json', 'r') as myfile:
        data1 = myfile.read()

    # parse the FoamFileDict from string to json
    FoamFileDict = json.loads(data1)

    nodeName = "fvSolution"

    # update FoamFileDict with node name
    FoamFileDict["object"] = nodeName

    # =============================== update dict Data ================================

    # update lists to dict

    # -----------------------------------------------
    # update solvers
    solvers = list2dict(jsonData["solvers"])

    # loop all the solvers parameters
    for parameterKey,parameterValue in solvers.items():

        # add all "more properties" , and remove its object
        if "more properties" in parameterValue:
            parameter = getNestedProperties(parameterValue, "more properties")

        # add all "GAMGproperties" , and remove its object
        if "GAMGproperties" in parameterValue:
            parameterValue["GAMGproperties"] = parameterValue["GAMGproperties"][0]
            parameter = getNestedProperties(parameterValue, "GAMGproperties")

            if "cacheAgglomeration" in parameter:
                # turn true/false into "on/off"
                parameter["cacheAgglomeration"] = "on" if parameter["cacheAgglomeration"] else "off"

        # update the updated parameter in solvers
        solvers[parameterKey] = parameter

    # update the updated solvers in jsonData
    jsonData["solvers"] = solvers

    # ---------------------------------------------------

    # update algorithms
    jsonData["algorithms"] = list2dict(jsonData["algorithms"])

    # take all the algorithms data, move it to jsonData, and then remove algorithms
    for Key,Value in jsonData["algorithms"].items():
        jsonData[Key] = Value
    jsonData.pop("algorithms")


    # ====================================================================================


    # define the environment - in this case : templates directory
    file_loader = FileSystemLoader(workingDir+'fvSolutionDir/templates')
    env = Environment(loader=file_loader)

    # call the main file that contain all refernces to others
    template = env.get_template('fvSolBasicStruct')

    output = template.render(Foamdict=FoamFileDict, dict=jsonData)

    # print(output)

    # to save the results
    with open(saveDir+"/OpenFOAMfiles/fvSolutionOutput", "w") as fh:
        fh.write(output)

# =========================================================
