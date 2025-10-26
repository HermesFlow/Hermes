"""
    Expands the templates in a file to a detaile pipeline file.
    Allow the addition of outer parameter to overwrite existing values of the pipeline.

    Note:
        Check if we want to use jsonpath.
"""
# from ..Resources.nodeTemplates.old.templateCenter import templateCenter
from ..Resources.reTemplateCenter import templateCenter
import json
import os
import collections.abc
from ..utils.jsonutils import loadJSON
from ..utils.logging import get_classMethod_logger
from importlib.resources import read_text
# import FreeCAD


class expandWorkflow:
    """ this class is taking a json with reference
      to other files , end inject the data from those other
      files into that json """

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


    @property
    def templateCenter(self):
        return self._templateCenter 

    def __init__(self):
        self.TEMPLATE = "Template"
        self.IMPORTJSONFROMFILE = "importJsonfromfile"
        paths = None
        self._templateCenter = templateCenter(paths)


        self.cwd = ""
        self.WD_path = ""

    def expandBatch(self, templateJSON, parameters={}):
        """
        Expamd workflow and remove the GUI part
        Parameters
        ----------
        templateJSON
        parameters

        Returns
        -------

        """

        JsonObjectBatch = self.expand(templateJSON,parameters)
        for nodeKey, nodeVal in JsonObjectBatch["workflow"]["nodes"].items():
            if "GUI" in nodeVal.keys():
                nodeVal.pop("GUI")

        ret = self.updateMap(JsonObjectBatch, parameters)

        return ret


    def expand(self, templateJSON, parameters={}):
        """
        Expands a workflow by imbedding the template node to the workflow.

        Parameters
        -----------

            templateJSON: str, dict
                        The path of the workflow json, a json str or a json obj

            parameters : dict
                        A dictionary that can overwrite the template defaults.
                        Adds the values to the dictionary if necessary

        Returns
        --------
            Dict.
        """
        logger = get_classMethod_logger(self,"expand")
        logger.info("---------------- Start ------------")
        logger.debug(f"Got templateJSON : {templateJSON}")
        JsonObjectfromFile = loadJSON(templateJSON)
        #nodeList = JsonObjectfromFile["workflow"]["nodeList"]
        nodes = JsonObjectfromFile["workflow"]["nodes"]

        for nodeName,nodeData in nodes.items():
            logger.info(f"Processing node {nodeName}")
            logger.debug(f"Node {nodeName} in the list, using type {nodeData['type']} ")
            fullNodeData = dict(self._templateCenter[nodeData['type']])
            logger.debug(f"Got template, now updating map {fullNodeData}")
            self.updateMap(fullNodeData,nodeData)

            fullNodeData["type"] = nodeData.get("type", fullNodeData.get("type"))

            JsonObjectfromFile["workflow"]["nodes"][nodeName] = fullNodeData

        logger.debug(json.dumps(JsonObjectfromFile,indent=4))
        logger.info("--------------- End --------------")
        return JsonObjectfromFile
