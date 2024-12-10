defineNewBoundaryConditions Node
================================
In OpenFOAM, the boundaryField section within a field file (e.g., U for velocity, p for pressure) specifies the
boundary conditions for that field. These boundary conditions describe how the field behaves at the domain
boundaries, which significantly affects the simulation results. This node is responsible for defining the boundary condition for all the fields.


.. table:: Table of content
   :align: left

   ================= ============================ =======================
   `Type <#type_h>`_  `Execution <#Execution_h>`_ `Example <#Example_h>`_
   ================= ============================ =======================

.. raw:: html

   <h3 id="type_h">Type</h3>
   <hr>

.. code-block:: javascript

    "type" : "openFOAM.system.ChangeDictionary"


.. raw:: html

   <h3 id="Execution_h">Execution</h3>
   <hr>

**input_parameters**

the input parameter include a structure of *fields* that contains a list of the boundary condition of each field.

.. list-table::
   :widths: 25 25 250
   :header-rows: 1
   :align: left

   * - Parameter
     - Data Type
     - Description
   * - internalField
     - string
     - set uniform or non-uniform values for the domain.
   * - boundaryField
     - struct
     - specify different types of boundary conditions.

| Each boundary will be defined by its name and a small structure containing its properties, such as type, value, refValue, etc.

**Boundary condition of OpenFOAM**

.. list-table::
   :widths: 25 250 50
   :header-rows: 1
   :align: left

   * - Name
     - Description
     - properties
   * - fixedValue
     - Sets the field to a constant value at the boundary.
     - value
   * - zeroGradient
     - Sets the gradient normal to the boundary to zero.
     - no need
   * - noSlip
     - Sets velocity to zero at walls (no-slip condition for viscous flows).
     - no need
   * - surfaceNormalFixedValue
     - Specifies a fixed value for a scalar or vector field, but only in the direction normal to the surface.
     - value, refValue
   * - fixedFluxPressure
     - Adjusts pressure to maintain consistent flux at the boundary.
     - value, rho
   * - kLowReWallFunction
     - Provides a low-Reynolds-number boundary condition for the turbulent kinetic energy (kk) near walls.
     - value, refValue
   * - nutLowReWallFunction
     - Applies a low-Reynolds-number treatment for the kinematic eddy viscosity (νtνt​) near walls.
     - value, refValue
   * - epsilonWallFunction
     - Provides a boundary condition for the turbulence dissipation rate (ϵϵ) at walls.
     - value, refValue




.. code-block:: javascript

      "epsilon": {
         "internalField": "uniform 0.01",
         "boundaryField": {
            "Walls": {
               "type": "fixedValue",
               "value": "uniform  6.3e-5"
            },
            "inlet": {
               "type": "zeroGradient"
            },
            "outlet": {
               "type": "zeroGradient"
            }
         }
      }



`up <#type_h>`_

.. raw:: html

   <h3 id="Example_h">Example</h3>
   <hr>
   <h4>JSON File  (input) </h4>


.. literalinclude:: defineNewBoundaryConditions_example.json
   :language: JSON
   :linenos:

.. raw:: html

    <hr style="border: 1px dashed;">
    <h4>OpenFOAM dictionary (output)</h4>

.. literalinclude:: defineNewBoundaryConditions
   :language: none
   :linenos:

`up <#type_h>`_

.. raw:: html

   <hr>
