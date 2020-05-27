from _io import TextIOWrapper
import os
import json
from hermes.taskwrapper import hermes_task_wrapper_home
from hermes.taskwrapper import hermesTaskWrapper
from itertools import product
from hermes.engines import builders
from hermes.taskwrapper import hermesTaskWrapper

class hermesWorkflow(dict):
    """
        The role of the workflow task is to load all the tasks and build a network
        of taskWrapper out of a workflow JSON that will actually be initiated in the task engine.

        An example for the workflow JSON is:
        {
            "workflow" : {
                    root : "node3",

                    nodes: {
                        "baseParameters" : {
                            "typeExecution" : "parameters",
                            "WebGUI" : {

                            }
                        },
                        "node1" : {
                                "typeExecution" : "copyDir",
                                "input_parameters": {
                                        "source" : "{WebGUI.formData.source}",
                                        "target" : "{WebGUI.formData.target}",
                                }
                        },
                        "node2" : {
                                "typeExecution" : "executeScript",
                                 "input_parameters": {
                                        "executeDir" : "{node1.target}"
                                        "path"       : ...
                                        "execute"    : "python
                                 }
                        },
                        "node3" : {
                                "typeExecution" : "transformTemplate",
                                "input_parameters" : {
                                        "templates" :
                                }
                    }
            }
        }

        This is the name of the final node of the workflow.

        A taskWrapper is holds all the metadata needed for
        the construction of the task by the appropriate workflow engine (luigi, airflow and ect).

        The taskWrapper holds all the data needed for the initialization of the
        workflow script of the appropriate engine (luigi, airflow and ect).
        Therefore, each node includes the list of nodes it requires.
        If a node generates a list of nodes, then we create a list of nodes
        and multiple nodes that depends on that node.



    """

    _taskRepresentations = None # A map with nodeName->list of TaskWrappers.
    _workflowJSON = None

    _hermes_task_wrapper_home = None

    @property
    def taskRepresentations(self):
        return self._taskRepresentations

    def __init__(self, workflowJSON,WD_path,Resources_path):
        """
                Initiates the hermes workflow.

        :param workflowJSON:
                a json of the workflow.

        """
        if isinstance(workflowJSON,str):
            if os.path.exists(workflowJSON):
                with open(workflowJSON,"r") as infile:
                    workflowJSON = json.load(infile)
            else:
                    workflowJSON = json.loads(workflowJSON)
        elif isinstance(workflowJSON,TextIOWrapper):
            workflowJSON = json.load(workflowJSON)


        self.WD_path=WD_path
        self.Resources_path=Resources_path
        self._workflowJSON = workflowJSON
        self._hermes_task_wrapper_home = hermes_task_wrapper_home
        self._buildNetwork()

    def _buildNetworkRepresentations(self, taskname, taskJSON):
        """
            Get the TaskWrapper instances of the requested node.

            Algorithm:
                1. call _buildNetworkRepresentations for all the required nodes.
                2. Create an TaskWrapper of the taskJSON for all the cross products of
                   the required lists.
                3. Add all TaskWrappers as the representation of this class
                   and return that list

        :param taskJSON:
            The JSON that represents
        :return:
        """

        requiredNodeList = hermesTaskWrapper.getRequiredTasks(taskJSON)
        # for requirednode in requiredNodeList:
        #     if requirednode not in self._taskRepresentations:
        #         self._buildNetworkRepresentations(requirednode, self._getTaskJSON(requirednode))

        # Now build your own network representation.

        ListOfRequiredTaskLists = [[(node,x) for x in self._taskRepresentations[node]] for node in requiredNodeList]

        nodeNetworkRepresentation = []
        for i,combination in enumerate(product(*ListOfRequiredTaskLists)):
            # each combination is a list of tuples (node name,TaskWrapper).
            taskwrp = self._hermes_task_wrapper_home.getTaskWrapper(taskJSON=taskJSON,
                                                                    taskid=i,
                                                                    taskname=taskname,
                                                                    requiredTasks=dict(combination),
                                                                    workflowJSON=self._workflowJSON)
            nodeNetworkRepresentation.append(taskwrp)

        self._taskRepresentations[taskname] = nodeNetworkRepresentation

    def _buildNetwork(self):
        """
            Populates the nodeRepresenations datastructure with the
            appropriate TaskWrappers.

        """
        self._taskRepresentations = {}
        root_task_name = self.getRootTaskName()
        root_task = self._getTaskJSON(root_task_name)

        self._buildNetworkRepresentations(root_task_name, root_task)


    def getRootTaskName(self):


        rootTaskName = self._workflowJSON["workflow"].get("root",None)
        #rootTaskName = self._workflowJSON.get("root",None)

        if rootTaskName is None:
            # add the finalnode to the workflow.
            rootTaskName = self._createFinalNode()

        return rootTaskName

    def _getTaskJSON(self, nodeName):
        return self._workflowJSON["workflow"]["nodes"][nodeName]
        #return self._workflowJSON["nodes"][nodeName]


    def _createFinalNode(self):
        """
            Adds a final node that depends on all nodes in the workflow.

            The final node is a parameters type (really just a stub).

        :return:
            The finalnode name
        """

        finalNodeName = "finalnode_xx"

        finalnode = dict(name=finalNodeName ,
                         typeExecution="parameters",
                         requires=[x for x in self._workflowJSON["workflow"]["nodes"]],
                         #requires=[x for x in self._workflowJSON["nodes"]],
                         input_parameters={})


        self._workflowJSON["workflow"]["nodes"]["finalnode_xx"] =finalnode
        #self._workflowJSON["nodes"]["finalnode_xx"] =finalnode
        return finalNodeName

    def __str__(self):
        ret = ""
        for key,value in self.taskRepresentations.items():
            ret += "\t\t-- %s --\n" % key
            for stask in value:
                ret += str(stask) + "\n"
        return ret


    def build(self,buildername):

        print("self.WD_path="+self.WD_path+"\n")
        
        return builders[buildername.lower()].buildWorkflow(self)


