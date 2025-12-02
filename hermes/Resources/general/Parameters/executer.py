from ...executers.abstractExecuter import abstractExecuter

class Parameters(abstractExecuter):
    def __init__(self, JSON, full_workflow=None):
        super().__init__(JSON)

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
