from ..jinjaExecuters import jinjaExecuter

class decomposeparExecuter(jinjaExecuter):

    def run(self, **inputs):

        templateName = "openFOAM/decomposepar"
        template = self._getTemplate(templateName)
        output = template.render(**inputs)
        return dict(openFOAMfile=output)


class controlDictExecuter(jinjaExecuter):

    def run(self, **inputs):
        templateName = "openFOAM/ControlDict"
        template = self._getTemplate(templateName)
        output = template.render(**inputs)
        return dict(openFOAMfile=output)


