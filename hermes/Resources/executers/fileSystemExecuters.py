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
            shutil.copytree(inputs['Source'],inputs['Target'],dirs_exist_ok=inputs.get("dirs_exist_ok",True))
        else:
            print("=============== empty ===============")

        absSource = os.path.abspath(inputs["Source"])
        absTarget = os.path.abspath(inputs["Target"])

        return dict(copyDirectory="copyDirectory",
                    Source =absSource,Target=absTarget)


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
                shutil.copy(inputs['Source'], inputs['Target']) # this will change to a flag like the other version.
            else:
                print("=============== empty ===============")

            absSource = os.path.abspath(inputs["Source"])
            absTarget = os.path.abspath(inputs["Target"])

            return dict(copyField="copyFile",Source =absSource,Target=absTarget)

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
        import stat,os

        if "changeDirTo" in inputs:
            cwd = os.getcwd()
            os.chdir(os.path.abspath(inputs["changeDirTo"]))

        if inputs["Method"]=="batchFile":
            #get the path of the batchfile
            fullPath = inputs["batchFile"]
            #update 'pathFile' to full path- absolute
            fullPath=os.path.abspath(fullPath)
            # give the file execute premission of the user
            os.chmod(fullPath, stat.S_IRWXU)
            # run the batch file
            os.system(fullPath)
        elif inputs["Method"]=="Command list":
            import subprocess, stat, numpy
            ret = []
            for cmd in numpy.atleast_1d(inputs["Command"]):
                ret_val = os.system(cmd)
                ret.append("Success" if ret == 1 else "Failed")

                #### This solution to save the std out doesn't work when there are multiple parameters.
                # output = subprocess.Popen(cmd.split(" "),stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
                # stdout,stderr = output.communicate()
                #
                # stdout = "" if stdout is None else stdout.decode()
                # stderr = "" if stderr is None else stderr.decode()
                #
                # result = dict(command=cmd,
                #               stdout=stdout,
                #               stderr=stderr)
                # ret.append(result)
        else:
            raise ValueError(f"Method must be 'batchFile', or 'Command list'. got {input['Method']}")


        if "changeDirTo" in inputs:
            os.chdir(cwd)

        return dict(RunOsCommand="RunOsCommand",
                    commands=ret)



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
