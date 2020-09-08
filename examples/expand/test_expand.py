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
from hermes.pipline import expandPipeline



# load json file
path= os.path.abspath("simpleFOAMexpandFC.json")
with open(path) as json_file:
    expandjson = json.load(json_file)

# define dict vars
x = {}
# expend=expandPipeline.expandPipeline(path)
x = expandPipeline.expandPipeline().expand(path)


# for nodeKey,nodeValue in expandjson["workflow"]["nodes"].items():
#     if "Template" in nodeValue:
#         overide= nodeValue.copy()
#         overide.pop("Template")
#         print("Template =" + str(nodeValue["Template"]) + "; overide = " + str(overide) +"\n")
#         x=expandPipeline.expandPipeline(nodeValue["Template"])
#         x.expandPipeline.expand(nodeValue["Template"],overide if len(overide)!= 0 else None)
#
#         expandjson["workflow"]["nodes"][nodeKey]=x



# print values for debug
for Jkey,Jval in x["workflow"]["nodes"].items():
    print("=======================================\n")
    print("Jkey = " + Jkey + "\n" )
    print("Jval = \n" + str(Jval))

# print("J:" + str(J))

# save file to the selected place
with open("afterexpand.json", "w") as write_file:
    json.dump(x, write_file, indent=4)  # indent make it readable



