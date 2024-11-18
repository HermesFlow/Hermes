CopyBuildingObject
===================
This node is responsible for coping the case object to the wanted path.

.. raw:: html

   <h3>Type</h3>
   <hr>

.. code-block:: javascript

    "type" : "general.RunOsCommand"


.. raw:: html

   <h3>Execution</h3>
   <hr style="border: 1px solid">

**Requirement**

.. code-block:: javascript

    "requires": "CopyObjectToCase"

|

.. raw:: html

   <hr style="border: 1px dashed">

**Node input_parameters**

.. list-table::
   :widths: 25 50
   :header-rows: 1
   :align: left

   * - Parameter
     - Description
   * - Method
     - How the OS command is called
   * - Command
     - The OS commands goiog to be execute

.. code-block:: javascript

    "input_parameters": {
        "Method": "Command list",
        "Command": "surfaceMeshConvert {Parameters.output.objectFile} {Parameters.output.targetDirectory}/constant/triSurface/building.obj -scaleIn 0.001 -case {Parameters.output.targetDirectory}"
    }

.. raw:: html

   <hr>
