import os

from ...executers.abstractExecuter import abstractExecuter
import pydoc
import sys

class RunPythonCode(abstractExecuter):
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

            inputs=["CodeDirectory","ModulePath", "function"],
            webGUI=dict(JSONSchema="webGUI/pythonExecuter_JSONchema.json",
                        UISchema="webGUI/pythonExecuter_UISchema.json"),
            parameters={}
        )

    def run(self, **inputs):

        # newobj = pydoc.locate(inputs['classpath'])()
        # func   = getattr(newobj,input["funcName"])
        # ret = func(**inputs['parameters'])
        self.logger.info("Starting run of run python script")

        codeDir =  inputs.get("CodeDirectory",None )

        sys.path.append(os.getcwd())
        if codeDir is not None:
            sys.path.append(codeDir)

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
        #full_json = inputs["Parameters"].get("fullJSON", {})  # default to empty
        #newobj = objcls(full_json)

        func   = getattr(newobj,inputs["MethodName"])
        ret = func(**inputs['Parameters'])
        return dict(pythonExecuter="pythonExecuter",Return=ret)