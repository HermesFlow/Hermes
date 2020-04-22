import json
from openFOAM import CopenFOAM

with open('openfoam.json') as json_file:
    openFOAMjson = json.load(json_file)

R=CopenFOAM().buildOpenFOAM(openFOAMjson)
for Rkey,Rval in R.items():
    print("Rkey = " + Rkey + "\n" )
    print("Rval = \n" + Rval)
