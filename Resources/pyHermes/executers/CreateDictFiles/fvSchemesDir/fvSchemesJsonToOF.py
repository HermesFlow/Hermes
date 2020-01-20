#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 13 09:48:45 2019

@author: noga
"""

import json
from jinja2 import FileSystemLoader, Environment

# =========================================================

# # read DataFile
# with open('formDataJson.json', 'r') as myfile:
#     data2 = myfile.read()
#
# # parse json
# jsonData = json.loads(data2)
#

# =========================================================

def fvSchemeOFfunc(jsonData,saveDir):

    # get the path uses before
    import sys
    sysPathList=sys.path

    #find the path of the FreeCAD Resource folder
    import re
    for path in sysPathList:
        m = re.search('Mod/Hermes/Resources/',path)
        if m is not None:
            Resources_path=path
    
    workingDir=Resources_path+"pyHermes/executers/CreateDictFiles/"

    # read file -FoamFile
    with open(workingDir+'fvSchemesDir/templates/FoamFileDict.json', 'r') as myfile:
        data1 = myfile.read()

    # parse json file into dict
    FoamFileDict = json.loads(data1)

    nodeName = 'fvSchemes'

    # update FoamFileDict with node name
    FoamFileDict["object"] = nodeName

    # update dict Data
    divSchemes = jsonData["divSchemes"]
    # check if there are additional properties
    if ("more divSchemes properties" in divSchemes) and (len(divSchemes["more divSchemes properties"])>0) :
        # loop the properties and add them to the divSchemes object
        for key,val in divSchemes["more divSchemes properties"].items():
            divSchemes[key] = val
        # remove "more divSchemes properties" from the divSchemes
        divSchemes.pop("more divSchemes properties")
    # update the jsonData structure
    jsonData["divSchemes"] = divSchemes




    # define the environment - in this case : templates directory
    file_loader = FileSystemLoader(workingDir+'fvSchemesDir/templates')
    env = Environment(loader=file_loader)

    # call the main file that contain all refernces to others
    template = env.get_template('fvSchemesBasicStruct')

    output = template.render(Foamdict=FoamFileDict, dict=jsonData)
    # output = templates.render(Foamdict=FoamFileDict)

    # print(output)

    # to save the results
    with open(saveDir+"/OpenFOAMfiles/fvSchemesOutput", "w") as fh:
        fh.write(output)

# =========================================================
# # call the function to make sure it works
# fvSchemeOFfunc(jsonData,nodeName)
