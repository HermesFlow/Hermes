from ..jinjaExecuters import jinjaExecuter

class decomposeparExecuter(jinjaExecuter):

    def run(self, **inputs):

        templateName = "openFOAM/decomposepar"
        template = self._getTemplate(templateName)
        print(inputs)
        output = template.render(**inputs)
        return dict(openFOAMfile=output)
