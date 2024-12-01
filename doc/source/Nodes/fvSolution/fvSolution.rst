fvSolution Node
===============



.. table:: Table of content
   :align: left

   ================= ============================ =======================
   `Type <#type_h>`_  `Execution <#Execution_h>`_ `Example <#Example_h>`_
   ================= ============================ =======================

.. raw:: html

   <h3 id="type_h">Type</h3>
   <hr>

.. code-block:: javascript

    "type" : "openFOAM.system.FvSolution"


.. raw:: html

   <h3 id="Execution_h">Execution</h3>
   <hr>

**input_parameters**

.. list-table::
   :widths: 25 20 250
   :header-rows: 1
   :align: left

   * - Parameter
     - Data Type
     - Description
   * - application
     - string
     - The type of the simulation


.. code-block:: javascript

    "input_parameters": {
        "values": {
            }
    }

`up <#type_h>`_

.. raw:: html

   <h3 id="Example_h">Example</h3>
   <hr>
   <h4>JSON File  (input) </h4>


.. literalinclude:: fvSolution_example.json
   :language: JSON
   :linenos:

.. raw:: html

    <hr style="border: 1px dashed;">
    <h4>OpenFOAM dictionary (output)</h4>

.. literalinclude:: fvSolution
   :language: OpenFOAM dictionary
   :linenos:

`up <#type_h>`_

.. raw:: html

   <hr>