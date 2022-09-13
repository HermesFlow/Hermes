from ..executers.jinjaExecuters import jinjaExecuter

class BC(jinjaExecuter):

    def run(self, **inputs):

        template = self._getTemplate("openFOAM/mesh/BC")
        output = template.render(**inputs)
        return dict(openFOAMfile=output)