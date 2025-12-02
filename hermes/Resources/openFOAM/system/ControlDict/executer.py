from ..abstractSystemExecuter import abstractSystemExecuter

class ControlDict(abstractSystemExecuter):

    def __init__(self, JSON, full_workflow=None):
        super().__init__(JSON, templateName="ControlDict", full_workflow=full_workflow)

