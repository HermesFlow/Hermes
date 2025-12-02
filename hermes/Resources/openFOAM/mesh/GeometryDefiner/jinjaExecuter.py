from ....executers.abstractExecuter import abstractExecuter

class GeometryDefinerExecuter(abstractExecuter):

    def _defaultParameters(self):
        return dict(
            output=[],
            inputs=[],
            webGUI=dict(JSONSchema=None,
                        UISchema=None),
            parameters={}
        )

    def run(self, **inputs):
        version = self._workflow.get("workflow", {})

        if version == 2:
            return super().run()
        else:
            template_name = "openFOAM/mesh/GeometryDefiner/jinjaTemplate"
            return super().run(template=template_name, parameters=inputs)


