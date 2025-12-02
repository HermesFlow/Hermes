from ..abstractConstantExecuter import abstractConstantExecuter

class physicalProperties(abstractConstantExecuter):

    def __init__(self, JSON, full_workflow=None):
        self._templateName = "openFOAM/constant/physicalProperties/jinjaTemplate"
        super().__init__(JSON, full_workflow=full_workflow)
