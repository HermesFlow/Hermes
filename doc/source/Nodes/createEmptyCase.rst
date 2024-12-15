createEmptyCase
===============
Initial the simulation by creating an empty case

.. table:: Table of content
   :align: left

   ================= ============================ =======================
   `Type <#type_h>`_  `Execution <#Execution_h>`_ `Example <#Example_h>`_
   ================= ============================ =======================

.. raw:: html

   <h3 id="type_h">Type</h3>
   <hr>

.. code-block:: javascript

    "type" : "general.RunOsCommand"

.. raw:: html

   <h3 id="Execution_h">Execution</h3>
   <hr>

**input_parameters**

.. |br| raw:: html

   <br/>

.. list-table::
   :widths: 25 50
   :header-rows: 1
   :align: left

   * - Parameter
     - Description
   * - Method
     - How the OS command is called |br| here: "Command list"
   * - Command
     - The OS commands goiog to be execute

`up <#type_h>`_

.. raw:: html

   <h3 id="Example_h">Example</h3>
   <hr>
   <h4>JSON File  (input) </h4>

.. code-block:: javascript

    "input_parameters": {
        "Method": "Command list",
        "Command": "hera-openFoam {workflow.solver} case createEmpty {Parameters.output.targetDirectory} --fields {workflow.SolvedFields}"
    }

.. raw:: html

    <hr style="border: 1px dashed;">
    <h4>Output</h4>

| Create an empty case by running the "Commands" with the "Method" mentioned.
|

`up <#type_h>`_

.. raw:: html

   <hr>
