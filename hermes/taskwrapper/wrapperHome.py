from .wrapper import hermesTaskWrapper

from pydoc import locate
# from . import specializedwrapper


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

        self._wrappers = {}

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

        # print("-----------------------")
        # print("taskid: " + str(taskid))
        # print("taskname: " + str(taskname))
        # print("taskJSON: " + str(taskJSON))
        # print("-----------------------")
        try:
            if "template" in taskJSON['Execution']["input_parameters"]:
                # add wrapper to path - and creste new full path
                specializedName = taskname + "TaskWrapper"
                specializedPath = taskJSON['Execution']["input_parameters"]['template']
                splitPath = specializedPath.split("/")
                wrapperPath = [element + "wrapper" for element in splitPath]
                specializedPath =  "hermes.taskwrapper.specializedwrapper." + ".".join(wrapperPath)
                full = specializedPath + "." + specializedName

                # try locate the package
                specializedPack = locate(full)
                if specializedPack is not None:
                    hermesTaskWrapperObj = self._wrappers.get(taskJSON['type'], specializedPack)
                else:
                    hermesTaskWrapperObj = self._wrappers.get(taskJSON['type'], hermesTaskWrapper)
            else:
                hermesTaskWrapperObj = self._wrappers.get(taskJSON['type'], hermesTaskWrapper)
        except KeyError as e:
            raise KeyError(f"Missing data in processing Node {taskname}: {taskJSON}. Error is {e}")


        return hermesTaskWrapperObj(taskname=taskname,
                                    taskJSON=taskJSON,
                                    taskid=taskid,
                                    requiredTasks=requiredTasks,
                                    workflowJSON=workflowJSON)


