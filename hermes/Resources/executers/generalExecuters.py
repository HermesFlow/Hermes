from .abstractExecuter import abstractExecuter

class parameterExecuter(abstractExecuter):

    def _defaultParameters(self):
        return dict(
            output=[],
            inputs=[],
            webGUI=dict(JSONSchema=None,
                        UISchema  =None),
            parameters={}
        )

    def run(self, **inputs):
        return dict(parameterExecuter="parameterExecuter")


class transformTemplateExecuter(abstractExecuter):

    def _defaultParameters(self):
        return dict(
            output=["transformed"],
            inputs=["template","templatedir"],
            webGUI=dict(JSONSchema=None,
                        UISchema  =None),
            parameters={}
        )

    def run(self, **inputs):
        return dict(transformTemplate="transformTemplate")
