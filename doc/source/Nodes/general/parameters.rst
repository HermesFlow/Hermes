parameters
===========

Parameters is the node responsible for the general data needed for the case.

.. table:: Table of content
   :align: left

   ================= ============================ =======================
   `Type <#type_h>`_  `Execution <#Execution_h>`_ `Example <#Example_h>`_
   ================= ============================ =======================

.. raw:: html

   <h3 id="type_h">Type</h3>
   <hr>

.. code-block:: javascript

    "type" : "general.Parameters"


.. raw:: html

   <h3 id="Execution_h">Execution</h3>
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

`up <#type_h>`_

.. raw:: html

   <h3 id="Example_h">Example</h3>
   <hr>
   <h4>JSON File(input) </h4>

.. code-block:: javascript

    "input_parameters": {
        "OFversion": "of10",
        "targetDirectory": "{#moduleName}",
        "objectFile": "CADobject.obj",
        "decomposeProcessors": 8
    }

.. raw:: html

    <hr style="border: 1px dashed;">
    <h4>Output</h4>

| Update the parameters of the simulation.
|

.. raw:: html

   <hr>
