#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 13 09:48:45 2019

@author: noga
"""

import json
from jinja2 import FileSystemLoader, Environment

# read files

# FoamFile
with open('templates/FoamFileDict.json', 'r') as myfile:
    data1 = myfile.read()
nodeName='snappyHexMeshDict'

# DataFile
with open('formDataJson.json', 'r') as myfile:
    data2 = myfile.read()

# parse json file into dict
FoamFileDict = json.loads(data1)
jsonData = json.loads(data2)
# print(jsonData)

# update FoamFileDict with node name
FoamFileDict["object"] = nodeName

# =============================== update dict Data ================================
# turn true/false into "on/off"
jsonData["castellatedMesh"] = "on" if jsonData["castellatedMesh"] else "off"
jsonData["snap"] = "on" if jsonData["snap"] else "off"
jsonData["addLayers"] = "on" if jsonData["addLayers"] else "off"
# ------------------------------------------------------------------------------
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
# ------------------------------------------------------------------------------
# update lists to dict
jsonData["geometry"] = list2dict(jsonData["geometry"])

castellatedMeshControls=jsonData["castellatedMeshControls"]

castellatedMeshControls["refinementSurfaces"] = list2dict(castellatedMeshControls["refinementSurfaces"])
castellatedMeshControls["refinementRegions"] = list2dict(castellatedMeshControls["refinementRegions"])

castellatedMeshControls["features"] = list2dict(castellatedMeshControls["features"])


jsonData["castellatedMeshControls"] = castellatedMeshControls

# ------------------------------------------------------------------------------



# ====================================================================================


# define the environment - in this case : templates directory
file_loader = FileSystemLoader('templates')
env = Environment(loader=file_loader)



# call the main file that contain all refernces to others
template = env.get_template('snappyBasicStruct')

output = template.render(Foamdict=FoamFileDict, dict=jsonData)
# output = templates.render(Foamdict=FoamFileDict)

print(output)

# to save the results
with open("output.txt", "w") as fh:
    fh.write(output)

