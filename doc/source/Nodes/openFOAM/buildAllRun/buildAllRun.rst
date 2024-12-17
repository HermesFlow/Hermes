buildAllRun
============
The buildAllRun node writes the allRun file that executes the workflow, and the allClean file that cleans the case to
the case directory.

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
   :widths: 25 25 50
   :header-rows: 1
   :align: left

   * - subParameter
     - type
     - Description
   * - parallelCase
     - boolean
     - Write the execution for parallel execution
   * - slurm
     - boolean
     - A boolean value that says if using SLURM (Simple Linux Utility for Resource Management)
   * - getNumberOfSubdomains
     - number
     - The number of subdomains to use in the run file.
   * - runFile
     -
     - a list of nodes


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
   :widths: 25 25 50
   :header-rows: 1
   :align: left

   * - subParameter
     - type
     - Description
   * - name
     - string
     - The name of the node to execute
   * - couldRunInParallel
     - boolean
     - Write as parallel (only if parallel case is True).
   * - parameters
     - null | string
     - Parameters for each run
   * - foamJob
     - boolean
     - define using foamJob to run this task
   * - screen
     - boolean
     - write log to screen
   * - wait
     - boolean
     - wait to the end of execution before next step



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
    <h4>Allrun file (output)</h4>

.. literalinclude:: Allrun
   :language: none
   :linenos:


.. raw:: html

    <hr style="border: 1px dashed;">
    <h4>Allclean file (output)</h4>

.. literalinclude:: Allclean
   :language: none
   :linenos:

`up <#type_h>`_

.. raw:: html

   <hr>
