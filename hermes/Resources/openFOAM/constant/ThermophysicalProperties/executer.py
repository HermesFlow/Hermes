from ..abstractConstantExecuter import abstractConstantExecuter

class ThermophysicalProperties(abstractConstantExecuter):
    def __init__(self,JSON):
        super().__init__(JSON,"ThermophysicalProperties")
