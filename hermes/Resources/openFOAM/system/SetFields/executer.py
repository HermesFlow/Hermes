from ..abstractSystemExecuter import abstractSystemExecuter

class SetFields(abstractSystemExecuter):
    def __init__(self, JSON, full_workflow=None):
        super().__init__(JSON, templateName="SetFields", full_workflow=full_workflow)

