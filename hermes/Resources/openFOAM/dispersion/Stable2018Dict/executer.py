from ..abstractDispersionExecuter import abstractDispersionExecuter

class Stable2018Dict(abstractDispersionExecuter):
    def __init__(self,JSON):
        super().__init__(JSON,"IndoorDict")
