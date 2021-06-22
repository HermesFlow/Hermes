from ..jinjaExecuters import jinjaExecuter

class decomposeparExecuter(jinjaExecuter):

    def run(self, **inputs):

        templateName = "openFOAM/system/decomposepar"
        template = self._getTemplate(templateName)
        output = template.render(**inputs)
        return dict(openFOAMfile=output)


class controlDictExecuter(jinjaExecuter):

    def run(self, **inputs):
        templateName = "openFOAM/system/ControlDict"
        template = self._getTemplate(templateName)
        output = template.render(**inputs)
        return dict(openFOAMfile=output)


class fvSchemesExecuter(jinjaExecuter):

    def run(self, **inputs):
        templateName = "openFOAM/system/FvSchemes"
        template = self._getTemplate(templateName)
        output = template.render(**inputs)
        return dict(openFOAMfile=output)

class fvSolutionExecuter(jinjaExecuter):

    def run(self, **inputs):
        templateName = "openFOAM/system/FvSolution"
        template = self._getTemplate(templateName)
        output = template.render(**inputs)
        return dict(openFOAMfile=output)
