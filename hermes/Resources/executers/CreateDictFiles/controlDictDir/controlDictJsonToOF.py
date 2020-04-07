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


def controlDictOFfunc(jsonData,saveDir):

    #import os
    #WD_path=os.getcwd()
    
    # get the path uses before
    import sys
    sysPathList=sys.path

    #find the path of Hermes folder
    HermesDirpath = os.getenv('HERMES_2_PATH')  
    workingDir=HermesDirpath+"/hermes/Resources/executers/CreateDictFiles/"

    # read FoamFile

    with open(workingDir+'controlDictDir/templates/FoamFileDict.json', 'r') as myfile:
        data1 = myfile.read()

    # parse FoamFileDict from string to json
    FoamFileDict = json.loads(data1)

    nodeName = 'controlDict'

    # update FoamFileDict with node name
    FoamFileDict["object"] = nodeName

    # update dict Data
    # make True/False to on/off
    jsonData["writeCompression"] = "on" if jsonData["writeCompression"] else "off"
    # make True/False to true/false
    jsonData["runTimeModifiable"] = "true" if jsonData["runTimeModifiable"] else "false"
    jsonData["interpolate"] = "true" if jsonData["interpolate"] else "false"



    # update the function structure in the json
    funcStruct = {}
    if len(jsonData["functions"]) == 0:
        jsonData["functions"] = {}
    else:
        # upload the file data
        for func in jsonData["functions"]:
            path=workingDir+"controlDictDir/"+func
            with open(path, 'r') as myfile:
                funcData = myfile.read()

            funcKey = func.split(".")[0]
            # add the file data to the func structure
            funcStruct[funcKey] = funcData
        # update the data in the main json
        jsonData["functions"] = funcStruct

        # print("funcStruct="+str(funcStruct))



    # define the environment - in this case : templates directory
    file_loader = FileSystemLoader(workingDir+'controlDictDir/templates')
    env = Environment(loader=file_loader)

    # call the main file that contain all refernces to others
    template = env.get_template('controlDictBasicStruct')

    output = template.render(Foamdict=FoamFileDict, dict=jsonData)

    # print(output)

    # to save the results
    with open(saveDir+"/OpenFOAMfiles/controlDictOutput", "w") as fh:
        fh.write(output)

