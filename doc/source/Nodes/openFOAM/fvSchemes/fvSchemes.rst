fvSchemes
==========

The fvSchemes dictionary defines the numerical discretization schemes used for solving equations in a simulation. It determines how derivatives, gradients, interpolations, and fluxes are approximated on the computational mesh. Proper selection of schemes is essential for the accuracy, stability, and efficiency of the solution.


.. table:: Table of content
   :align: left

   ================= ============================ =======================
   `Type <#type_h>`_  `Execution <#Execution_h>`_ `Example <#Example_h>`_
   ================= ============================ =======================

.. raw:: html

   <h3 id="type_h">Type</h3>
   <hr>

.. code-block:: javascript

    "type" : "openFOAM.system.FvSchemes"


.. raw:: html

   <h3 id="Execution_h">Execution</h3>
   <hr>

**input_parameters**

The fvSchemes separates the definition of the default value of the simulation, and the fields' specific values. Yet,
the parameters to be defined are the same.

.. list-table::
   :widths: 25 20 250
   :header-rows: 1
   :align: left

   * - Parameter
     - Data Type
     - Description
   * - ddtSchemes
     - string
     - Time-derivative schemes: Euler | backward | CrankNicolson
   * - gradSchemes
     - string
     - Gradient schemes: Gauss linear | Gauss leastSquares
   * - divSchemes
     - list | struct
     - Divergence schemes (elaborate below)
   * - laplacianSchemes
     - list | struct
     - Laplacian operator schemes  (elaborate below)
   * - interpolationSchemes
     - string
     - Interpolation schemes for values at face centers: linear | upwind
   * - snGradSchemes
     - string
     - Surface-normal gradient schemes: uncorrected | corrected | limited
   * - wallDist
     - string
     - specify the discretization scheme for calculating the wall distance field (turbulence): meshWave | propagated
   * - fluxRequired
     - string
     - specifies which fields require flux computations for certain boundary conditions or solver operations: "yes" - enable, "no" disable calculation of the flux.

.. raw:: html

    <hr style="border: 1px dotted;">

**divSchemes**

Specifies how divergence terms ∇⋅(ϕU) are calculated in the equations. This is critical for convection-dominated problems.

*input*

.. list-table::
   :widths: 25 20 250
   :header-rows: 1
   :align: left

   * - Parameter
     - Data Type
     - Description
   * - type
     - string
     - The major divergence method : Gauss
   * - name
     - string
     - The sub divergence method : upwind | linear | limitedLinear | QUICK
   * - parameters
     - string
     - A place to add data or equation.
   * - phi
     - string
     - refers to the flux ϕ = ρU -> "phi"
   * - noOfOperators
     - number
     -

default:

.. code-block:: javascript

    "divSchemes": {
       "type": "Gauss",
       "name": "linear",
       "parameters": ""
    }



field:

.. code-block:: javascript

   "U":{
       "divSchemes": [
          {
             "noOfOperators": 2,
            "phi": "phi",
            "type": "Gauss",
            "name": "SuperBeeV",
            "parameters": ""
          }
       ],
   }

*output*

.. code-block:: javascript

    divSchemes
    {
       default               Gauss linear ;
       div(phi,U) Gauss SuperBeeV ;
    }

.. raw:: html

    <hr style="border: 1px dotted;">

**laplacianSchemes**

Defines how diffusion terms ∇2ϕ are computed.

*input*

.. list-table::
   :widths: 25 20 250
   :header-rows: 1
   :align: left

   * - Parameter
     - Data Type
     - Description
   * - type
     - string
     - The major divergence method : Gauss
   * - name
     - string
     - The sub divergence method : linear
   * - parameters
     - string
     - A place to add data or equation: uncorrected | corrected | limited
   * - coefficient
     - string
     - other simulation parameters to calculate the laplacian on.
   * - noOfOperators
     - number
     -

*input*

default:

.. code-block:: javascript

    "laplacianSchemes": {
       "type": "Gauss",
       "name": "linear",
       "parameters": "uncorrected"
    }

field:

.. code-block:: javascript

    "U":{
       "laplacianSchemes": [
           {
              "noOfOperators": 2,
              "coefficient": "nuEff",
              "type": "Gauss",
              "name": "linear",
              "parameters": "uncorrected"
           },
           {
               "noOfOperators": 2,
               "coefficient": "AnisotropicDiffusion",
               "type": "Gauss",
               "name": "linear",
               "parameters": "uncorrected"
           }
       ],
    }

*output*

.. code-block:: javascript

    laplacianSchemes
    {
       default               Gauss linear uncorrected;
       laplacian((1|A(U)),p) Gauss linear uncorrected;
       laplacian(nuEff,U) Gauss linear uncorrected;
    }


`up <#type_h>`_

.. raw:: html

   <h3 id="Example_h">Example</h3>
   <hr>
   <h4>JSON File  (input) </h4>


.. literalinclude:: fvSchemes_example.json
   :language: JSON
   :linenos:

.. raw:: html

    <hr style="border: 1px dashed;">
    <h4>OpenFOAM dictionary (output)</h4>

.. literalinclude:: fvSchemes
   :language: none
   :linenos:

`up <#type_h>`_


.. raw:: html

   <hr>