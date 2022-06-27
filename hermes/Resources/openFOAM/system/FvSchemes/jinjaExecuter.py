from ....executers.openFOAM.systemExecuters import systemFileExecuter

class FvSchemesExecuter(systemFileExecuter):

    def __init__(self,JSON):
        super().__init__(JSON,"fvSchemes")