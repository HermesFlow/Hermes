from ..abstractDispersionExecuter import abstractDispersionExecuter

class IndoorDict(abstractDispersionExecuter):
    def __init__(self,JSON):
        super().__init__(JSON,"IndoorDict")
