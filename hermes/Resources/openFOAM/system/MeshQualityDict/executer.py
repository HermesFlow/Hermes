import logging
import json
from ....general import JinjaTransform


class MeshQualityDict(JinjaTransform):
    """
    OpenFOAM meshQualityDict executer for Hermes v2 workflow.
    Converts the Hermes JSON node into a valid OpenFOAM meshQualityDict file.
    """

    def run(self, **inputs):
        logger = logging.getLogger('luigi-interface')
        logger.info("------ Start meshQualityDict -----")
        logger.debug(json.dumps(inputs, indent=4))

        version = inputs.get("version", 1)

        if version == 2:
            try:
                ip = inputs["Execution"]["input_parameters"]
            except KeyError:
                raise ValueError("Missing Execution.input_parameters in version 2 input")

            render_inputs = {"input_parameters": ip}
            template = self._getTemplate("openFOAM/system/MeshQualityDict/jinjaTemplate.v2")
        else:
            render_inputs = inputs
            template = self._getTemplate("openFOAM/system/MeshQualityDict/jinjaTemplate")

        output = template.render(**render_inputs)
        return dict(openFOAMfile=output)
