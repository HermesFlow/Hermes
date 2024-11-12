WebGUI Nodes
=============

The WebGUI nodes are the nodes that have the ability to accept data through a form that display to the user after
clicking The node.

.. toctree::
   :maxdepth: 2
   :caption: The WebGUI nodes:

   snappyHexMesh.rst
   controlDict.rst
   fvSchemes.rst
   fvSolution.rst
   transportProperties.rst
   turbulence.rst


The Basic Json Structure
-------------------------
.. code-block:: javascript

    "NodeName": {
        "type": "path.to.node.dir",
        "Execution": {
            "input_parameters": {
                "param": "value"
            }
        },
        "GUI":{
        }
    }



