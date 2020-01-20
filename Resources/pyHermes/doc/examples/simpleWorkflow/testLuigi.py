import json
from pyHermes import hermesWorkflow


wf = hermesWorkflow("workflow.json")

print(wf)

print("===================================")
with open("hermes.py","w") as outfile:
    outfile.write(wf.build("luigi"))
