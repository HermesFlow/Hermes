blockMesh
==========
This node is responsible for coping a file to a wanted path.


.. raw:: html

   <h3>Type</h3>
   <hr>

.. code-block:: javascript

    "type" : "openFOAM.mesh.BlockMesh"


.. raw:: html

   <h3>Execution</h3>
   <hr>

**input_parameters**
There are 3 main parameters the blockmesh needs.

.. list-table::
   :widths: 25 50
   :header-rows: 1
   :align: left

   * - Parameter
     - Description
   * - geometry
     - Define the geometry properties
   * - boundary
     - a list of the Boundary conditions
   * - vertices
     - A list of coordinates of 8 vertices [ x, y, z]



.. code-block:: javascript

    "input_parameters": {
        "Source": "{Parameters.output.objectFile}",
        "Target": "{Parameters.output.targetDirectory}/{Parameters.output.objectFile}"
    }

.. raw:: html

   <hr>
