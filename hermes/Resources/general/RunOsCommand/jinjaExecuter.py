from ...executers.abstractExecuter import abstractExecuter
import shutil
import os, sys, stat

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

        cwd = os.getcwd()

        if "changeDirTo" in inputs:
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
                if ret_val != 0:
                    ret = "Failed Run"
                    break

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
            raise ValueError(f"Method must be 'batchFile', or 'Command list'. got {input['Method']}")

        os.chdir(cwd)

        return dict(RunOsCommand="RunOsCommand",commands=ret)

