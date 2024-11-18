createEmptyCase
===============
initial the simulation by creating an empty case

.. raw:: html

   <h3>Type</h3>
   <hr>

.. code-block:: javascript

    "type" : "general.RunOsCommand"

.. raw:: html

   <h3>Execution</h3>
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

.. code-block:: javascript

    "input_parameters": {
        "Method": "Command list",
        "Command": "hera-openFoam {workflow.solver} case createEmpty {Parameters.output.targetDirectory} --fields {workflow.SolvedFields}"
    }

.. raw:: html

   <hr>
