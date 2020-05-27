#from abstractExecuter import abstractExecuter
import os
from hermes.Resources.executers.abstractExecuter import abstractExecuter

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


        return dict(RunPythonScript="ModulePath")

class exportFiles(abstractExecuter):

    def __init__(self):
        pass

    def _defaultParameters(self):
        return dict(
            output=["status"],
            inputs=["classpath", "function"],
            webGUI=dict(JSONSchema="webGUI/exportFiles_JSONchema.json",
                        UISchema="webGUI/exportFiles_UISchema.json"),
            parameters={}
        )

    def run(self, **inputs):
        # # get the working directory
        # path = os.getcwd()
        #
        # # export all data in the dict
        # for Ikey,Ival in inputs.items():
        #
        #     # get the path to dir and file seperatly
        #     key_list = Ikey.split('/')
        #     dir_path= path + "/" + key_list[0]
        #     file_path = path + "/" + Ikey
        #
        #     # if dir doesnt exsit, create one
        #     if not(os.path.isdir(dir_path)):
        #         os.mkdir(dir_path)
        #
        #     # export the file
        #     with open( file_path , "w+" ) as f:
        #         f.write(Ival)
        path = inputs["casePath"]
        files = inputs["files"]

        for filename, file in files.items():
            newPath = os.path.join(path, filename)
            with open(newPath, "w") as newfile:
                newfile.write(file)









