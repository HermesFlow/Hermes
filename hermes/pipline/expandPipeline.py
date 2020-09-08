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

        ret = dict(pipeline)
        for node in pipeline["workflow"]["nodes"]:
            print(node)
            template = pipeline["workflow"]["nodes"][node]["Template"]
            newTemplate = self._templateCenter.getTemplate(template)

            for field in ["input_parameters","formData"]:
                newparams = pipeline["workflow"]["nodes"][node].get(field,{})
                if newparams:
                    newTemplate[field].update(newparams)

            ret["workflow"]["nodes"][node]= newTemplate

        return ret

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
