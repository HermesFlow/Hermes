from ....general import jinjaTransform

class SnappyHexMesh(jinjaTransform):

    def run(self, **inputs):

        template = self._getTemplate("openFOAM/mesh/SnappyHexMesh/jinjaTemplate")
        output = template.render(**inputs)
        return dict(openFOAMfile=output)