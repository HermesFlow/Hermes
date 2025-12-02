from ..abstractSystemExecuter import abstractSystemExecuter

class FvSolution(abstractSystemExecuter):
    def __init__(self, JSON, full_workflow=None):
        super().__init__(JSON, templateName="FvSolution", full_workflow=full_workflow)
