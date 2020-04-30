import json
import os
from jinjaExecuter import jinjaExecuter

# load json file
path= os.path.abspath("programs/openFOAM/openfoam2.json")
with open(path) as json_file:
    openFOAMjson = json.load(json_file)

# define dict vars
inputs={}
J={}

for nodeKey,nodeValue in openFOAMjson["files"].items():

    # defined 3 argument: template path, values , where to save(name)
    inputs["name"]=nodeValue["name"]
    inputs["values"]=nodeValue["values"]
    inputs["template"]="/".join([openFOAMjson["casePath"],nodeKey])

    # inject input args to jinja executer,
    # save the rendered data into J
    J.update(jinjaExecuter().run(inputs))

# print values for debug
for Jkey,Jval in J.items():
    print("=======================================\n")
    print("Jkey = " + Jkey + "\n" )
    print("Jval = \n" + Jval)

