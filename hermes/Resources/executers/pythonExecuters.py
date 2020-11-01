#from abstractExecuter import abstractExecuter
import os
from hermes.Resources.executers.abstractExecuter import abstractExecuter
import errno
import json

class pythonExecuter(abstractExecuter):

    def _defaultParameters(self):
        return dict(
            output=["status"],
            inputs=["classpath", "function"],
            webGUI=dict(JSONSchema="webGUI/pythonExecuter_JSONchema.json",
                        UISchema="webGUI/pythonExecuter_UISchema.json"),
            parameters={}
        )

    def run(self, **inputs):



        return dict(pythonExecuter="pythonExecuter")








