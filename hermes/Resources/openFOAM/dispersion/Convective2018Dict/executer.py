from ..abstractDispersionExecuter import abstractDispersionExecuter

class Convective2018Dict(abstractDispersionExecuter):
    def __init__(self,JSON):
        super().__init__(JSON,"IndoorDict")
