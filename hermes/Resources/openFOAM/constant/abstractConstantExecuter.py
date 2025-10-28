from ...general import JinjaTransform

class abstractConstantExecuter(JinjaTransform):
    _templateName = None

    def __init__(self,JSON,templateName):
        super().__init__(JSON)
        self.templateName =f"openFOAM/constant/{templateName}/jinjaTemplate"

    def run(self, **inputs):
        inputs = inputs or {}
        inputs.setdefault("template", self.templateName)
        return super().run(**inputs)


