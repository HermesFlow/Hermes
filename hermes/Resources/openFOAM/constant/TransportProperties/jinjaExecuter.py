from ....executers.jinjaExecuters import jinjaExecuter

class transportPropertiesExecuter(jinjaExecuter):

    def run(self, **inputs):
        templateName = "jinjaTemplate"
        template = self._getTemplate(templateName)

        effectiveInputs = inputs.get('values',inputs)

        output = template.render(**effectiveInputs)
        return dict(openFOAMfile=output)