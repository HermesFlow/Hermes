Workflow 1: Copy directory and run python code
================================================

The workflow in this section will copy the directory ./source to ./target and then will execute the function
printDirectories in the tutorialPrinter class in file (module) tutorial1.py

.. code-block:: javascript

    {
        "workflow": {
            "nodes": {
                "CopyDirectory": {
                    "Execution": {
                        "input_parameters": {
                            "Source": "source",
                            "Target": "target",
                            "dirs_exist_ok": true
                        }
                    },
                    "type": "general.CopyDirectory"
                },
                "RunPythonCode": {
                    "Execution": {
                        "input_parameters": {
                            "ModulePath": "tutorial1",
                            "ClassName": "tutorialPrinter",
                            "MethodName": "printDirectories",
                            "Parameters": {
                                "source": "{CopyDirectory.output.Source}",
                                "target": "{CopyDirectory.output.Target}"
                            }
                        }
                    },
                    "type": "general.RunPythonCode"
                }
            }
        }
    }

To execute the workflow, hermes translates the workflow JSON file to a python program that uses
the luigi package. To do so, the JSON is first expanded with default values (if exist) and then executes it.

Executing the workflow can be achieved though the code or using the command line interface (CLI).
Here, we will use the CLI to expand, build and execute the workflow. Note that using the combined command
overwrites the expanded file on the original file.

::

    >> hermes-workflow buildExecute workflow.json

After execution, the program writes the output each not to the directory workflow_targetFile.

for example use:

::

    >> cat workflow_targetFiles/CopyDirectory_0.json

to get:

.. code-block:: javascript

    {
        "input_parameters": {
            "Source": "source",
            "Target": "target",
            "dirs_exist_ok": true,
            "WD_path": "examples/Tutorial/Example1"
        },
        "output": {
            "copyDirectory": "copyDirectory",
             "Source": "examples/Tutorial/Workflow1/source",
             "Target": "examples/Tutorial/Workflow1/target"
        }
    }

Note that the output of the CopyDirectory node are Source and Target, that are used as inputs for the
RunPythonCode. Specifically:

.. code-block:: javascript

    "source": "{CopyDirectory.output.Source}",
    "target": "{CopyDirectory.output.Target}"


When the code is re-executed, the luigi package determines whether a taks was completed by examining the files
in the '<workflo>_targetFiles'. If the a file with the name of the node exists there, then luigi assumes that the task
was complete. Hence, rerunning the work required either deleting the  '<workflo>_targetFiles'

::

    >> rm workflow_targetFiles -rf

Or using a --force flag in the CLI:

::

    >> hermes-workflow buildExecute workflow.json --force

