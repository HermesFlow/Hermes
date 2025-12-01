from hermes.Resources.executers.abstractExecuter import abstractExecuter
import shutil
import os, sys, stat
import numpy

class BuildAllrun(abstractExecuter):

    def _defaultParameters(self):
        return dict(
            output=["status"],
            inputs=["source","target"],
            webGUI=dict(),
            parameters={}
        )

    def run(self, **inputs):
        path = inputs["casePath"]
        self.buildCaseExecutionScript(caseDirectory=path,
                                      execConfiguration=inputs)

        return dict(buildAllRun="buildAllrun")


    def buildCaseExecutionScript(self,caseDirectory,execConfiguration):
        """
            Writes the allRun file that executes the workflow and the allClean file
            that cleans the case to the case directory.

        Parameters
        ----------
        caseDirectory: str
            The directory to write the files to.

        execConfiguration: dict
            A configuration file that is used to build the execution of the node.
            Specifically, includes a node 'caseExecution' with the structure:

             {
                "parallelCase": true|false             # Write the execution for parallel execution.
                "runFile": [
                            --------------- A list of nodes.
                  {
                    "name": "blockMesh",               # The name of the program to execute.
                    "couldRunInParallel": false,       # Write as parallel (only if parallel case is True).
                    "parameters": null                 # Parameters for each run.
                    "foamJob"  : true|false            # Should I use foamJob to run this task
                                                       #     default True
                    "screen"   : true|false            # write log to screen
                                                       #     default True
                    "wait"     : true|false            # wait to the end of execution before next step
                                                       #     default True
                    "slurm"    : true|false            #  Use slurm support to run the code. (override foamJob).
                  }
                ]
                            --------------- A list of nodes.
             }


        getNumberOfSubdomains: int
                The number of subdomains to use in the run file.
                Required if isSlurm is True.


        """

        isSlurm   = execConfiguration['caseExecution'].get('slurm',False)
        isParallel = execConfiguration['parallelCase']
        outputFileName = execConfiguration['caseExecution'].get('fileName',"Allrun")
        execLine = ""

        for execNode in execConfiguration['runFile']:
            #logger.debug(f"Processing Node {execNode['name']}")
            parallelInstruction = (isParallel and execNode['couldRunInParallel'])
            parallelFlag = "-parallel" if parallelInstruction else ""
            progName = execNode['name']
            parameters = execNode.get('parameters',None)
            if parameters is not None:
                params   = " ".join(numpy.atleast_1d(execNode['parameters']))
            else:
                params = ""

            foamJob = execNode.get("foamJob",True)
            wait    = execNode.get("wait",True)
            screenDefault = False if isSlurm else True
            screen  = execNode.get("screen",screenDefault)

            if foamJob:
                execLine += f"foamJob {parallelFlag} -append {'-screen' if screen else ''} {'-wait' if wait else ''} {progName} {params}\n"
            else:
                execLine += f"{progName} {params}\n"

        allrunFile = os.path.join(caseDirectory,outputFileName)
        if not os.path.exists(caseDirectory):
            os.makedirs(caseDirectory,exist_ok=True)

        with open(allrunFile,'w') as execFile:
            execFile.write(execLine)
        os.chmod(allrunFile, 0o777)

        # Now write the allClean file.
        allCleanContent = """
    #!/bin/sh
    cd ${0%/*} || exit 1    # Run from this directory
    
    # Source tutorial clean functions
    . $WM_PROJECT_DIR/bin/tools/CleanFunctions
    
    cp 0.orig/* 0
    cleanCase
        """
        allcleanFile = os.path.join(caseDirectory,"Allclean")
        with open(allcleanFile,'w') as allclean:
            allclean.write(allCleanContent)

        os.chmod(allcleanFile, 0o777)
