momentumTransport Node
======================

The momentumTransport dictionary is used in simulations involving turbulence modeling and fluid flow. It controls properties related to the momentum transport equations, including viscosity, turbulence models, and associated parameters.


.. table:: Table of content
   :align: left

   ================= ============================ =======================
   `Type <#type_h>`_  `Execution <#Execution_h>`_ `Example <#Example_h>`_
   ================= ============================ =======================

.. raw:: html

   <h3 id="type_h">Type</h3>
   <hr>

.. code-block:: javascript

    "type" : "openFOAM.constant.momentumTransport"


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
   * - simulationType
     - string
     - specifies the type of simulation to be performed with respect to turbulence modeling: RAS | laminar | LES
   * - Model
     - string
     - turbulance model depend on the simulationType. RAS: kEpsilon | kOmegaSST | SpalartAllmaras | LienLeschziner; LES: Smagorinsky | WALE
   * - turbulence
     - boolean
     - toggles turbulence modeling (on or off).


`up <#type_h>`_

.. raw:: html

   <h3 id="Example_h">Example</h3>
   <hr>
   <h4>JSON File  (input) </h4>


.. literalinclude:: momentumTransport_example.json
   :language: JSON
   :linenos:

.. raw:: html

    <hr style="border: 1px dashed;">
    <h4>OpenFOAM dictionary (output)</h4>

.. literalinclude:: momentumTransport
   :language: none
   :linenos:

`up <#type_h>`_

.. raw:: html

   <hr>
