import pydoc


class LuigiBuilder(object):
    """
        Builds a luigi workflow (a python file)
        from the TaskWrappers of hermes workflow.


        Build the Luigi workflow from TaskWrappers.

            Each task is built using jinja2 and inherits the task.hermesLuigiTask.

                It should build the 3 components of the run:

                - requires
                - output
                - run.

                requires - getRequiredTasks:
                ----------------------------

                    Gets a map from the task outputname->TaskName.
                    [Add all these tasks to the generate Task List].
                    [[ Check if we need a parameter passing to the node from the father]]


                output
                ----------------------------

                    Create a LocalTarget with the name worflow/networkname/[node name][node id].json.
                          It will contain all the data output of the current node.

                run
                ---------------------------
                    Get a map of all the parameters that are required by the
                    executer (getMappingValues).

                    Call the executer with the map values.

                    Write the output of the executer to the output as JSON.

    """

    _mapping = None  # holds the mapping of the [task type]->luigiTaskTransform.

    # uses default convertor if not specified.

    def __init__(self):
        self._mapping = {} # dict(spanParameters=pydoc.locate("Hermes.transform.spanParameters")())
        #self.WD_path=WD_path

    def _getTransformaer(self, tasktype):
        return self._mapping.get(tasktype, pydoc.locate("hermes.engines.luigi.default.transform")())


    def buildWorkflow(self, workflow):

        """
            Converts the workflow to a Luigi python program.


        :param workflow:
            A Hermes.workflow.workflow object.
        :return:
            A str that contains a python luigi program.
        """

        ret = """

import shutil
import os
import luigi
import json 
import sys

sys.path.insert(1, "{{Resources_path}}")
from hermes.engines.luigi.taskUtils import utils as hermesutils

"""
        import jinja2

        rtemplate = jinja2.Environment(loader=jinja2.BaseLoader()).from_string(ret)
        ret=rtemplate.render(Resources_path=workflow.Resources_path)

        print("LuigiBuilder-workflow.WD_path="+workflow.WD_path+"\n")

        for taskname,taskWrapperList in workflow.taskRepresentations.items():
            for taskwrapper in taskWrapperList:
                transformer = self._getTransformaer(taskwrapper.taskType)
                ret += transformer.transform(taskwrapper,workflow.WD_path) + "\n"

        return ret
