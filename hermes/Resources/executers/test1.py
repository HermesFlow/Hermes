import json
import os
# from openFOAM import CopenFOAM
from jinjaExecuter import jinjaExecuter

# get json file
path= os.path.abspath("programs/openFOAM/openfoam.json")
with open(path) as json_file:
    openFOAMjson = json.load(json_file)

#     to do: figure out how to savr the templates, and hoe to call them
#   1) simpleFoam.system.controlDict
#   2) simpleFoam.controlDict
# are we need 3 argument: template path, values , where to save

inputs={
    "name" : "simpleFoam.controlDict",
    # "name": openFOAMjson["files"]["controlDict"]["name"],
    "values" : openFOAMjson["files"]["controlDict"]["values"]
}

J=jinjaExecuter().run(inputs)
# R=CopenFOAM().buildOpenFOAM(openFOAMjson)
for Jkey,Jval in J.items():
    print("Jkey = " + Jkey + "\n" )
    print("Jval = \n" + Jval)

