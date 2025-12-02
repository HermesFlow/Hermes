from ...general import JinjaTransform

class abstractConstantExecuter(JinjaTransform):
    _templateName = None

    def __init__(self, JSON, full_workflow=None):
        super().__init__(JSON, full_workflow=full_workflow)

    def run(self, **inputs):
        return super().run(template=self._templateName, **inputs)
