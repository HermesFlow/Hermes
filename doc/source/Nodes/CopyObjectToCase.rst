CopyObjectToCase
=================
This node is responsible for coping a file to a wanted path.


.. raw:: html

   <h3>Type</h3>
   <hr>

.. code-block:: javascript

    "type" : "general.CopyFile"


.. raw:: html

   <h3>Execution</h3>
   <hr>

**Requirement**

.. code-block:: javascript

    "requires": "createEmptyCase"

|

.. raw:: html

   <hr style="border: 1px dashed">


**input_parameters**

.. list-table::
   :widths: 25 50
   :header-rows: 1
   :align: left

   * - Parameter
     - Description
   * - Source
     - The path of the file want to be copied
   * - Target
     - The path to directory that the file will be copied to.

.. code-block:: javascript

    "input_parameters": {
        "Source": "{Parameters.output.objectFile}",
        "Target": "{Parameters.output.targetDirectory}/{Parameters.output.objectFile}"
    }

.. raw:: html

   <hr>
