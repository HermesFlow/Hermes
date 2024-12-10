fvSolution Node
===============
The fvSolution node is a key configuration file used to control the solution of equations and the settings for numerical
solvers. It is located in the system directory of an OpenFOAM case and serves as the primary interface for specifying how the solver behaves during a simulation.


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

The main parameters for the fvSolution node.

.. list-table::
   :widths: 25 250
   :header-rows: 1
   :align: left

   * - Parameter
     - Description
   * - `fields <#fields_h>`_
     - Defines the numerical methods and tolerances for solving individual fields,  such as pressure, velocity, or turbulence quantities.
   * - `solverProperties <#solverProperties_h>`_
     - Contains settings for iterative algorithms like SIMPLE (steady-state) or PIMPLE (transient).
   * - `relaxationFactors <#relaxationFactors_h>`_
     - Controls under-relaxation to improve numerical stability, especially for iterative solvers.

.. raw:: html

    <hr style="border: 1px dashed;">
    <h5 id="fields_h">fields</h5>

for each field (pressure, velocity and etc.) we will define a struct that contains the following parameters

.. list-table::
   :widths: 25 20 250
   :header-rows: 1
   :align: left

   * - Parameter
     - Data Type
     - Description
   * - solver
     - string
     - Specifies the algorithm (e.g., PCG, smoothSolver, GAMG).
   * - preconditioner
     - string
     - Defines the preconditioning method (e.g., DIC, DILU).
   * - tolerance
     - number
     - Absolute convergence criterion.
   * - relTol
     - number
     - Relative convergence criterion.
   * - maxIter
     - number
     - specifies the maximum number of iterations allowed for solving a field variable
   * - final
     - struct
     - This is the solver configuration used for the final correction step at the end of each time-step. It contains the same parameters as described above.


.. code-block:: javascript

    "fields": {
       "p": {
          "solver": "PCG",
          "preconditioner": "DIC",
          "tolerance": 1e-08,
          "relTol": 0.0001,
          "maxIter": 5000,
          "final": {
             "solver": "PCG",
             "preconditioner": "DIC",
             "tolerance": 1e-08,
             "relTol": 0,
             "maxIter": 5000
          }
       },
       "U" :
       {
          ...
       },
       ...
    }


`up <#type_h>`_

.. raw:: html

    <hr style="border: 1px dashed;">
    <h5 id="solverProperties_h">solverProperties</h5>

This section defines which solver will be used in the simulation. Also, define the specific parameters of the solver.

.. list-table::
   :widths: 25 20 250
   :header-rows: 1
   :align: left

   * - Parameter
     - Data Type
     - Description
   * - algorithm
     - string
     - Choose the algorithm of the simulation: SIMPLE | PISO | SIMPLEC | PIMPLE | GAMG
   * - residualControl
     - struct
     - Provides convergence criteria for field variables, defining the target residuals below which the solution is considered converged for each field.
   * - solverFields
     - struct
     - Define the solver specific parameters (elaborated below)

**SIMPLE Solver**

The SIMPLE (Semi-Implicit Method for Pressure-Linked Equations) solver is an algorithm primarily used for solving steady-state problems involving incompressible or weakly compressible flows. It operates by iteratively solving for the velocity and pressure fields to satisfy the momentum and continuity equations.

.. list-table::
   :widths: 25 20 250
   :header-rows: 1
   :align: left

   * - Parameter
     - Data Type
     - Description
   * - nNonOrthogonalCorrectors
     - number
     - Specifies the number of additional corrector loops to address non-orthogonality in the mesh geometry during the pressure equation solution.
   * - pRefCell
     - number
     - Index of the cell where the reference pressure is set.
   * - pRefValue
     - number
     - Value of the reference pressure at the specified cell.
   * - momentumPredictor
     - string
     - determines whether to solve the momentum equation (velocity prediction) before solving the pressure correction equation.
   * - nOuterCorrectors
     - number
     - Specifies the number of outer correction loops performed during each SIMPLE iteration.
   * - nCorrectors
     - number
     - Determines the number of inner pressure-velocity correction loops (SIMPLE correctors) performed during each time step.
   * - nonlinearSolver
     - string
     - Specifies the nonlinear solver method used for the SIMPLE algorithm.


.. code-block:: javascript

    "solverProperties": {
       "algorithm": "SIMPLE",
       "residualControl": {
          "p": 0.0001,
          "U": ...,
          ...
       },
       "solverFields": {
          "nNonOrthogonalCorrectors": 2,
          "pRefCell": 0,
          "pRefValue": 0,
          "momentumPredictor": "yes",
          "nOuterCorrectors": 2,
          "nCorrectors": 2,
          "nonlinearSolver": "fixedPoint"
       }
    }

`up <#type_h>`_

.. raw:: html

    <hr style="border: 1px dashed;">
    <h5 id="relaxationFactors_h">relaxationFactors</h5>

Relaxation factors reduce the change in a variable between iterations, effectively slowing down the solution updates. They are a critical component in achieving convergence for steady-state problems.

.. list-table::
   :widths: 25 20 250
   :header-rows: 1
   :align: left

   * - Parameter
     - Data Type
     - Description
   * - fields
     - struct
     - Applies to the variables directly. For each field we will define its value.
   * - equations
     - struct
     - Applies to the equations being solved for the fields. This can be used when solving equations where fields are tightly coupled. for each field  we will define its factor and final values.


.. code-block:: javascript

    "relaxationFactors": {
        "fields": {
           "p": 0.15,
           "U": ...,
           ...
        },
        "equations": {
           "p": {
              "factor": 0.4,
              "final": 0.4
        },
           "U": {
               ...
           },
           ...
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
   :language: none
   :linenos:

`up <#type_h>`_


.. raw:: html

   <hr>