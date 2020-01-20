from .abstractExecuter import abstractExecuter


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

class RunPythonScript(abstractExecuter):

    def _defaultParameters(self):
        return dict(
            output=["status"],
            inputs=["classpath", "function"],
            webGUI=dict(JSONSchema="webGUI/RunPythonScript_JSONchema.json",
                        UISchema="webGUI/RunPythonScript_UISchema.json"),
            parameters={}
        )

    def run(self, **inputs):
        return dict(RunPythonScript="RunPythonScript")


class nogaExec(abstractExecuter):

    def _defaultParameters(self):
        return dict(
            output=["status"],
            inputs=["classpath", "function"],
            webGUI=dict(JSONSchema="webGUI/nogaExec_JSONchema.json",
                        UISchema="webGUI/nogaExec_UISchema.json"),
            parameters={}
        )

    def run(self, **inputs):
        print("========================")
        print("-----got to nogaExac----")
        print("========================")
    
        print("=======Print inputs args===========")
        for x in inputs:
            print(x,str(inputs[x]))

        print("=======try print specific===========")
        if "formData" in inputs:
            A=inputs["formData"]
            print(A)
        print("====================================")

        return dict(nogaExec="nogaExec")

class snappyHexMesh(abstractExecuter):

    def _defaultParameters(self):
        return dict(
            output=["status"],
            inputs=["classpath", "function"],
            webGUI=dict(JSONSchema="webGUI/snappyHexMesh_JSONchema.json",
                        UISchema="webGUI/snappyHexMesh_UISchema.json"),
            parameters={}
        )

    def run(self, **inputs):

        print("=============================")
        print("-----got to snappyHexMesh----")      
        print("=============================")
        
        #working directory - where to save the OF dictionaries
        WD=inputs["WD_path"]

        # check that form data do exsit in inputs
        if "formData" in inputs:

            #get the formData structure from inputs
            formData=inputs["formData"]
            
            #import the python script which create the dictionary
            from pyHermes.executers.CreateDictFiles.snappyHexMeshDictDir.snappyDictJsonToOF import snappyOFfunc

            #call the function and create the node dictionary
            snappyOFfunc(formData,WD)

        return dict(snappyHexMesh="snappyHexMesh")

class controlDict(abstractExecuter):

    def _defaultParameters(self):
        return dict(
            output=["status"],
            inputs=["classpath", "function"],
            webGUI=dict(JSONSchema="webGUI/controlDict_JSONchema.json",
                        UISchema="webGUI/controlDict_UISchema.json"),
            parameters={}
        )

    def run(self, **inputs):
        print("===========================")
        print("-----got to controlDict----")
        print("===========================")

        #working directory - where to save the OF dictionaries
        WD=inputs["WD_path"]

        # check that form data do exsit in inputs
        if "formData" in inputs:

            #get the formData structure from inputs
            formData=inputs["formData"]

            #import the python script which create the dictionary
            from pyHermes.executers.CreateDictFiles.controlDictDir.controlDictJsonToOF import controlDictOFfunc

            #call the function and create the node dictionary
            controlDictOFfunc(formData,WD)

        return dict(controlDict="controlDict")

class fvSchemes(abstractExecuter):

    def _defaultParameters(self):
        return dict(
            output=["status"],
            inputs=["classpath", "function"],
            webGUI=dict(JSONSchema="webGUI/fvSchemes_JSONchema.json",
                        UISchema="webGUI/fvSchemes_UISchema.json"),
            parameters={}
        )

    def run(self, **inputs):

        print("=========================")
        print("-----got to fvSchemes----")
        print("=========================")

        #working directory - where to save the OF dictionaries
        WD=inputs["WD_path"]

        # check that form data do exsit in inputs
        if "formData" in inputs:

            #get the formData structure from inputs
            formData=inputs["formData"]

            #import the python script which create the dictionary
            from pyHermes.executers.CreateDictFiles.fvSchemesDir.fvSchemesJsonToOF import fvSchemeOFfunc

            #call the function and create the node dictionary
            fvSchemeOFfunc(formData,WD)

        return dict(fvSchemes="fvSchemes")

class fvSolution(abstractExecuter):

    def _defaultParameters(self):
        return dict(
            output=["status"],
            inputs=["classpath", "function"],
            webGUI=dict(JSONSchema="webGUI/fvSolution_JSONchema.json",
                        UISchema="webGUI/fvSolution_UISchema.json"),
            parameters={}
        )

    def run(self, **inputs):

        print("==========================")
        print("-----got to fvSolution----")
        print("==========================")

        #working directory - where to save the OF dictionaries
        WD=inputs["WD_path"]

        # check that form data do exsit in inputs
        if "formData" in inputs:

            #get the formData structure from inputs
            formData=inputs["formData"]

            #import the python script which create the dictionary
            from pyHermes.executers.CreateDictFiles.fvSolutionDir.fvSolJsonToOF import fvSolOFfunc

            #call the function and create the node dictionary
            fvSolOFfunc(formData,WD)

        return dict(fvSolution="fvSolution")

class transportProperties(abstractExecuter):

    def _defaultParameters(self):
        return dict(
            output=["status"],
            inputs=["classpath", "function"],
            webGUI=dict(JSONSchema="webGUI/transportProperties_JSONchema.json",
                        UISchema="webGUI/transportProperties_UISchema.json"),
            parameters={}
        )

    def run(self, **inputs):

        print("===================================")
        print("-----got to transportProperties----")
        print("===================================")

        #working directory - where to save the OF dictionaries
        WD=inputs["WD_path"]

        # check that form data do exsit in inputs
        if "formData" in inputs:

            #get the formData structure from inputs
            formData=inputs["formData"]

            #import the python script which create the dictionary
            from pyHermes.executers.CreateDictFiles.transPropDir.transPropJsonToOF import transPropOFfunc

            #call the function and create the node dictionary
            transPropOFfunc(formData,WD)

        return dict(transportProperties="transportProperties")

class RASProperties(abstractExecuter):

    def _defaultParameters(self):
        return dict(
            output=["status"],
            inputs=["classpath", "function"],
            webGUI=dict(JSONSchema="webGUI/RASProperties_JSONchema.json",
                        UISchema="webGUI/RASProperties_UISchema.json"),
            parameters={}
        )

    def run(self, **inputs):

        print("=============================")
        print("-----got to RASProperties----")
        print("=============================")

        #working directory - where to save the OF dictionaries
        WD=inputs["WD_path"]

        # check that form data do exsit in inputs
        if "formData" in inputs:

            #get the formData structure from inputs
            formData=inputs["formData"]

            #import the python script which create the dictionary
            from pyHermes.executers.CreateDictFiles.turbulencePropDir.turbulencePropJsonToOF import turbulencePropOFfunc

            #call the function and create the node dictionary
            turbulencePropOFfunc(formData,WD)

        return dict(RASProperties="RASProperties")










