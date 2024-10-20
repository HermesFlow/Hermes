from ...executers.abstractExecuter import abstractExecuter
import shutil
import os, sys, stat
import subprocess

class RunOsCommand(abstractExecuter):

    def _defaultParameters(self):
        return dict(
            output=["status"],
            inputs=["Method", "Command"],
            webGUI=dict(JSONSchema="webGUI/RunOsCommand_JSONchema.json",
                        UISchema="webGUI/RunOsCommand_UISchema.json"),
            parameters={}
        )

    def run(self, **inputs):
        import stat,os
        cwd = os.getcwd()
        if "changeDirTo" in inputs:
            os.chdir(os.path.abspath(inputs["changeDirTo"]))

        ErrorMsg=None
        if inputs["Method"]=="batchFile":
            #get the path of the batchfile
            fullPath = inputs["batchFile"]
            #update 'pathFile' to full path- absolute
            fullPath=os.path.abspath(fullPath)
            # give the file execute premission of the user
            os.chmod(fullPath, stat.S_IRWXU)
            # run the batch file
            ret_val = os.system(fullPath)
            if ret_val != 0:
                ErrorMsg = f"{fullPath} failed"

        elif inputs["Method"]=="Command list":
            import subprocess, stat, numpy
            ret = []
            for cmd in numpy.atleast_1d(inputs["Command"]):
                ret_val = os.system(cmd)
                if ret_val != 0:
                    ErrorMsg = f"{cmd} failed"
                else:
                    ret.append("Success")

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
            ErrorMsg = f"Method must be 'batchFile', or 'Command list'. got {input['Method']}"

        os.chdir(cwd)
        if ErrorMsg is not None:
            raise ValueError(ErrorMsg)

        return dict(RunOsCommand="RunOsCommand",commands=ret)

