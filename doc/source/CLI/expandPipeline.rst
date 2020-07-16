Expand Pipeline
===============

This page demonstrates how to expand a pipeline, meaning replacing
names of templates with the templates themselves.

For example, let's use the file simpleFOAM.json from the examples:

.. code-block:: python

    {
        "workflow": {
            "root": null,
            "Templates": [],
            "nodeList": [
                "CopyDirectory",
                "RunPythonScript"
            ],
            "nodes": {
                "CopyDirectory": {
                    "Template": "general.CopyDirectory",
                    "input_parameters": {
                        "Target": "I'm from the pipeline",
                        "Properties.Source.prop": "I'm from the pipeline too!"
                    }
                },
                "RunPythonScript": {
                    "Template": "general.RunPythonScript"
                    }
                }
            }
        }

We would like to expand it.
This pipeline uses the default parameters for all nodes except for the parameter "Target"
of "CopyDirectory", which is "I'm from the pipeline".
In addition, it sets the value of Properties.Source.prop to "I'm from the pipeline too!".
We can expand it using the hermes-Pipeline command line.

.. code-block:: python

    hermes-Pipeline expand "/home/ofir/Downloads/Hermes/Hermes_git/examples/simpleFOAM/simpleFOAM.json"
                           "/home/ofir/Downloads/Hermes/Hermes_git/examples/simpleFOAM/simpleFOAMexpanded.json"

The first argument is the path of the file.
The second one is the path of the new, expanded file.

We can also use parameters given in another json file,
for example this file named parameters:

.. code-block:: python

    {
      "Source" :  "I'm from the parameters json"
    }

In order to use it, we add its path to the command:

.. code-block:: python

    hermes-Pipelineexpand "/home/ofir/Downloads/Hermes/Hermes_git/examples/simpleFOAM/simpleFOAM.json"
                          "/home/ofir/Downloads/Hermes/Hermes_git/examples/simpleFOAM/simpleFOAMexpanded.json"
                          "/home/ofir/Downloads/Hermes/Hermes_git/examples/simpleFOAM/parameters.json"

The expanded template is shown below.
Note that the parameter "Target"
of "CopyDirectory" is "I'm from the pipeline",
and the parameter "Source" is "I'm from the parameters json".

.. code-block:: python

    {
      "workflow": {
        "root": null,
        "Templates": [],
        "nodeList": [
          "CopyDirectory",
          "RunPythonScript"
        ],
        "nodes": {
          "CopyDirectory": {
            "Template": {
              "typeExecution": "copyDirectory",
              "TypeFC": "WebGuiNode",
              "input_parameters": {
                "Source": "I'm from the parameters json",
                "Target": "I'm from the pipeline"
              },
              "Properties": {
                "Source": {
                  "prop": "I'm from the pipeline too!",
                  "init_val": "",
                  "type": "App::PropertyPath",
                  "Heading": "Parameters",
                  "tooltip": "The source directory",
                  "current_val": ""
                },
                "Target": {
                  "prop": "Target",
                  "init_val": "",
                  "type": "App::PropertyPath",
                  "Heading": "Parameters",
                  "tooltip": "The target directory",
                  "current_val": ""
                }
              },
              "WebGui": {}
            }
          },
          "RunPythonScript": {
            "Template": {
              "typeExecution": "RunPythonScript",
              "TypeFC": "WebGuiNode",
              "input_parameters": {
                "ModulePath": "Properties.ModulePath.current_val",
                "MethodName": "Properties.MethodName.current_val",
                "Parameters": "Properties.Parameters.current_val"
              },
              "Properties": {
                "ModulePath": {
                  "prop": "ModulePath",
                  "init_val": "",
                  "type": "App::PropertyPath",
                  "Heading": "PythonNodule",
                  "tooltip": "The path to the python module directory",
                  "current_val": ""
                },
                "MethodName": {
                  "prop": "MethodName",
                  "init_val": "",
                  "type": "App::PropertyString",
                  "Heading": "PythonNodule",
                  "tooltip": "The python module name",
                  "current_val": ""
                },
                "Parameters": {
                  "prop": "Parameters",
                  "init_val": [],
                  "type": "App::PropertyStringList",
                  "Heading": "PythonNodule",
                  "tooltip": "The python module input parameters",
                  "current_val": []
                }
              },
              "WebGui": {}
            }
          }
        }
      }
}