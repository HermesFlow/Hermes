buildAllRun Node
=================
This node is responsible for

.. table:: Table of content
   :align: left

   ================= ============================ =======================
   `Type <#type_h>`_  `Execution <#Execution_h>`_ `Example <#Example_h>`_
   ================= ============================ =======================

.. raw:: html

   <h3 id=type_h>Type</h3>
   <hr>

.. code-block:: javascript

    "type" : "openFOAM.BuildAllrun"


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
   * - casePath
     - The path of the case
   * - caseExecution
     - parameters of how to execute the case
   * - parallelCase
     - A boolean value that says is the simulation could run in parallel.
   * - runFile
     - A list of nodes and how to execute them

.. raw:: html

   <hr style="border: 1px dotted">

**caseExecution**

An item in the runFile list will be look as follow

.. list-table::
   :widths: 25 50
   :header-rows: 1
   :align: left

   * - subParameter
     - Description
   * - parallelCase
     - A boolean value that says if the Case could run in parallel.
   * - slurm
     - A boolean value that says if the ____
   * - getNumberOfSubdomains
     - get the __
   * - runFile
     - a list of ____


.. code-block:: javascript

       "caseExecution":{
       {
           "parallelCase": true,
           "slurm": false,
           "getNumberOfSubdomains": 10
           "runFile": []
       }


.. raw:: html

   <hr style="border: 1px dotted">

**runFile**

An item in the runFile list will be look as follow

.. list-table::
   :widths: 25 50
   :header-rows: 1
   :align: left

   * - subParameter
     - Description
   * - name
     - The name of the node
   * - couldRunInParallel
     - A boolean value that says is the node could run in parallel.
   * - parameters
     - parameters of how to execute the case


.. code-block:: javascript

       {
           "name": "blockMesh",
           "couldRunInParallel": false,
           "parameters": null
       }



`up <#type_h>`_

.. raw:: html

   <h3 id="Example_h">Example</h3>
   <hr>
   <h4>JSON File  (input) </h4>


.. literalinclude:: buildAllRun_example.json
   :language: JSON
   :linenos:


.. raw:: html

    <hr style="border: 1px dashed;">
    <h4>Output</h4>

|
|


`up <#type_h>`_

.. raw:: html

   <hr>
