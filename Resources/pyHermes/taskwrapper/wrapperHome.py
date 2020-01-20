from .wrapper import hermesTaskWrapper

class hermesTaskWrapperHome(object):
    """
        Implements a factory of the wrapper objects available.

    """
    _wrappers = None

    def __contains__(self, item):
        return item in self._wrappers

    def __init__(self):
        """
                Reads the configuration JSON
                and loads the existing wrappers.

                TODO: Extend to load wrappers from other locations as well.
            """

        self._wrappers = dict(spanParameters="pyHermes.taskwrappers.specializedwrapper.spanParameters")

    def getTaskWrapper(self, taskid, taskname, taskJSON, workflowJSON, requiredTasks=None):
        """
                Return an instance of the task represented by the taskJSON

                Matches the executer to the type

            :param taskid:
                An id for the representation of this node representation.

            :param taskJSON:
                A JSON that describes the task.


            :param requiredList:
                A dict of [node name]->[TaskWrapper] that are required by this task.

            :return:
                An instace of the taskwrapper.
            """

        hermesTaskWrapperObj = self._wrappers.get(taskJSON['typeExecution'],hermesTaskWrapper)

        return hermesTaskWrapperObj(taskname=taskname,
                                    taskJSON=taskJSON,
                                    taskid=taskid,
                                    requiredTasks=requiredTasks,
                                    workflowJSON=workflowJSON)
