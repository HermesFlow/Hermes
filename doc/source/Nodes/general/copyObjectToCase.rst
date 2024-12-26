copyObjectToCase
=================
This node is responsible for coping a file to a wanted path.

.. table:: Table of content
   :align: left

   ================= ============================ =======================
   `Type <#type_h>`_  `Execution <#Execution_h>`_ `Example <#Example_h>`_
   ================= ============================ =======================

.. raw:: html

   <h3 id="type_h">Type</h3>
   <hr>

.. code-block:: javascript

    "type" : "general.CopyFile"


.. raw:: html

   <h3 id="Execution_h">Execution</h3>
   <hr>

**Requirement**

.. code-block:: javascript

    "requires": "createEmptyCase"



`up <#type_h>`_

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

`up <#type_h>`_

.. raw:: html

   <h3 id="Example_h">Example</h3>
   <hr>
   <h4>JSON File  (input) </h4>

.. code-block:: javascript

    "input_parameters": {
        "Source": "{Parameters.output.objectFile}",
        "Target": "{Parameters.output.targetDirectory}/{Parameters.output.objectFile}"
    }


.. raw:: html

    <hr style="border: 1px dashed;">
    <h4>Output</h4>

| The File is being copied from the "Source" to the "Target" directory.


`up <#type_h>`_

.. raw:: html

   <hr>
