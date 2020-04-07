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

def transPropOFfunc(jsonData,saveDir):

    # get the path uses before
    import sys
    sysPathList=sys.path

    #find the path of Hermes folder
    HermesDirpath = os.getenv('HERMES_2_PATH')  
    workingDir=HermesDirpath+"/hermes/Resources/executers/CreateDictFiles/"

    # read FoamFile
    with open(workingDir+'transPropDir/templates/FoamFileDict.json', 'r') as myfile:
        data1 = myfile.read()

    # parse FoamFileDict from string to json
    FoamFileDict = json.loads(data1)

    nodeName = "transportProperties"

    # update FoamFileDict with node name
    FoamFileDict["object"] = nodeName

    # update dict Data


    # ---------------------------------------------------------


    # define the environment - in this case : templates directory
    file_loader = FileSystemLoader(workingDir+'transPropDir/templates')
    env = Environment(loader=file_loader)

    # call the main file that contain all refernces to others
    template = env.get_template('transPropBasicStruct')

    output = template.render(Foamdict=FoamFileDict, dict=jsonData)

    # print(output)

    # to save the results
    with open(saveDir+"/OpenFOAMfiles/transportPropertiesOutput", "w") as fh:
        fh.write(output)

