import os
import stat

from ...executers.abstractExecuter import abstractExecuter


class RunOsCommand(abstractExecuter):

    def _defaultParameters(self):
        return dict(
            output=["commands"],
            inputs=["Method"],
            webGUI=dict(JSONSchema="webGUI/RunOsCommand_JSONchema.json",
                        UISchema="webGUI/RunOsCommand_UISchema.json"),
            parameters={}
        )
    

    @staticmethod
    def testParamValues(params: dict[str, any]):
        passed, status_message = abstractExecuter.checkParamAgainstList(params, "Method", ["batchFile", "Command list"], True)
        if not passed:
            return passed, status_message
        
        if abstractExecuter.isParamTestable(params, "Method"):
            if params["Method"] == "batchFile":
                passed, status_message = abstractExecuter.checkParamType(params, "batchFile", str, True)
                if not passed:
                    return passed, status_message
            elif params["Method"] == "Command list":
                passed, status_message = abstractExecuter.checkParamType(params, "Command", (dict, list), True)
                if not passed:
                    return passed, status_message
        

        passed, status_message = abstractExecuter.checkParamType(params, "changeDirTo", str, False)
        if not passed:
            return passed, status_message
        
        return True, ""

    def run(self, **inputs):
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
            import numpy
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

        return dict(commands=ret)

