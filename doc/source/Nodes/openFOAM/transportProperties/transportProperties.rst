transportProperties
====================
The transportProperties is used to define the transport properties of a fluid or material in a simulation. The dictionary is located in the constant directory of the case setup and is typically employed for solvers involving fluid flow, such as simpleFoam, pimpleFoam, or icoFoam.


|

.. raw:: html

   <hr>

**It can be used with OpenFOAM V7-V10**

.. raw:: html

   <hr>

|

.. table:: Table of content
   :align: left

   ================= ============================ =======================
   `Type <#type_h>`_  `Execution <#Execution_h>`_ `Example <#Example_h>`_
   ================= ============================ =======================

.. raw:: html

   <h3 id="type_h">Type</h3>
   <hr>

.. code-block:: javascript

    "type" : "openFOAM.constant.TransportProperties"


.. raw:: html

   <h3 id="Execution_h">Execution</h3>
   <hr>

**input_parameters**

.. list-table::
   :widths: 25 25 250
   :header-rows: 1
   :align: left

   * - Parameter
     - Data Type
     - Description
   * - transportModel
     - string
     - Defines how viscosity or transport properties are calculated: Newtonian | sutherland | powerLaw
   * - nu
     - number
     - Kinematic viscosity (m²/s).



`up <#type_h>`_

.. raw:: html

   <h3 id="Example_h">Example</h3>
   <hr>
   <h4>JSON File  (input) </h4>


.. literalinclude:: transportProperties_example.json
   :language: JSON
   :linenos:

.. raw:: html

    <hr style="border: 1px dashed;">
    <h4>OpenFOAM dictionary (output)</h4>

.. literalinclude:: transportProperties
   :language: none
   :linenos:

`up <#type_h>`_


.. raw:: html

   <hr>
