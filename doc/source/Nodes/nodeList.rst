Hermes Nodes
============

The nodes in Hermes are divided into types to ease the search for a specific function.

Currently, there are general nodes that execute tasks such as:
    * creating files or directories
    * copying or moving files or directories
    * executing OS command or python script
    * creating text files from templates.
    * writing the output of a node to a file.

Each node is characterized by its input parameters, the task it performes when executed and its
output parameters.

The Basic Json Structure Of A Node
----------------------------------
.. code-block:: javascript

    "NodeName": {
        "type": "path.to.node.dir",
        "Execution": {
            "input_parameters": {
                "param": "value"
            }
            "requires":"NodeName"
        },
        "GUI":{
        }
    }

Each node contain 3 inputs:
    1. type - define the functionality of the node and what it supposed to do.
    2. Execution - define the input data that the node needs in order to operate its functionality.
    3. GUI - The data needed to display the nodes data in the GUI.
|


.. toctree::
   :maxdepth: 2
   :caption: The Nodes List:

   Parameters.rst
   createEmptyCase.rst
   CopyObjectToCase.rst
   CopyBuildingObject.rst
   blockMesh/blockMesh.rst
   snappyHexMesh/snappyHexMesh.rst
   controlDict/controlDict.rst
   fvSchemes/fvSchemes.rst
   fvSolution/fvSolution.rst