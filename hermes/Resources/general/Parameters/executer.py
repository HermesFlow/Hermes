from ...executers.abstractExecuter import abstractExecuter

class Parameters(abstractExecuter):

    def _defaultParameters(self):
        return dict(
            output=[],
            inputs=[],
            webGUI=dict(JSONSchema=None,
                        UISchema  =None),
            parameters={}
        )

    def run(self, **inputs):
        ret = dict(transformTemplate="parameterExecuter")
        ret.update(inputs)
        return ret
