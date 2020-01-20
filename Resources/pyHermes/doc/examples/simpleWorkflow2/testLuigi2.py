import json
from pyHermes import hermesWorkflow


def run(workflow_path,WD_path,Resources_path):


    #print("workflow_path"+workflow_path)
    #wf = hermesWorkflow("workflow2.json")
    wf = hermesWorkflow(workflow_path,WD_path,Resources_path)



    print(wf)

    print("===================================")
    #with open("hermes.py","w") as outfile:
    #with open("/home/noga/Downloads/hermes.py","w") as outfile:
    #hermes_path = "/michelangelo/alon/Downloads/FreeCAD/freecad_build_deb/data/Mod/Hermes/Resources/hermes.py"
    hermes_path = WD_path+"/FCtoLuigi.py"
    with open(hermes_path,"w") as outfile:
        outfile.write(wf.build("luigi"))

