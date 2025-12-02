from ..abstractConstantExecuter import abstractConstantExecuter

class homogenousWindLogProfileDict(abstractConstantExecuter):
    def __init__(self, JSON, full_workflow=None):
        self._templateName = "openFOAM/constant/homogenousWindLogProfileDict/jinjaTemplate"
        super().__init__(JSON, full_workflow=full_workflow)