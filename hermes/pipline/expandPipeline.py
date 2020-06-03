"""
    Expands the templates in a file to a detaile pipeline file.
    Allow the addition of outer parameter to overwrite existing values of the pipeline.

    Note:
        Check if we want to use jsonpath.
"""
from ..Resources.nodeTemplates.templateCenter import templateCenter
import json

class expandPipeline():

    _templateCenter = None

    def __init__(self, paths=None):

        self._templateCenter = templateCenter(paths)

    def expand(self, pipelinePath, parametersPath = None):
        """
        Returns an expanded template - replace the templates names with the full templates,
        and change the parameters to the requested parameters.
        params:
            pipelinePath: The path of the pipeline (string)
            parametersPath: Optional, a path of a parameters json file.
        Returns:
            The expanded pipeline as a dict.
        """
        with open(pipelinePath) as json_file:
            pipeline = json.load(json_file)
        if parametersPath is not None:
            with open(parametersPath) as json_file:
                parameters = json.load(json_file)
        parameters = None if parametersPath is None else parameters

        for node in pipeline["workflow"]["nodes"]:
            template = pipeline["workflow"]["nodes"][node]["Template"]
            parametersDict = None
            if "input_parameters" in pipeline["workflow"]["nodes"][node]:
                parametersDict = pipeline["workflow"]["nodes"][node]["input_parameters"]
                del pipeline["workflow"]["nodes"][node]["input_parameters"]
            pipeline["workflow"]["nodes"][node] = self._templateCenter.getTemplate(template)
            if parametersDict is not None:
                pipeline = self.changeParameters(pipeline, node, parametersDict)
            if parameters is not None:
                pipeline = self.changeParameters(pipeline,node,parameters)
        return pipeline

    def changeParameters(self, pipeline, node, parametersDict):
        """
        Changes the parameters in a node according to the parameters specified in a dictionary.
        Params:
            pipeline: The pipeline (as dictionary)
            node: The node (string)
            parametersDict: A dictionary of parameters and their values.
        Returns:
            The pipeline as a dict.
        """

        for parameter in parametersDict:
            if parameter in pipeline["workflow"]["nodes"][node]["input_parameters"]:
                pipeline["workflow"]["nodes"][node]["input_parameters"][parameter] = parametersDict[parameter]
            else:
                addresses = parameter.split(".")
                pipe=pipeline["workflow"]["nodes"][node]
                for address in addresses[:-1]:
                    if pipe is None:
                        break
                    else:
                        pipe = pipe.get(address)

                pipe[addresses[-1]] = parametersDict[parameter]

        return pipeline
