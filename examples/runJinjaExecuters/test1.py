import json
import os
import sys

# get the path 
HermesDirpath = os.getenv('HERMES_2_PATH')
print(HermesDirpath)

# insert the path to sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, HermesDirpath)

#import hermes

from hermes.Resources.executers.jinjaExecuter import jinjaExecuter
from hermes.Resources.executers.pythonExecuter import exportFiles


# load json file
path= os.path.abspath("openfoam2.json")
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

    output = (jinjaExecuter().run(**inputs))
    J[nodeValue["name"]] = output


# print values for debug
# for Jkey,Jval in J.items():
#     print("=======================================\n")
#     print("Jkey = " + Jkey + "\n" )
#     print("Jval = \n" + Jval)

# print("J:" + str(J))

# export strings to files
# exportFiles().run(**J)

