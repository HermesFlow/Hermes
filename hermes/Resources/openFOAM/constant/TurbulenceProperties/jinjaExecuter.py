from ....executers.jinjaExecuters import jinjaExecuter

class TurbulencePropertiesExecuter(jinjaExecuter):

    def run(self, **inputs):
        templateName = "openFOAM/constant/turbulenceProperties"
        template = self._getTemplate(templateName)
        effectiveInputs = inputs.get('values',inputs)
        output = template.render(**effectiveInputs)
        return dict(openFOAMfile=output)