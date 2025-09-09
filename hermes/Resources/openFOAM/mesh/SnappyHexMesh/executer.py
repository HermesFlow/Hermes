from ....general import JinjaTransform
import logging
import json

class SnappyHexMesh(JinjaTransform):

    def run(self, **inputs):
        logger = logging.getLogger('luigi-interface')
        logger.info("------ Start -----")
        logger.debug(json.dumps(inputs,indent=4))
        version = inputs.get("version", 1)
        if version == 2:
            try:
                ip = inputs["Execution"]["input_parameters"]
            except KeyError:
                raise ValueError("Missing Execution.input_parameters in version 2 input")

            render_inputs = {
                "input_parameters": ip
            }
            template = self._getTemplate("openFOAM/mesh/SnappyHexMesh/jinjaTemplate.v2")
        else:
            render_inputs = inputs
            template = self._getTemplate("openFOAM/mesh/SnappyHexMesh/jinjaTemplate")

        output = template.render(**render_inputs)
        return dict(openFOAMfile=output)