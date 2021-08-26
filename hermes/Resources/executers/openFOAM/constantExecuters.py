from ..jinjaExecuters import jinjaExecuter

class transportPropertiesExecuter(jinjaExecuter):

    def run(self, **inputs):
        templateName = "openFOAM/constant/transportProperties"
        template = self._getTemplate(templateName)

        effectiveInputs = inputs.get('values',inputs)

        output = template.render(**effectiveInputs)
        return dict(openFOAMfile=output)


class turbulencePropertiesExecuter(jinjaExecuter):

    def run(self, **inputs):
        templateName = "openFOAM/constant/turbulenceProperties"
        template = self._getTemplate(templateName)
        effectiveInputs = inputs.get('values',inputs)
        output = template.render(**effectiveInputs)
        return dict(openFOAMfile=output)
