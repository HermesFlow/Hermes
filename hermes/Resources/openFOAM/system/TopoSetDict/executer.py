from ..abstractSystemExecuter import abstractSystemExecuter

class TopoSetDict(abstractSystemExecuter):

    def __init__(self, JSON, full_workflow=None):
        super().__init__(JSON, templateName="TopoSetDict", full_workflow=full_workflow)