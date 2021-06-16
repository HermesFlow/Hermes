from .abstractExecuter import abstractExecuter
import shutil
import os, sys, stat

class copyDirectoryExecuter(abstractExecuter):

    def _defaultParameters(self):
        return dict(
            output=["status"],
            inputs=["source","target"],
            webGUI=dict(JSONSchema="webGUI/copyDirectory_JSONchema.json",
                        UISchema  = "webGUI/copyDirectory_UISchema.json"),
            parameters={}
        )

    def run(self, **inputs):
        if (len(inputs["Source"]) > 0 and len(inputs["Target"]) > 0):
            shutil.copytree(inputs['Source'],inputs['Target'])
        else:
            print("=============== empty ===============")

        return dict(copyDirectory="copyDirectory")


class copyFileExecuter(abstractExecuter):

    def _defaultParameters(self):
        return dict(
            output=["status"],
            inputs=["source", "target"],
            webGUI=dict(JSONSchema="webGUI/copyFile_JSONchema.json",
                        UISchema="webGUI/copyFile_UISchema.json"),
            parameters={}
        )

    def run(self, **inputs):
            if (len(inputs["Source"]) > 0 and len(inputs["Target"]) > 0):
                shutil.copy(inputs['Source'], inputs['Target'])
            else:
                print("=============== empty ===============")

            return dict(copyField="copyFile")

class RunOsCommandExecuter(abstractExecuter):

    def _defaultParameters(self):
        return dict(
            output=["status"],
            inputs=["source", "target"],
            webGUI=dict(JSONSchema="webGUI/RunOsCommand_JSONchema.json",
                        UISchema="webGUI/RunOsCommand_UISchema.json"),
            parameters={}
        )

    def run(self, **inputs):
        import os, sys, stat

        print("===========================")
        print(" ---got to RunOsCommand---")
        print("===========================")

        if inputs["Method"]=="batchFile":
            #get the path of the batchfile
            fullPath = inputs["batchFile"]
            #update 'pathFile' to full path- absolute
            fullPath=os.path.abspath(fullPath)
            # give the file execute premission of the user
            os.chmod(fullPath, stat.S_IRWXU)
            # run the batch file
            os.system(fullPath)
        else:
            # commands where choosen
            # create a batchfile from the commands using jinja, save it and run

            #create the file
            # define the interpreter-
            ret = "#!/bin/bash" + "\n"+"\n"

            #loop all items in the list and add it to the string
            for item in inputs["Commands"]:
                ret+= item +"\n"
            
            #save the file in the working directory
            path = inputs["WD_path"]+"/Commands.sh"
            with open(path, "w") as fh:
                fh.write(ret) 

            # give the file execute premission of the user
            os.chmod(path, stat.S_IRWXU)
            # run the batch file
            os.system(path)
            

        return dict(RunOsCommand="RunOsCommand")



class executeScriptExecuter(abstractExecuter):

    def _defaultParameters(self):
        return dict(
            output=["status"],
            inputs=["runcmd", "cmd"],
            webGUI=dict(JSONSchema="webGUI/copyOSExecuter_JSONchema.json",
                        UISchema="webGUI/copyOSExecuter_UISchema.json"),
            parameters={}
        )

def run(self, **inputs):
    return dict(executeScript="executeScript")
