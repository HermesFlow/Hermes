from ....general import JinjaTransform

class FvConstraints(JinjaTransform):
    def __init__(self, JSON, full_workflow=None):
        super().__init__(JSON, templateName="FvConstraints", full_workflow=full_workflow)
