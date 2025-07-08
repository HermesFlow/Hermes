
from PyFoam.RunDictionary.ParsedParameterFile import ParsedParameterFile
from ..Resources.reTemplateCenter import templateCenter

import copy

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
        fullNodeData = dict(templateCenter[node_type])
        expand.updateMap(fullNodeData, self.dictData)