from ..abstractConstantExecuter import abstractConstantExecuter

class TurbulenceProperties(abstractConstantExecuter):

    def __init__(self, JSON, full_workflow=None):
        self._templateName = "openFOAM/constant/TurbulenceProperties/jinjaTemplate"
        super().__init__(JSON, full_workflow=full_workflow)

    # def run(self, **inputs):
    #     templateName = "openFOAM/constant/TurbulenceProperties/jinjaTemplate"
    #     template = self._getTemplate(templateName)
    #     effectiveInputs = inputs.get('values',inputs)
    #     output = template.render(**effectiveInputs)
    #     return dict(openFOAMfile=output)