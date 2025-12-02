from ....general import JinjaTransform

class BlockMesh(JinjaTransform):
    """
    Transforms JSON -> blockMeshDict using Jinja templates.

    JSON structure:
    {
        "geometry": { ... },
        "boundary": [ ... ],
        "vertices": [ ... ]
    }

    Notes:
    - Automatically switches between versioned general template and classic based on workflow version.
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
        version = self._workflow.get("workflow", {})

        if version == 2:
            return super().run()
        else:
            template_name = "openFOAM/mesh/BlockMesh/jinjaTemplate"
            return super().run(template=template_name, parameters=inputs)
