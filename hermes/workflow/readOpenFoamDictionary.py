
from PyFoam.RunDictionary.ParsedParameterFile import ParsedParameterFile
from ..Resources.reTemplateCenter import templateCenter

import copy
import json
from PyFoam.Basics.DataStructures import BoolProxy

class FoamJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, BoolProxy):
            return bool(o)
        return super().default(o)

def saveJson(data, saveName):
    with open(saveName, "w", encoding="utf-8") as f:
        json.dump(
            data,
            f,
            indent=4,
            sort_keys=True,
            ensure_ascii=False,
            cls=FoamJSONEncoder
        )

class readDictionary:

    def __init__(self, dictionaryPath, JsonTemplatePath):
        self.ppf = self.readOneDictionary(dictionaryPath)
        self.dictData = self.getDictionaryData()
        paths = None
        self._templateCenter = templateCenter(paths)

    def readOneDictionary(self, DictionaryPath):

        # read the dictionat to python object
        ppf = ParsedParameterFile(DictionaryPath)
        return ppf

    def getDictionaryName(self):

        # get dictinary name
        nodeName = self.ppf.header["object"]

        return nodeName

    def getDictionaryData(self):

        # get the parameters of the dictionary
        dictData = copy.deepcopy(self.ppf.content)

        return dictData

    def updateJsonFromDictionary(self):
        # upload JSON Templatte of the node
        node_type = "openFOAM.system.ControlDict"
        fullNodeData = dict(self._templateCenter[node_type])
        expand.updateMap(fullNodeData, self.dictData)



