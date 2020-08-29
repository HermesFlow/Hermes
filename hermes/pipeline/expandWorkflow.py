"""
    Expands the templates in a file to a detaile pipeline file.
    Allow the addition of outer parameter to overwrite existing values of the pipeline.

    Note:
        Check if we want to use jsonpath.
"""
from ..Resources.nodeTemplates.templateCenter import templateCenter
import json

class expandWorkflow():

    _templateCenter = None

    def __init__(self, paths=None):

        self._templateCenter = templateCenter(paths)

    def expand(self, workflowPath):
        """
        Expands a workflow by imbedding the template node to the workflow.

        Parameters
        -----------

            workflowPath: str
                        The path of the workflow

        Returns
        --------
            Dict.
        """
        with open(workflowPath) as json_file:
            workflow = json.load(json_file)

        ret = dict(workflow)
        for node in workflow["workflow"]["nodes"]:
            print(node)
            currentNodeParams = workflow["workflow"]["nodes"][node]
            if "Template" in currentNodeParams:
                newTemplate = self._templateCenter.getTemplate(currentNodeParams["Template"])

                ## Update the execution input_parameters.
                if "Execution" in currentNodeParams:
                    newparams = currentNodeParams["Execution"].get("input_parameters", {})
                    if "input_parameters" in newTemplate["Execution"]:
                        newTemplate["Execution"]["input_parameters"].update(newparams)
                    else:
                        newTemplate["Execution"]["input_parameters"] = newparams

                ## Update the GUI.Properties
                if "GUI" in currentNodeParams:
                    newparams = currentNodeParams["GUI"].get("Properties", {})
                    if "Properties" in newTemplate["GUI"]:
                        newTemplate["GUI"]["Properties"].update(newparams)
                    else:
                        newTemplate["GUI"]["Properties"] = newparams


                ## Update the GUI.WebGui.formData
                if "GUI" in currentNodeParams:
                    if "WebGui" in currentNodeParams["GUI"]:
                        newparams = currentNodeParams["GUI"]["WebGui"].get("formData", {})
                    else:
                        newparams = dict()

                    if "WebGui" in newTemplate["GUI"]:
                        if "formData" in currentNodeParams["GUI"]["WebGui"]:
                            newTemplate["GUI"]["WebGui"]['formData'].update(newparams)
                        else:
                            newTemplate["GUI"]["WebGui"]['formData'] = newparams
                    else:
                        newTemplate["GUI"]["WebGui"] = dict(formData=newparams)

                ret["workflow"]["nodes"][node] = newTemplate

        return ret

    def changeParameters(self, workflow, node, parametersDict):
        """
        Changes the parameters in a node according to the parameters specified in a dictionary.

        Parameters
        ----------
            workflow: The workflow (as dictionary)
            node: The node (string)
            parametersDict: A dictionary of parameters and their values.

        Return
        -------
            dict
            The workflow as a dict.
        """

        for parameter in parametersDict:
            if parameter in workflow["workflow"]["nodes"][node]["input_parameters"]:
                workflow["workflow"]["nodes"][node]["input_parameters"][parameter] = parametersDict[parameter]
            else:
                addresses = parameter.split(".")
                pipe=workflow["workflow"]["nodes"][node]
                for address in addresses[:-1]:
                    if pipe is None:
                        break
                    else:
                        pipe = pipe.get(address)

                pipe[addresses[-1]] = parametersDict[parameter]

        return workflow
