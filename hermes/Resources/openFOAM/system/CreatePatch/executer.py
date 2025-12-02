from ..abstractSystemExecuter import abstractSystemExecuter

class CreatePatch(abstractSystemExecuter):
    def __init__(self, JSON, full_workflow=None):
        super().__init__(JSON, templateName="CreatePatch", full_workflow=full_workflow)
