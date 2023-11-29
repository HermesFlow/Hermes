.. Hermes documentation master file, created by
   sphinx-quickstart on Thu Dec  5 12:11:55 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Hermes's documentation!
==================================

Hermes is a package that aims to simplify the batch operation of programs. Different than
other packages (..), the workflow is specified in JSON format, which allows queries and comparison of different workflows
using MongoDB.

The workflow is defined as a series of nodes, and the input to one node can be defined as the output of
another node. The hermes engine builds a python workflow using the luigi package which allows the
concomitant execution of all the node withc respect to their depencies.

An additional workbench was programmed using the opensource CAD program FreeCAD, so simplify the definition of
boundary conditions and complex objects in the simulation.

10 minute Tutorial
------------------

This tutorial shows how to run a Hermes workflow that will copy the directory named source to a directory
named target, and then execute

.. code-block:: javascript

    {
        "workflow": {
            "root": null,
            "nodeList": [
                "CopyDirectory",
                "RunPythonCode"
            ],
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



.. toctree::
   :maxdepth: 2
   :caption: Contents:

   Usage/UsingByExample.rst

   FreeCAD/FreeCAD.rst
   simpleWorkflow/intro.rst
   Json/JsonStructure.rst
   CLI/CLI.rst


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
