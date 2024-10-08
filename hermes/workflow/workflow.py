import copy
from _io import TextIOWrapper
import os
import json
from itertools import product
import pandas.io.json

from ..taskwrapper import hermes_task_wrapper_home,hermesTaskWrapper
from ..engines import builders
from .expandWorkflow import expandWorkflow
from ..utils.jsonutils import loadJSON
from ..utils.logging import helpers as hermes_logging, get_classMethod_logger

try:
    import mongoengine.base.datastructures as mongoDataStructures
    loadedMongo = True
except ImportError:
    loadedMongo = False


class workflow:
    """
        The role of the workflow task is to load all the tasks and build a network
        of taskWrapper out of a workflow JSON that will actually be initiated in the task engine.

        An example for the workflow JSON is:
        {
            "workflow" : {
                    "root": null,
                    "SolvedFields": "p U k epsilon nut",
                    "AuxFields": "",
                    "Templates": [],
                    "nodeList": : "node3",
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

    BUILDER_LUIGI = "luigi"

    _taskRepresentations = None # A map with nodeName->list of TaskWrappers.
    _workflowJSON = None

    _hermes_task_wrapper_home = None

    @property
    def taskRepresentations(self):
        return self._taskRepresentations

    def __init__(self, workflowJSON,WD_path=None,Resources_path="",name=None):
        """
                Initiates the hermes workflow.

        Parameters
        ----------
        workflowJSON
        WD_path
        Resources_path
        name : str,Optional
            The name of the workflow

        """
        if (loadedMongo):
            # The mongoDB returns a weak reference from the DB, that mkes it a problem to expand.
            # Here, we catch that object and then severe it from the DB by pronting it to str and reading it again...
            # a bit ugly but works.
            if isinstance(workflowJSON,mongoDataStructures.BaseDict):
                workflowJSON = json.loads(json.dumps(workflowJSON))

        workflowJSON = loadJSON(workflowJSON)

        self.name = name
        self.WD_path=WD_path if WD_path is not None else os.getcwd()
        self.Resources_path=Resources_path
        self.logger = hermes_logging.get_logger(self)
        workflowJSON = expandWorkflow().expand(workflowJSON)
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
        logger = get_classMethod_logger(self,"_buildNetworkRepresentations")
        logger.execution(f"Building {taskname}")
        if taskJSON is None:
            raise ModuleNotFoundError(f"Node {taskname} is not found")
        requiredNodeList = [x for x in hermesTaskWrapper.getRequiredTasks(taskJSON) if not (x.startswith("#") or x in ['workflow',''])]

        logger.execution(f"The required nodes for {taskname} are {requiredNodeList}")
        for requirednode in  requiredNodeList:
            if requirednode not in self._taskRepresentations:
                #taskJSON = self._getTaskJSON(requirednode)
                #if taskJSON is not None:

                self._buildNetworkRepresentations(requirednode, self._getTaskJSON(requirednode))

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
        logger = get_classMethod_logger(self,"_buildNetwork")
        self._taskRepresentations = {}
        root_task_name = self.getRootTaskName()
        root_task = self._getTaskJSON(root_task_name)
        # print(root_task)
        # print("--------------------------")

        logger.debug(f"Building network for\n {json.dumps(self._workflowJSON)}")
        self._buildNetworkRepresentations(root_task_name, root_task)


    def getRootTaskName(self):


        rootTaskName = self._workflowJSON["workflow"].get("root",None)
        #rootTaskName = self._workflowJSON.get("root",None)

        if rootTaskName is None:
            # add the finalnode to the workflow.
            rootTaskName = self._createFinalNode()

        return rootTaskName

    def _getTaskJSON(self, nodeName):
        return self._workflowJSON["workflow"]["nodes"].get(nodeName,None)

    def _createFinalNode(self):
        """
            Adds a final node that depends on all nodes in the workflow.

            The final node is a parameters type (really just a stub).

        :return:
            The finalnode name
        """

        finalNodeName = "finalnode_xx"
        #
        # finalnode = dict(name=finalNodeName ,
        #                  typeExecution="generalExecuter.parameterExecuter",
        #                  requires=[x for x in self._workflowJSON["workflow"]["nodes"]],
        #                  #requires=[x for x in self._workflowJSON["nodes"]],
        #                  input_parameters={})

        finalnode = dict(name=finalNodeName ,
                         type="general.Parameters",
                         Execution=dict(
                                        input_parameters={}),
                         GUI=dict(TypeFC={}, Properties={}, WebGui={}),
                         requires=[x for x in self._workflowJSON["workflow"]["nodes"] if x != finalNodeName])

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
        """
            Builds the python code that executes this workflow
        :param buildername:
        :return:
        """
        return builders[buildername.lower()].buildWorkflow(self)

    @property
    def json(self):
        return self._workflowJSON

    @property
    def workflowJSON(self):
        return self._workflowJSON["workflow"]

    @property
    def nodeList(self):
        return self.workflowJSON['nodeList']

    @property
    def nodes(self):
        return self.workflowJSON['nodes']

    def keys(self):
        return self.workflowJSON['nodes'].keys()

    def items(self):
        for ndeName in self.workflowJSON['nodes'].keys():
            yield  (ndeName,self[ndeName])

    def values(self):
        for ndeName in self.workflowJSON['nodes'].keys():
            yield  self[ndeName]

    def __getitem__(self, item):
        """
            Returns a node.
        Parameters
        ----------
        item: str
            The node name

        Returns
        -------
            A node object of the requested node.

        """
        nodeJSON = self.workflowJSON['nodes'][item]
        return hermesNode(item,nodeJSON)


    def __delitem__(self, key):
        """
            Removes a node from the workflow.
            Raises ValueError if node not found.

        Parameters
        ----------
        key: The name of the node

        Returns
        -------
            None

        """

        # 1. Remove the node from the nodelist in key: "workflow.nodeList"
        try:
            self.nodeList.remove(key)

            # 2. Remove the node from the nodes. "workflow.nodes"
            del self.workflowJSON['nodes'][key]

        except ValueError:
            raise ValueError(f"{key} node is not found. Found nodes: {','.join(self.nodeList)}")


    def getNodeValue(self,jsonpath):
        """
            Returns a value from the JSON path.
            The search is relative to the 'nodes' node in the workflow.

        Parameters
        ----------
        jsonpath: str
            The path to obtain.

        Returns
        -------
            List
            jsonpath DatumInContext object with the query results.
        """
        jsonexpr = jsonpath.parse(jsonpath)
        return jsonexpr.find(self._workflowJSON['nodes'])


    def updateNodes(self,parameters : dict):
        """
            Updates the input_parameters of a specific node.

        Parameters
        -----------
        parameters: dict
                A dictionary with the parameters to override the default parameters of the workflow.
                The structure of the dict is :

                {
                    <node name> : {
                            "parameter path 1(eg. a.b.c)" : value,
                            "parameter path 2(eg. a.b.c)" : value
                            .
                            .
                            .
                    }
                }
        :return:
            None
        """
        for nodeName,parameterData in parameters.items():
            if nodeName not in self.nodeList:
                raise ValueError(f"The node {nodeName} is not part of the current nodes. The current nodes are {','.join(self.nodeList)}")

            basePath = f"workflow.nodes.{nodeName}.Execution.input_parameters"
            for parameterPath,parameterValue in parameterData.items():
                fullPath = f"{basePath}.{parameterPath}"
                self.updateNodeValue(fullPath,parameterValue)

    def updateNodeValue(self,jsonpath,value):
        """

            Updates the parametrs in the workflow according to the path.
            Note that a complete path is required.

            To update the input_parameters of a specific node use updateNodes

        Parameters
        ----------
        jsonpath: str
            The path to obtain.

        value: str
            The new value.

        Returns
        -------
            None
        """
        jsonexpr = jsonpath.parse(jsonpath)
        jsonexpr.update(self._workflowJSON['nodes'],value)

    def getNodesParametersTable(self):
        """
            A pandas (table) of  the parameters from all the nodes.
            Returned in a long format. ie.

            nodeName parametersName parameter Value.

        :return:
            pandas.
        """
        paramsList = []
        for nodeName in self.nodeList:
            paramsList.append(self[nodeName].parametersTable)

        return pandas.concat(paramsList)

    @property
    def parametersJSON(self):
        """
            Returns a json with only the parameters of the nodes.
            Used to query the db.
        :return:
            dict

        """
        retdict = dict()
        for node in self.nodeList:
            hermesNode = self[node]
            retdict[node] = hermesNode.parameters

        return retdict


    def _stripGUIandFinalNode(self):
        """
            Return the workflowJSON without the GUI node.

        Returns
        -------

        """
        retJSON = dict(self._workflowJSON)

        del retJSON['workflow']["nodes"]['finalnode_xx']

        for nodeName,nodeData in retJSON['workflow']["nodes"].items():
            if 'GUI' in nodeData:
                del nodeData['GUI']

        return retJSON


    @property
    def solver(self):
        return self.workflowJSON['solver']

    @solver.setter
    def solver(self, value):
        self.workflowJSON['solver'] = value


    def write(self,workflowName=None,directory=None,fullJSON=False):
        """
            Writing the workflow to the disk

            use  workflowName if supplied, else use the name of the workflow
            if the name is not set and the workflowName is not supplied - raise error.

        Parameters
        ----------
        workflowName : str
            optional file name

        directory : str
            optional directory location, else writes to current directory.

        fullJSON  :bool
            If true, return the full JSON (including the final and the GUI nodes)
            otherwise stripthen out

        Returns
        -------

        """


        if workflowName is None and self.name is None:
            raise ValueError("Must supply file name")

        if workflowName is not None:
            if 'json' in workflowName:
                outFileName = workflowName
            else:
                outFileName = f"{workflowName}.json"
        else:
            outFileName = f"{self.name}.json"

        if directory is not None:
            outFileName = os.path.join(directory,outFileName)

        if fullJSON:
            output = self._workflowJSON
        else:
            output = self._stripGUIandFinalNode()

        with open(outFileName,'w') as writeFile:
            json.dump(output,writeFile,indent=4)


class hermesNode:
    """
        An interface to the JSON of an hermes workflow.
    """
    _nodeJSON= None
    _nodeName = None

    def __init__(self,nodeName,nodeJSON):
        self._nodeJSON =nodeJSON
        self._nodeName = nodeName

    def __str__(self):
        return f"Node {self.name} | parameters: \n {json.dumps(self.parameters,indent=4)}"

    def __repr__(self):
        return f"Node {self.name} | parameters: {','.join(self.keys())}"

    @property
    def name(self):
        return self._nodeName

    @property
    def parameters(self):
        return self._nodeJSON['Execution']['input_parameters']

    @property
    def executionJSON(self):
        """
            Return the JSON file without the GUI node.
        Returns
        -------

        """
        return self._nodeJSON['Execution']

    @property
    def parametersTable(self):
        return pandas.json_normalize(self._nodeJSON['Execution']['input_parameters'])\
            .T\
            .reset_index()\
            .rename(columns={'index':'parameterName',0:'value'})\
            .assign(nodeName=self.name)


    def __setitem__(self, item,value):
        self._nodeJSON['Execution']['input_parameters'][item] = value

    def __getitem__(self, item):
        return self._nodeJSON['Execution']['input_parameters'][item]

    def keys(self):
        return self._nodeJSON['Execution']['input_parameters'].keys()

    def values(self):
        return self._nodeJSON['Execution']['input_parameters'].values()

    def items(self):
        return self._nodeJSON['Execution']['input_parameters'].items()

