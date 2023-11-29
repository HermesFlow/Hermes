from ..abstractConstantExecuter import abstractConstantExecuter

class momentumTransport(abstractConstantExecuter):

    def __init__(self,JSON):
        super().__init__(JSON,"momentumTransport")

    # def run(self, **inputs):
    #     templateName = "openFOAM/constant/TurbulenceProperties/jinjaTemplate"
    #     template = self._getTemplate(templateName)
    #     effectiveInputs = inputs.get('values',inputs)
    #     output = template.render(**effectiveInputs)
    #     return dict(openFOAMfile=output)