Workflow 2: Running OS command and creating file using template
===============================================================

The following workflow first creates a directory using a sytem call
and then generate a file names README.txt.
The file contains the line

::
    We will now write the sentence 3 times:
        1. My name is Tester and my Directory is myCase
        2. My name is Tester and my Directory is myCase
        3. My name is Tester and my Directory is myCase

However, the number of lines, the name of the user and the case are parameters that
passed from the workflow itself. Hence, to do so,  Hermes uses the Jinja2 engine.

A Jinja template file that produces the requested output is

::

    We will now write the sentence {{repeat}} times:
        {%- for pnt in range(repeat) %}
            {{pnt+1}}. My name is {{myName}} and my Directory is {{directoryName}}
        {%- endfor %}

Where repeat, myName and directoryName are parameters that are provided to the template file.

The workflow that creates the directory and the file is

.. code-block:: javascript

    {
        "workflow": {
            "nodes": {
                "Parameters": {
                    "Execution": {
                        "input_parameters": {
                            "directoryName": "myCase",
                            "name": "Tester"
                        }
                    },
                    "type": "general.Parameters"
                },
                "createDirectory": {
                    "Execution": {
                        "input_parameters": {
                            "Command": "mkdir {Parameters.output.directoryName}"
                        }
                    },
                    "type": "general.RunOsCommand"
                },
                "makeTemplate": {
                    "Execution": {
                        "input_parameters": {
                            "path": [
                                "."
                            ],
                            "parameters": {
                                "myName": "{Parameters.output.name}",
                                "directoryName": "{Parameters.output.directoryName}",
                                "repeat": 3
                            },
                            "template": "myTemplate"
                        }
                    },
                    "type": "general.JinjaTransform"
                },
                "writeFile": {
                    "Execution": {
                        "input_parameters": {
                            "directoryPath": "{Parameters.output.directoryName}",
                            "Files": {
                                "README": {
                                    "fileName": "README.txt",
                                    "fileContent": "{makeTemplate.output.renderedText}"
                                }
                            }
                        },
                        "requires": "createDirectory"
                    },
                    "type": "general.FilesWriter"
                }
            }
        }
    }

Building and executing the workflow is just as before:
::

    >> hermes-workflow buildExecute workflow.json

The **parameters** node is a comfortable way to collect all the important parameters that are expected to change during the simulation
in a single place. However, it is not necessary, as the parameters can be written directly to the relevant node in the JSON.

The **makeTemplate** node just creates the rendedred text and does not save it to the disk. The actual writing takes place
when the **writeFile** node is executed. Because the file can only be written after the directory was created,
the **writeFile** node requires the **createDirectory** node. That is, the execution of this node is delayed until the
**createDirectory** node is complete. We note, that since **writeFile** uses the outputs of the **makeTemplate** and
**Parameters** nodes, then its execution starts only after these nodes were executed.



