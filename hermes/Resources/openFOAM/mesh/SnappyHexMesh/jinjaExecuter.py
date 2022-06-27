from ....executers.jinjaExecuters import jinjaExecuter

class SnappyHexMeshExecuter(jinjaExecuter):

    def run(self, **inputs):

        template = self._getTemplate("openFOAM/mesh/SnappyHexMeshDict")
        output = template.render(**inputs)
        return dict(openFOAMfile=output)