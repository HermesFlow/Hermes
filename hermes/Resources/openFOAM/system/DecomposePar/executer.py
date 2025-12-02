from ..abstractSystemExecuter import abstractSystemExecuter

class DecomposePar(abstractSystemExecuter):
    def __init__(self, JSON, full_workflow=None):
        super().__init__(JSON, templateName="DecomposePar", full_workflow=full_workflow)