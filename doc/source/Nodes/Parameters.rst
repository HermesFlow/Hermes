Parameters
===========

Parameters is the node responsible for the general data needed for the case.



.. raw:: html

   <h3>Type</h3>
   <hr>

.. code-block:: javascript

    "type" : "general.Parameters"


.. raw:: html

   <h3>Execution</h3>
   <hr>

**input_parameters**

.. list-table::
   :widths: 25 50
   :header-rows: 1
   :align: left

   * - Parameter
     - Description
   * - OFversion
     - The OpenFOAM version that is used to run the case
   * - targetDirectory
     - The directory where the data will be saved
   * - objectFile
     - The CAD file of the case
   * - decomposeProcessors
     - Define the number of processors for a parallel run of the simulation.

.. code-block:: javascript

    "input_parameters": {
        "OFversion": "of10",
        "targetDirectory": "{#moduleName}",
        "objectFile": "CADobject.obj",
        "decomposeProcessors": 8
    }

.. raw:: html

   <hr>
