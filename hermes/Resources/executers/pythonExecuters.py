#from abstractExecuter import abstractExecuter
import os
from hermes.Resources.executers.abstractExecuter import abstractExecuter
import errno
import json
import pydoc



class pythonExecuter(abstractExecuter):
    """
        Executes the function in the class.

        inputs:
            classpath : str, The class path string to the class
            funcName  : str, The name of the function to run .
            parameters : dict, The parameters for the function.
    """

    def _defaultParameters(self):
        return dict(
            output=["status"],
            inputs=["classpath", "function"],
            webGUI=dict(JSONSchema="webGUI/pythonExecuter_JSONchema.json",
                        UISchema="webGUI/pythonExecuter_UISchema.json"),
            parameters={}
        )

    def run(self, **inputs):

        # newobj = pydoc.locate(inputs['classpath'])()
        # func   = getattr(newobj,input["funcName"])
        # ret = func(**inputs['parameters'])
        self.logger.info("Starting run of run python script")

        try:
            modulecls = pydoc.locate(inputs['ModulePath'])

            if modulecls is None:
                print(f"Error loading module {inputs['ModulePath']}")
                raise RuntimeError(f"Error loading module {inputs['ModulePath']}")

        except pydoc.ErrorDuringImport as e:
            self.logger.critical(f"Error loading module {inputs['ModulePath']}")
            raise(e)

        objcls = getattr(modulecls, inputs["ClassName"])
        newobj = objcls()
        func   = getattr(newobj,inputs["MethodName"])
        ret = func(**inputs)
        return dict(pythonExecuter="pythonExecuter",Return=ret)








