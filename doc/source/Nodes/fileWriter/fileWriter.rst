fileWriter Node
=================
This node is responsible for writing files.


.. raw:: html

   <h3 id=type_h>Type</h3>
   <hr>

.. code-block:: javascript

    "type" : "general.FilesWriter"


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
   * - directoryPath
     - The path of the directory
   * - Files
     - A list of all the files to be written.
   * - casePath
     - The path of the case

**Files**
    Each file to be written will be define as follow

.. code-block:: javascript

       "NodeName": {
          "fileName": "dir/fileName",
          "fileContent": "{path.to.content}"
       }


`up <#type_h>`_

.. raw:: html

   <h3 id="Example_h">Example</h3>
   <hr>
   <h4>JSON File  (input) </h4>


.. literalinclude:: fileWriter_example.json
   :language: JSON
   :linenos:

.. raw:: html

    <hr style="border: 1px dashed;">
    <h4>Output</h4>

| All The files in the list are being created, and filled with the content mentioned in the JSON.
|


`up <#type_h>`_

.. raw:: html

   <hr>
