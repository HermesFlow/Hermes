from ..abstractSystemExecuter import abstractSystemExecuter

class MeshQualityDict(abstractSystemExecuter):

    def __init__(self, JSON, full_workflow=None):
        super().__init__(JSON, templateName="MeshQualityDict", full_workflow=full_workflow)
