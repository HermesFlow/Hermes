from ..jinjaExecuters import jinjaExecuter

class decomposeparExecuter(jinjaExecuter):

    def run(self, **inputs):

        templateName = "openFOAM/system/decomposepar"
        template = self._getTemplate(templateName)
        output = template.render(**inputs)
        return dict(openFOAMfile=output)


class controlDictExecuter(jinjaExecuter):

    def run(self, **inputs):
        templateName = "openFOAM/system/controlDict"
        template = self._getTemplate(templateName)
        output = template.render(**inputs)
        return dict(openFOAMfile=output)


class fvSchemesExecuter(jinjaExecuter):

    def run(self, **inputs):
        templateName = "openFOAM/system/fvSchemes"
        template = self._getTemplate(templateName)
        output = template.render(**inputs)
        return dict(openFOAMfile=output)

class fvSolutionExecuter(jinjaExecuter):

    def run(self, **inputs):
        templateName = "openFOAM/system/fvSolution"
        template = self._getTemplate(templateName)
        output = template.render(**inputs)
        return dict(openFOAMfile=output)


class changeDictionaryExecuter(jinjaExecuter):

    def run(self, **inputs):

        templateName = "openFOAM/system/changeDictionary"
        template = self._getTemplate(templateName)
        output = template.render(**inputs)
        return dict(openFOAMfile=output)
