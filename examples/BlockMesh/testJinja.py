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

from hermes.Resources.executers.jinjaExecuter import BlockMeshExecuter
# from hermes.Resources.executers.pythonExecuter import exportFiles


# load json file
path= os.path.abspath("HermesWorkflow1.json")
with open(path) as json_file:
    BlockMeshjson = json.load(json_file)

# define dict vars
inputs = {}

BlockMeshNode = BlockMeshjson["workflow"]["nodes"]["BlockMesh"]["GUI"]
templateType= "openFOAM"
casePath = "simpleFOAM"
nodeName = "blockMesh"

# defined 3 argument: template path, values , where to save(name)
inputs["name"] = "system/BlockMesh"
inputs["Properties"] = BlockMeshNode["Properties"]
inputs["boundary"] = BlockMeshNode["boundary"]
inputs["vertices"] = BlockMeshNode["vertices"]
inputs["template"] = "/".join([templateType, casePath, nodeName])
# print(inputs)

# inject input args to jinja executer,
output = BlockMeshExecuter().run(**inputs)

# print values for debug
print("output:")
print(output)

# # export strings to files
# exportFiles().run(**J)

