from ..abstractSystemExecuter import abstractSystemExecuter

class FvSchemes(abstractSystemExecuter):
    def __init__(self, JSON, full_workflow=None):
        super().__init__(JSON, templateName="FvSchemes", full_workflow=full_workflow)
