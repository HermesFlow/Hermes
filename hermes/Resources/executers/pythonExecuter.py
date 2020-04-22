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
        print("===============================")
        print("-----got to RunPythonScript----")
        print("===============================")

        ModulePath=inputs["ModulePath"]
        MethodName=inputs["MethodName"]
        Parameters=inputs["Parameters"]



        
        # #====== take care of the path ==============
        # #update 'current_dir' to full path- absolute
        # ModulePath=os.path.abspath(ModulePath)
        #
        # #insert the path to sys
        # # insert at 1, 0 is the script path (or '' in REPL)
        # sys.path.insert(1, ModulePath)
        #
        # #====== take care of the MethodName ==============
        # # import the module by his name
        #
        # # split ModulePath
        # splitModulePath = ModulePath.split('.')
        #
        # # check its length to find out a module or an inside class
        # if len(splitModulePath)==1:
        #     # imort module directly
        #     import MethodName
        # else:
        #     # the method name is the last item in the split list
        #     MethodName=splitModulePath[-1]
        #
        #     #remove MethodName from the list
        #     splitModulePath.remove(MethodName)
        #
        #     # create the path from the rest
        #     fromPath="."
        #     fromPath=fromPath.join(splitModulePath)
        #
        #     #import module
        #     from fromPath import MethodName
        #
        #
        # import MethodName
        #
        # #====== take care of the parameters ==============
        # # create a new dict contain all parameters
        # NewParameters=[]
        #
        # # loop all parameters and cast them
        # for param in Parameters:
        #
        #     # split between the type and the value
        #     splitParam = param.split('.')
        #
        #     # cast each param
        #     if splitParam[0] == "int":
        #        splitParam[1] = int(splitParam[1])
        #     elif splitParam[0] == "float":
        #        splitParam[1] = float(splitParam[1])
        #     elif splitParam[0] == "str":
        #        splitParam[1] = str(splitParam[1])
        #     elif splitParam[0] == "dict":
        #        splitParam[1] = dict(splitParam[1])
        #     elif splitParam[0] == "list":
        #        splitParam[1] = list(splitParam[1])
        #     elif splitParam[0] == "None":
        #        splitParam[1] = None
        #     elif splitParam[0] == "bool":
        #        splitParam[1] = bool(splitParam[1])
        #
        # NewParameters.append(splitParam[1])
        #
        # print(str(NewParameters))
        #
        # MethodName(NewParameters)





        return dict(RunPythonScript="ModulePath")


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
            from hermes.Resources.executers.CreateDictFiles.snappyHexMeshDictDir.snappyDictJsonToOF import snappyOFfunc

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
            from hermes.Resources.executers.CreateDictFiles.controlDictDir.controlDictJsonToOF import controlDictOFfunc

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
            from hermes.Resources.executers.CreateDictFiles.fvSchemesDir.fvSchemesJsonToOF import fvSchemeOFfunc

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
            from hermes.Resources.executers.CreateDictFiles.fvSolutionDir.fvSolJsonToOF import fvSolOFfunc

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
            from hermes.Resources.executers.CreateDictFiles.transPropDir.transPropJsonToOF import transPropOFfunc

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
            from hermes.Resources.executers.CreateDictFiles.turbulencePropDir.turbulencePropJsonToOF import turbulencePropOFfunc

            #call the function and create the node dictionary
            turbulencePropOFfunc(formData,WD)

        return dict(RASProperties="RASProperties")










