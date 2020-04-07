#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 13 09:48:45 2019

@author: noga
"""

import json
import re
from jinja2 import FileSystemLoader, Environment
import os

# =========================================================

# # read DataFile
# with open('formDataJson.json', 'r') as myfile:
#     data2 = myfile.read()
#
#
# # parse json file into dict
# jsonData = json.loads(data2)

# =========================================================

def list2dict(listVar):
    dictVar = {}
    # loop all items in the list
    i=1
    for item in listVar:
        # 2 keys in each item- name and properties
        keys = list(item.keys())
        # find the key contain the name
        if "ame" in keys[0]:
            nameKey = keys[0]
            nameVal = keys[1]
            # the name set as key in geometryDict, and the properties as the value of that key
            dictVar[item[nameKey]] = item[nameVal]
        elif "ame" in keys[1]:
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

def snappyOFfunc(jsonData,saveDir):

    import os

    # get the path uses before
    import sys
    sysPathList=sys.path

    #find the path of Hermes folder
    HermesDirpath = os.getenv('HERMES_2_PATH')  
    workingDir=HermesDirpath+"/hermes/Resources/executers/CreateDictFiles/"

    #workingDir=os.path.abspath(workingDir)
    # read FoamFile
    with open(workingDir+'snappyHexMeshDictDir/templates/FoamFileDict.json', 'r') as myfile:
        data1 = myfile.read()

    # parse the FoamFileDict from string to json
    FoamFileDict = json.loads(data1)

    nodeName ='snappyHexMeshDict'

    # update FoamFileDict with node name
    FoamFileDict["object"] = nodeName

    # =============================== update dict Data ================================
    # turn true/false into "on/off"
    jsonData["castellatedMesh"] = "on" if jsonData["castellatedMesh"] else "off"
    jsonData["snap"] = "on" if jsonData["snap"] else "off"
    jsonData["addLayers"] = "on" if jsonData["addLayers"] else "off"
    # ------------------------------------------------------------------------------

    # update lists to dict
    # update geometry
    # turn list into a dictionary
    geometry = list2dict(jsonData["geometry"])

    # loop all the geometries
    for geoName,geoValue in geometry.items():
        # create copy to the specific geometry
        updatedGeoVal=geoValue.copy()
        # loop all the keys of the geometry - remove extra data from the keys
        for key in geoValue:
            # split the lower case and upper case
            splitKey=re.findall('[a-zA-Z][^A-Z]*', key)
            # take the first value from the split
            firstSplitKey = splitKey[0]
            # change the key value from its orgininal to the firstSplitKey
            # add the new key value
            updatedGeoVal[firstSplitKey] = geoValue[key]
            # add the old key value
            updatedGeoVal.pop(key)
        # update the updatedGeoVal inside the geometry json
        geometry[geoName]=updatedGeoVal
    # update geometry inside the  jsonData
    jsonData["geometry"] = geometry


    # update castellatedMeshControls
    castellatedMeshControls=jsonData["castellatedMeshControls"]
    castellatedMeshControls["refinementSurfaces"] = list2dict(castellatedMeshControls["refinementSurfaces"])
    castellatedMeshControls["refinementRegions"] = list2dict(castellatedMeshControls["refinementRegions"])
    castellatedMeshControls["features"] = list2dict(castellatedMeshControls["features"])
    jsonData["castellatedMeshControls"] = castellatedMeshControls

    # update layers
    jsonData["layers"] = list2dict(jsonData["layers"])

    # update addLayersControls
    addLayersControls = jsonData["addLayersControls"]
    # turn True/False into "true/false"
    addLayersControls["relativeSizes"] = "true" if addLayersControls["relativeSizes"] else "false"
    jsonData["addLayersControls"]=addLayersControls


    # ------------------------------------------------------------------------------
    # turn True/False into "true/false"
    snap = jsonData["snapControls"]
    snap["explicitFeatureSnap"] = "true" if snap["explicitFeatureSnap"] else "false"
    snap["implicitFeatureSnap"] = "true" if snap["implicitFeatureSnap"] else "false"
    jsonData["snapControls"] = snap

    # ====================================================================================


    # define the environment - in this case : templates directory
    file_loader = FileSystemLoader(workingDir+'snappyHexMeshDictDir/templates')
    env = Environment(loader=file_loader)

    # call the main file that contain all refernces to others
    template = env.get_template('snappyBasicStruct')

    output = template.render(Foamdict=FoamFileDict, dict=jsonData)

    # print(output)

    # to save the results
    with open(saveDir+"/OpenFOAMfiles/snappyOutput", "w") as fh:
        fh.write(output)

# =========================================================
# # make sure the function works
# snappyOFfunc(jsonData,nodeName)
