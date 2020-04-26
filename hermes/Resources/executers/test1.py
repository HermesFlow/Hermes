import json
import os
# from openFOAM import CopenFOAM
from jinjaExecuter import jinjaExecuter

# get json file
path= os.path.abspath("programs/openFOAM/openfoam.json")
with open(path) as json_file:
    openFOAMjson = json.load(json_file)

#     to do: figure out how to save the templates, and how to call them
#   1) simpleFoam.system.controlDict
#   2) simpleFoam.controlDict
# are we need 3 argument: template path, values , where to save
inputs={}
J={}
for nodeKey,nodeValue in openFOAMjson["files"].items():
    # inputs["name"]="simpleFoam.controlDict"
    inputs["name"]=nodeValue["name"]
    inputs["values"]=nodeValue["values"]
    inputs["template"]="/".join([openFOAMjson["casePath"],nodeKey])
    J.update(jinjaExecuter().run(inputs))

# R=CopenFOAM().buildOpenFOAM(openFOAMjson)
for Jkey,Jval in J.items():
    print("=======================================\n")
    print("Jkey = " + Jkey + "\n" )
    print("Jval = \n" + Jval)

