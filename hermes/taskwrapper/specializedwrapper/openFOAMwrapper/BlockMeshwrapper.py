
from ...wrapper import hermesTaskWrapper

class BlockMeshTaskWrapper(hermesTaskWrapper):

    # def __init__(self,taskname, taskid,  taskJSON, requiredTasks, workflowJSON):
    #     super().__init__(taskname, taskid,  taskJSON, requiredTasks, workflowJSON)
    #     print("got to BlockMeshTaskWrapper __init__")

    @property
    def task_vertices(self):
        return self._taskJSON['GUI'].get('vertices',{})

    @property
    def task_boundary(self):
        return self._taskJSON['GUI'].get('boundary',{})

    def printBlock(self):
        print("got to BlockMeshTaskWrapper.printBlock")