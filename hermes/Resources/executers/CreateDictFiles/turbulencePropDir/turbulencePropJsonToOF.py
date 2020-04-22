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

def turbulencePropOFfunc(jsonData,saveDir):

    # get the path uses before
    import sys
    sysPathList=sys.path

    #find the path of Hermes folder
    HermesDirpath = os.getenv('HERMES_2_PATH')  
    workingDir=HermesDirpath+"/hermes/Resources/executers/CreateDictFiles/"

    # read FoamFile
    with open(workingDir+'turbulencePropDir/templates/FoamFileDict.json', 'r') as myfile:
        data1 = myfile.read()

    # parse FoamFileDict from string to json
    FoamFileDict = json.loads(data1)

    nodeName = 'RASProperties'

    # update FoamFileDict with node name
    FoamFileDict["object"] = nodeName

    # update dict Data

    RAS = jsonData["RAS"]
    # turn true/false into "on/off"
    RAS["turbulence"] = "on" if RAS["turbulence"] else "off"
    RAS["printCoeffs"] = "on" if RAS["printCoeffs"] else "off"

    if "RASModelCoeffs" in RAS:
        RAS = getNestedProperties(RAS, "RASModelCoeffs")


    jsonData["RAS"]=RAS

    # ---------------------------------------------------------


    # define the environment - in this case : templates directory
    file_loader = FileSystemLoader(workingDir+'turbulencePropDir/templates')
    env = Environment(loader=file_loader)

    # call the main file that contain all refernces to others
    template = env.get_template('turbulencePropBasicStruct')

    output = template.render(Foamdict=FoamFileDict, dict=jsonData)

    # print(output)

    # to save the results
    with open(saveDir+"/OpenFOAMfiles/turbulencePropertiesOutput", "w") as fh:
        fh.write(output)

