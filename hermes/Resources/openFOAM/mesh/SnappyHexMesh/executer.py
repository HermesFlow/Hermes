from ....general import JinjaTransform
import logging
import json

class SnappyHexMesh(JinjaTransform):

    def run(self, **inputs):
        logger = logging.getLogger('luigi-interface')
        logger.info("------ Start -----")
        logger.debug(json.dumps(inputs,indent=4))
        template = self._getTemplate("openFOAM/mesh/SnappyHexMesh/jinjaTemplate")
        output = template.render(**inputs)
        return dict(openFOAMfile=output)