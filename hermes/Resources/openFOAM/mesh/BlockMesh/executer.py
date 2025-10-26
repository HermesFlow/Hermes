from ....general import JinjaTransform
import logging
import json

class BlockMesh(JinjaTransform):
    """
    Transforms JSON -> blockMeshDict using the Jinja template.

    Supports both v1 and v2 input formats:
    - v1: raw structured inputs
    - v2: Hermes-style input_parameters with versioning

    JSON format (v1):
    {
        "geometry": {
            "convertToMeters": 1,
            "cellCount": (50, 50, 30),
            "grading": [1, 1, 1]
        },
        "boundary": [...],
        "vertices": [...]
    }

    JSON format (v2):
    {
        "Execution": {
            "input_parameters": {
                "geometry": {...},
                "boundary": [...],
                "vertices": [...]
            }
        },
        "type": "openFOAM.mesh.BlockMesh",
        "version": 2
    }
    """

    def _defaultParameters(self):
        return dict(
            output=["status"],
            inputs=["classpath", "function"],
            webGUI=dict(
                JSONSchema="webGUI/BlockMeshExecuter_JSONchema.json",
                UISchema="webGUI/BlockMeshExecuter_UISchema.json"
            ),
            parameters={}
        )

    def run(self, **inputs):
        logger = logging.getLogger("luigi-interface")
        logger.info("Running BlockMesh executer")
        logger.debug("Received inputs:\n" + json.dumps(inputs, indent=4))

        version = inputs.get("version", 1)

        if version == 2:
            try:
                ip = inputs["Execution"]["input_parameters"]
            except KeyError:
                raise ValueError("Missing Execution.input_parameters in version 2 input")

            render_inputs = {
                "input_parameters": ip
            }
            template_name = "openFOAM/mesh/BlockMesh/jinjaTemplate.v2"
        else:
            render_inputs = inputs
            template_name = "openFOAM/mesh/BlockMesh/jinjaTemplate"

        template = self._getTemplate(template_name)
        output = template.render(**render_inputs)

        return dict(openFOAMfile=output)
