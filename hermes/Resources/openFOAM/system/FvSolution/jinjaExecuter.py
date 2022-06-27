from ....executers.openFOAM.systemExecuters import systemFileExecuter

class FvSolutionExecuter(systemFileExecuter):

    def __init__(self,JSON):
        super().__init__(JSON,"fvSolution")