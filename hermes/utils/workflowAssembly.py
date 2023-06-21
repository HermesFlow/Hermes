from hermes import expandWorkflow,workflow
import json
import os
import pathlib
import shutil
import logging
from ..utils.jsonutils import loadJSON

def handler_expand(arguments):
    logger = logging.getLogger("hermes.bin.expand")
    logger.info("---------- Start ---------")

    exapnder = expandWorkflow()

    templateFileName = f"{arguments.workflow.split('.')[0]}.json"
    expandedWorkflow = f"{arguments.caseName.split('.')[0]}.json"

    logger.execution(f"Expanding {templateFileName} to {expandedWorkflow}")
    newTemplate = exapnder.expandBatch(templateJSON=templateFileName)

    logger.execution(f"Writing the expanded workflow to {expandedWorkflow}")
    with open(expandedWorkflow, 'w') as fp:
        json.dump(newTemplate, fp,indent=4)

    logger.info("---------- End ---------")

def handler_build(arguments):
    logger = logging.getLogger("hermes.bin.build")
    logger.info("---------- Start ---------")
    handler_expand(arguments)

    templateFileName = f"{arguments.workflow.split('.')[0]}.json"
    newTemplate = loadJSON(templateFileName)
    newWorkflow = f"{arguments.caseName.split('.')[0]}.py"

    WDPath = os.getcwd()
    builder = "luigi"
    flow = workflow(newTemplate, WDPath)
    build = flow.build(builder)
    with open(newWorkflow, "w") as file:
        file.write(build)

def handler_execute(arguments):
    """
        Should be updated to select execution engine.
    :param arguments:
    :return:
    """

    pythonPath = arguments.caseName.split(".")[0]


    #cwd = pathlib.Path().absolute()
    #moduleParent = pathlib.Path(pythonPath).parent.absolute()
    #os.chdir(moduleParent)
    executionStr = f"python3 -m luigi --module {os.path.basename(pythonPath)} finalnode_xx_0 --local-scheduler"
    print(executionStr)

    if arguments.force:
        # delete the run files if exist.
        executionfileDir = f"{arguments.caseName.split('.')[0]}_targetFiles"
        shutil.rmtree(executionfileDir, ignore_errors=True)

    os.system(executionStr)


    #os.chdir(cwd)


def handler_buildExecute(arguments):
    logger = logging.getLogger("hermes.bin")
    logger.info("---------- Start ---------")
    arguments.caseName = arguments.workflow

    if not arguments.force:
        # check if there is old expanded json, or python.
        # also if there are old runfiles it will not rerun.

        expnded = f"{arguments.caseName.split('.')[0]}.json"
        newWorkflow = f"{arguments.caseName.split('.')[0]}.py"

        if os.path.exists(newWorkflow):
            print(f"Python execution file {newWorkflow} exists. Delete or run with --force flag.")
            exit()

    logger.execution(f"Expanding the workflow with arguments {arguments}")
    handler_expand(arguments)
    arguments.workflow = arguments.caseName
    arguments.parameters = None
    logger.execution(f"building the workflow with arguments {arguments}")
    handler_build(arguments)

    if arguments.force:

        # delete the run files if exist.
        executionfileDir = f"{arguments.caseName.split('.')[0]}_targetFiles"
        logger.execution(f"Got remove, tree, deleting {executionfileDir}")
        shutil.rmtree(executionfileDir, ignore_errors=True)

    logger.execution("Executing the workflow")
    handler_execute(arguments)
    logger.info("----------- End ----------")