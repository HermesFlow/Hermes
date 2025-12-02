from ....general import JinjaTransform
import logging
import json

class SnappyHexMesh(JinjaTransform):
    def run(self, **inputs):

        version = self._workflow.get("workflow", {})

        if version == 2:
            return super().run()
        else:
            template_name = "openFOAM/mesh/SnappyHexMesh/jinjaTemplate"
            return super().run(template=template_name, parameters=inputs)
