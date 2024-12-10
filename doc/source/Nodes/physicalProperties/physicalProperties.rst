physicalProperties Node
=======================
The physicalProperties is used to define the transport properties of a fluid or material in a simulation. The dictionary is located in the constant directory of the case setup and is typically employed for solvers involving fluid flow, such as simpleFoam, pimpleFoam, or icoFoam.


.. table:: Table of content
   :align: left

   ================= ============================ =======================
   `Type <#type_h>`_  `Execution <#Execution_h>`_ `Example <#Example_h>`_
   ================= ============================ =======================

.. raw:: html

   <h3 id="type_h">Type</h3>
   <hr>

.. code-block:: javascript

    "type" : "openFOAM.constant.physicalProperties"


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
   * - parameters
     - struct
     - A list of addition parameters if the simulation needs it( thermal and etc.).

**parametrs**

Each parameter will include 3 sub-parameters.

.. list-table::
   :widths: 25 25 250
   :header-rows: 1
   :align: left

   * - SubParameter
     - Data Type
     - Description
   * - printName
     - boolean
     - flag to turn on print the name of parameter.
   * - dimensions
     - list
     - a vector of the dimention of the parameter - [mass length time temperature moles current luminous intensity]
   * - value
     - number
     - The value of the parameter

*optional parameters*

    | beta : Thermal expansion coefficient [1/K]
    | Tref : Reference temperature [K]
    | Pr   : Prandtl number (laminar flows)
    | Prt  : Turbulent Prandtl number


.. code-block:: javascript

    "parameters": {
        "beta": {
            "printName": true,,
            "dimensions": "[0 0 0 -1 0 0 0]",
            "value": 0.0033333333333333335
        }
        "other parametet" {...}
    }


`up <#type_h>`_

.. raw:: html

   <h3 id="Example_h">Example</h3>
   <hr>
   <h4>JSON File  (input) </h4>


.. literalinclude:: physicalProperties_example.json
   :language: JSON
   :linenos:

.. raw:: html

    <hr style="border: 1px dashed;">
    <h4>OpenFOAM dictionary (output)</h4>

.. literalinclude:: physicalProperties
   :language: none
   :linenos:

`up <#type_h>`_


.. raw:: html

   <hr>
