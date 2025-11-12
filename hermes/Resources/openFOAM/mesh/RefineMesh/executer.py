from ....general import JinjaTransform

class RefineMesh(JinjaTransform):

    def _defaultParameters(self):
        return dict(
            output=["status"],
            inputs=["classpath", "function"],
            webGUI=dict(JSONSchema="webGUI/BlockMeshExecuter_JSONchema.json",
                        UISchema="webGUI/BlockMeshExecuter_UISchema.json"),
            parameters={}
        )

    def run(self, **inputs):

        # get the  name of the template
        templateName = "openFOAM/mesh/RefineMesh/jinjaTemplate"

        template = self._getTemplate(templateName)
        # render jinja for the choosen template
        output = template.render(**inputs)

        return dict(openFOAMfile=output)