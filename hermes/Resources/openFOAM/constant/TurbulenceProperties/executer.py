from ..abstractConstantExecuter import abstractConstantExecuter

class TurbulenceProperties(abstractConstantExecuter):

    def __init__(self,JSON):
        super().__init__(JSON,"TurbulenceProperties")

    # def run(self, **inputs):
    #     templateName = "openFOAM/constant/TurbulenceProperties/jinjaTemplate"
    #     template = self._getTemplate(templateName)
    #     effectiveInputs = inputs.get('values',inputs)
    #     output = template.render(**effectiveInputs)
    #     return dict(openFOAMfile=output)