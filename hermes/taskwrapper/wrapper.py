import jsonpath_rw_ext as jp
from ..Resources.executers import executerhome
from itertools import chain
import numpy

class hermesTaskWrapper(object):
    """
        The role of the task object wrapper is to serve as a frontend for the transformation to the engine.
        Each node has a metadata that is passed to the executer and to the translator.

        The task include the connectivity of the node in the workflow.
        The actual work is performed by the executer.

        Each task wrapper has a type.
            The type is related to:
                    ** executer
                    ** network behaviour - This decides how to get the network instances of this node.

                    These two are implemented in the implementation of the wrapper.


        The task is defined by the following:

            - name: an ID or a name for a specific node.
            - typeExecution: the execution type of the node.

            - input_parameters (mapping):
                    <parameter name> :  "string1 {[Exp path]|<node name>.[Node path]} string2 ..."


                    [Exp path]  = <workflow|input|output|input_parameters|WebGui>.[Exp path]
                    [Node Path] = <node name>.[Exp path|node path]

            - Properties:
                          a list of constant Properties.

            - requires : a list of required nodes (that not necessarily pass their output to the node).




       The list of node names in the mapping are taken to be
        the 'Required' Tasks in the notation of Luigi.

    """

    @classmethod
    def getRequiredTasks(cls, taskJSON):
        """
            Return the names of the nodes this task depends on.

            returns the list of node names in the parameter_mapping values.

            Also append a dependent node

            :param taskJSON:
                    The JSON definition of the
            :return:
                    A list of nodes that this nodes depends on.
        """
        notNodeTypes = ["workflowJSON","value","output","Properties","WebGui"]

        typesList = []
        for param_path in taskJSON['Execution']['input_parameters'].values():
            if type(param_path)==dict:
                for param_p in param_path.values():
                    typesList.append([x[0].split(".")[0] for x in cls.parsePath(param_p) if x[1]])
            else:
                typesList.append([x[0].split(".")[0] for x in cls.parsePath(param_path) if x[1]])


        # append nodes list in the 'dependent_tasks'
        typesList.append(numpy.atleast_1d(taskJSON.get('requires',[])))

        typesList = [*set([x for x in chain(*typesList)])]
        return [x for x in typesList if x not in notNodeTypes]


    @classmethod
    def parsePath(cls, parameter):
        """
            Determine which parts of the input are path to parse and which
            stay as they are.

            split ...{path}...{path}...
            to
            [(...,False),
             (path,True),
             (...,False),
             (path,True),
             (...,False)]

             True/False - is it path to evaluate or not.

             for example


             batch {path1} b {path2}

             to :
             [("batch ",False),
              ("path1" ,True),

        :param parameter:
                A string of the path.

        :return:
            a list with tokens and a flag that indicates if its a path or not.
        """
        retList = []
        for pot_token in parameter.split("{"):
            if "}" not in pot_token:
                if pot_token != '':
                    retList.append((pot_token,False))
            else:
                rest = pot_token.split("}")
                retList.append((rest[0],True))
                if rest[1] != '':
                    retList.append((rest[1], False))

        return retList

    ## ====================================================================
    ## ====================================================================

    _taskJSON = None  # The json that defines the module.
    _taskid   = None
    _taskname = None

    _workflowJSON = None  # A reference to the overall workflow.

    _executer = None  # the class path of the executer of this
    _requiredTasks = None # a taskname->TaskWrapper dictionary.

    @property
    def taskname(self):
        return self._taskname

    @property
    def taskid(self):
        return self._taskid

    @property
    def taskfullname(self):
        return "%s_%s" % (self._taskname,self._taskid)

    @property
    def taskJSON(self):
        return self._taskJSON

    @property
    def taskType(self):
        return self._taskJSON['Execution']['type']


    @property
    def requiredTasks(self):
        return self._requiredTasks

    @property
    def input_parameters(self):
        return self._taskJSON['Execution']['input_parameters']
        # return self._taskJSON.get("input_parameters", {})

    @property
    def formData(self):
        return self._taskJSON.get("formData", {})

    @property
    def Schema(self):
        return self._taskJSON.get("Schema", {})

    @property
    def files(self):
        return self._taskJSON.get("files", {})

    @property
    def uiSchema(self):
        return self._taskJSON.get("uiSchema", {})

    @property
    def task_Properties(self):
        return self._taskJSON["GUI"]["Properties"]

    @property
    def task_webGui(self):
        return self._taskJSON['GUI'].get('WebGui',{})

    @property
    def task_workflowJSON(self):
        return self._workflowJSON

    def __init__(self,taskname, taskid,  taskJSON, requiredTasks, workflowJSON):
        """
            Initiate a new task wrapper.

        :param taskname:
            The name of the node.

        :param taskid:
            The id of the a task (a sub-name for multiple nodes of the same type).

        :param taskJSON:
            The JSON that defines the task.

        :param requiredList:
            A dictionary of the taskname->TaskWrapper of the
            tasks that are required by this task.
        """
        self._taskJSON = taskJSON
        self._taskid = taskid
        self._taskname = taskname
        self._requiredTasks = requiredTasks
        self._workflowJSON = workflowJSON

    def _queryJSONPath(self, JSONPath):
        """
            Using the JSONPath module to query the

        :param JSONPath:
        :return:
        """
        res = [r for r in jp.match(JSONPath, self.taskJSON)]
        return res[0] if len(res) == 1 else res


    def getExecuterPackage(self):
        return ".".join(executerhome[self.taskType].split(".")[:-1])

    def getExecuterClass(self):
        return executerhome[self.taskType].split(".")[-1]

    def getNetworkTasks(self):
        """
            Return the list of tasks node in the workflow.

            A list is required for tasks that create multiple instances such as spannedParameters.

        :return:
            A list of TaskWrapper objects.
        """
        return [self]


    def __str__(self):
        ret = self.taskfullname +"\n"
        ret += "".join(["\t%s->%s\n" % (key,value.taskfullname) for key,value in self._requiredTasks.items()])
        return ret
