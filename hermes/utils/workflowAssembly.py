from hermes import expandWorkflow,workflow
import json
import os
import pathlib
import shutil


def handler_expand(arguments):
    exapnder = expandWorkflow()

    templateFileName = f"{arguments.workflow.split('.')[0]}.json"
    expandedWorkflow = f"{arguments.caseName.split('.')[0]}.json"
    newTemplate = exapnder.expand(templateJSON=templateFileName)

    with open(expandedWorkflow, 'w') as fp:
        json.dump(newTemplate, fp,indent=4)

def handler_build(arguments):
    exapnder = expandWorkflow()

    templateFile = f"{arguments.workflow.split('.')[0]}.json"
    newWorkflow = f"{arguments.caseName.split('.')[0]}.py"

    expandedWorkflow = f"{newWorkflow.split('.')[0]}.json"

    parametersPath = dict()
    if arguments.parameters is not None:
        with open(arguments.parameters) as paramfile:
            parametersPath = json.load(paramfile)

    newTemplate = exapnder.expand(templateJSON=templateFile, parameters=parametersPath)
    with open(expandedWorkflow, 'w') as fp:
        json.dump(newTemplate, fp,indent=4)

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

    arguments.caseName = arguments.workflow

    if not arguments.force:
        # check if there is old expanded json, or python.
        # also if there are old runfiles it will not rerun.

        expnded = f"{arguments.caseName.split('.')[0]}.json"
        newWorkflow = f"{arguments.caseName.split('.')[0]}.py"

        if os.path.exists(newWorkflow):
            print(f"Python execution file {newWorkflow} exists. Delete or run with --force flag.")
            exit()


    handler_expand(arguments)
    arguments.workflow = arguments.caseName
    arguments.parameters = None
    handler_build(arguments)

    if arguments.force:
        # delete the run files if exist.
        executionfileDir = f"{arguments.caseName.split('.')[0]}_targetFiles"
        shutil.rmtree(executionfileDir, ignore_errors=True)

    handler_execute(arguments)
