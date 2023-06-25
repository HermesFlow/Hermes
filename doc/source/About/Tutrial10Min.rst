
10-minute tutorial
################################

In this tutorial we will show examples for workflows at an increasing level of complexity.

Example 1: Copy and run workflow
================================

The following workflow copies a directory and then
executes a python program.

.. code-block:: javascript

    {
        "workflow": {
            "root": null,
            "nodeList": [
                "CopyDirectory",
                "RunPythonCode",
            ],
            "nodes": {
                "CopyDirectory": {
                    "Execution": {
                        "type": "fileSystemExecuters.copyDirectory",
                        "input_parameters": {
                            "Source": "./source",
                            "Target": "./target",
                            "dirs_exist_ok": true
                        }
                    }
                },
                "RunPythonCode": {
                    "Execution": {
                        "type": "pythonExecuters.python",
                        "input_parameters": {
                            "ModulePath": "tutorial1",
                            "ClassName": "tutrialPrinter",
                            "MethodName": "printDirectories",
                            "Parameters": {
                                "target" : {CopyDirectory.Output.target}
                            }
                        }
                    }
                }
    }

The workflow will copy the directory ./source to ./target and then will execute the code