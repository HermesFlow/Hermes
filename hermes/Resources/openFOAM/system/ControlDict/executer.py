from ....executers.openFOAM.systemExecuters import systemFileExecuter

class controlDictExecuter(systemFileExecuter):

    def __init__(self,JSON):
        super().__init__(JSON,"controlDict")