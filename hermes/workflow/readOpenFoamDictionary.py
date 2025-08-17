
from PyFoam.RunDictionary.ParsedParameterFile import ParsedParameterFile
from ..Resources.reTemplateCenter import templateCenter
from hermes.workflow.expandWorkflow import expandWorkflow
from ..utils.logging import get_classMethod_logger
from hermes.utils.jsonutils import loadJSON

import copy
import json
import os
from PyFoam.Basics.DataStructures import BoolProxy
import collections.abc
import pydoc

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

# ********************************************************************
def locateClass(path):
    ''' try locate class using pydoc.locate
        return class if found, or None and err '''
    e = None
    try:
        nodecls = pydoc.locate(path)
    except Exception as ex:
        nodecls = None
        e = ex

    return nodecls, e

class readDictionary:

    def __init__(self, dictionaryPath, workflowJSONPath):
        self.ppf = self.readOneDictionary(dictionaryPath)
        self.dictData = self.getDictionaryData()
        self.dictName = self.getDictionaryName()

        paths = None
        self._templateCenter = templateCenter(paths)
        self.TemplateData = self.updateTemplateData()
        self.updateJsonFromDictionary()

        workflowJSON = loadJSON(workflowJSONPath)
        self.expandWorkflow = expandWorkflow().expand(workflowJSON)

        # self.expandData = None

        # print("------: self.expandData")
        # print(self.expandData)

    @property
    def templateCenter(self):
        return self._templateCenter

    def readOneDictionary(self, DictionaryPath):

        # read the dictionat to python object
        ppf = ParsedParameterFile(DictionaryPath)
        return ppf

    def getDictionaryName(self):

        # get dictinary name
        nodeName = self.ppf.header["object"]

        if nodeName:
            nodeName_capital = nodeName[0].upper() + nodeName[1:]
        else:
            nodeName_capital = nodeName
        return nodeName_capital

    def getDictionaryData(self):

        # get the parameters of the dictionary
        dictData = copy.deepcopy(self.ppf.content)

        return dictData

    def updateTemplateData(self):
        # upload JSON Templatte of the node
        node_type = "openFOAM.system.ControlDict"
        fullNodeData = dict(self._templateCenter[node_type])
        # expandWorkflow.updateMap(fullNodeData, self.dictData)
        return fullNodeData


    def updateMap(self, destinationMap, templateMap):
        logger = get_classMethod_logger(self, "updateMap")
        for sourceKey, sourceValue in templateMap.items():
            logger.debug(f"Processing key {sourceKey} with value {sourceValue}")
            if isinstance(sourceValue, collections.abc.Mapping):
                logger.debug(f"Key is a mapping in template. It is a {destinationMap.get(sourceKey, {})} in destination, calling recursively")
                destinationMap[sourceKey] = self.updateMap(destinationMap.get(sourceKey, {}), sourceValue)
            else:
                logger.debug(f"Key is not a map, setting key {sourceKey} with value {sourceValue} (-{destinationMap}-)")
                destinationMap[sourceKey] = sourceValue
        return destinationMap

    def updateJsonFromDictionary(self):
        nodeClass = self.getNodeCalss()
        if nodeClass[0] is None:
            print("nodeClass has not been found:" + str(nodeClass[1]))
            return
        print("----------------------------------------")
        print(nodeClass)
        print("----------------------------------------")
        destJson = dict(name="Serah", age=13)
        sourceJson = dict(name="pedro", age=4, color="blue")
        print(destJson)
        nodeClass[0].updateDictionaryToJson(destJson, sourceJson)
        print(destJson)



    def getNodeCalss(self):
        dir = "hermes.Resources"
        outerType = ["openFOAM", "general"]
        innerType = ["constant", "mesh", "system", "dispersion", ""]
        found_flag = False
        for outerT in outerType:
            for innerT in innerType:
                path = os.path.join(dir, outerT, innerT, self.dictName, "convertData", "copyData" + self.dictName)
                path = path.replace("/", ".")
                nodeClass = locateClass(path)
                # print("gen: " + path)
                # print("is:  hermes.Resources.openFOAM.system.ControlDict.convertData.copyDataControlDict")
                # print(nodeClass)

                if nodeClass[0] is not None:
                    found_flag = True
                    break

            if found_flag:
                break

        return nodeClass



