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
import hermes.utils.logging.helpers as hera_logging
from importlib.resources import read_text
# import FreeCAD


class expandWorkflow:
    """ this class is taking a json with reference
      to other files , end inject the data from those other
      files into that json """

    def updateMap(self,d, u):
        for k, v in u.items():
            if isinstance(v, collections.abc.Mapping):
                d[k] = self.updateMap(d.get(k, {}), v)
            else:
                d[k] = v
        return d


    @property
    def templateCenter(self):
        return self._templateCenter 

    def __init__(self):
        self.TEMPLATE = "Template"
        self.IMPORTJSONFROMFILE = "importJsonfromfile"
        self.logger = hera_logging.get_logger(self)
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
        self.logger.info("---------------- Start ------------")
        self.logger.debug(f"Got templateJSON : {templateJSON}")
        JsonObjectfromFile = loadJSON(templateJSON)
        nodeList = JsonObjectfromFile["workflow"]["nodeList"]
        nodes = JsonObjectfromFile["workflow"]["nodes"]

        for nodeName,nodeData in nodes.items():
            self.logger.execution(f"Processing node {nodeName}")
            if nodeName in nodeList:
                self.logger.debug(f"Node {nodeName} in the list")
                fullNodeData = dict(self._templateCenter[nodeData['type']])
                self.updateMap(fullNodeData,nodeData)

                JsonObjectfromFile["workflow"]["nodes"][nodeName] = fullNodeData
            else:
                err = f"The {nodeName} exists in node list but is not specified in nodes. Abort! "
                self.logger.err(err)
                raise ValueError(err)

        self.logger.debug(json.dumps(JsonObjectfromFile,indent=4))
        self.logger.info("--------------- End --------------")
        return JsonObjectfromFile
