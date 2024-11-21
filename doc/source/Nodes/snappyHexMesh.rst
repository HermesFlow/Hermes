SnappyHexMesh Node
===================

SnappyHexMesh node is used for automated mesh generation. Its primary purpose is to create
high-quality computational meshes for solving problems in computational fluid dynamics (CFD) and other fields. It’s particularly well-suited for complex geometries and supports adaptive refinement, making it a powerful alternative to manual meshing.


.. raw:: html

   <h3>Type</h3>
   <hr>

.. code-block:: javascript

    "type" : "openFOAM.mesh.SnappyHexMesh"


.. raw:: html

   <h3>Execution</h3>
   <hr>
   <h4>input_parameters</h4>

The main parameters for the SnappyHexMesh node.

.. list-table::
   :widths: 25 50
   :header-rows: 1
   :align: left

   * - Parameter
     - Description
   * - modules
     - Define general parameters of SnappyHexMesh
   * - castellatedMeshControls
     - To switch on creation of the castellated mesh
   * - snapControls
     - To switch on surface snapping stage
   * - addLayersControls
     - To switch on surface layer insertion.
   * - meshQualityControls
     - Controls for mesh quality.
   * - geometry
     - Define all surface geometry used.

.. raw:: html

    <hr style="border: 1px dashed;">

**modules**

The modules section is responsible for the general properties of the SnappyHexMesh node.

.. list-table::
   :widths: 25 20 50
   :header-rows: 1
   :align: left

   * - Sub-Parameter
     - Data Type
     - Description
   * - castellatedMesh
     - boolean
     - Define if using castellatedMesh
   * - snap
     - boolean
     - Define if using snap
   * - layers
     - boolean
     - Define if using layers
   * - mergeTolerance
     - number
     - Define a tolerance


.. code-block:: javascript

    "modules": {
        "castellatedMesh": true,
        "snap": true,
        "layers": true,
        "mergeTolerance": 1e-6
    }

.. raw:: html

    <hr style="border: 1px dashed;">

**castellatedMeshControls**

The castellatedMeshControls define the properties to switch on creation of the castellated mesh

.. list-table::
   :widths: 25 25 50
   :header-rows: 1
   :align: left

   * - Sub-Parameter
     - Data Type
     - Description
   * - maxLocalCells
     - number
     - max number of cells per processor during refinement.
   * - maxGlobalCells
     - number
     - overall cell limit during refinement (i.e. before removal).
   * - minRefinementCells
     - number
     -  if minRefinementCells ≥ \relax \special {t4ht= number of cells to be refined, surface refinement stops.
   * - maxLoadUnbalance
     - number
     - Controls the maximum allowable load imbalance during the parallel execution of SnappyHexMesh.
   * - nCellsBetweenLevels
     - number
     -  number of buffer layers of cells between successive levels of refinement (typically set to 3).
   * - resolveFeatureAngle
     - number
     - pplies maximum level of refinement to cells that can see intersections whose angle exceeds resolveFeatureAngle (typically set to 30).
   * - allowFreeStandingZoneFaces
     - boolean
     - Determines whether isolated faces are allowed in zone boundaries.
   * - locationInMesh
     - vector [ x, y, z]
     - location vector inside the region to be meshed; vector must not coincide with a cell face either before or during refinement.


.. code-block:: javascript

    "castellatedMeshControls": {
         "maxLocalCells": 100000,
         "maxGlobalCells": 100000000,
         "minRefinementCells": 40,
         "maxLoadUnbalance": 0.1,
         "nCellsBetweenLevels": 8,
         "resolveFeatureAngle": 30,
         "allowFreeStandingZoneFaces": true,
         "locationInMesh": [ 0.2, 0.2, 0.1]
     }

.. raw:: html

    <hr style="border: 1px dashed;">

**snapControls**

.. list-table::
   :widths: 25 20 50
   :header-rows: 1
   :align: left

   * - Sub-Parameter
     - Data Type
     - Description
   * - nSmoothPatch
     - number
     - number of patch smoothing iterations before finding correspondence to surface (typically 3).
   * - tolerance
     - number
     - ratio of distance for points to be attracted by surface feature point or edge, to local maximum edge length (typically 2.0).
   * - SolveIter
     - number
     - number of mesh displacement relaxation iterations (typically 30-100).
   * - nRelaxIter
     - number
     - maximum number of snapping relaxation iterations (typically 5).
   * - nFeatureSnapIter
     - number
     - Number of iterations for feature snapping
   * - explicitFeatureSnap
     - boolean
     - Snapping to explicitly defined features (e.g., featureEdgeMesh)
   * - multiRegionFeatureSnap
     - boolean
     - Snapping to features at region boundaries (multi-region setups)
   * - implicitFeatureSnap
     - boolean
     - Snapping to features detected from geometry curvature

.. code-block:: javascript

    "snapControls": {
         "nSmoothPatch": 5,
         "tolerance": 6.0,
         "SolveIter": 200,
         "nRelaxIter": 5,
         "nFeatureSnapIter": 10,
         "explicitFeatureSnap": false,
         "multiRegionFeatureSnap": false,
         "implicitFeatureSnap": true
     }


.. raw:: html

    <hr style="border: 1px dashed;">

**addLayersControls**

.. list-table::
   :widths: 25 20 50
   :header-rows: 1
   :align: left

   * - Sub-Parameter
     - Data Type
     - Description
   * - Data
     - number
     - desc

.. code-block:: javascript

    "addLayersControls": {
         "relativeSizes": true,
         "expansionRatio": 1.05,
         "finalLayerThickness": 0.9,
         "minThickness": 0.01,
         "featureAngle": 100,
         "slipFeatureAngle": 30,
         "nLayerIter": 50,
         "nRelaxedIter": 20,
         "nRelaxIter": 5,
         "nGrow": 0,
         "nSmoothSurfaceNormals": 1,
         "nSmoothNormals": 3,
         "nSmoothThickness": 10,
         "maxFaceThicknessRatio": 0.5,
         "maxThicknessToMedialRatio": 0.3,
         "minMedianAxisAngle": 90,
         "nMedialAxisIter": 10,
         "nBufferCellsNoExtrude": 0,
         "additionalReporting": false
     }

.. raw:: html

    <hr style="border: 1px dashed;">

**meshQualityControls**

.. list-table::
   :widths: 25 20 50
   :header-rows: 1
   :align: left

   * - Sub-Parameter
     - Data Type
     - Description
   * - Data
     - type
     - desc

.. code-block:: javascript

    "meshQualityControls": {
         "maxBoundarySkewness": 20,
         "maxInternalSkewness": 4,
         "maxConcave": 80,
         "minVol": 1e-13,
         "minTetQuality": -1e+30,
         "minArea": -1,
         "minTwist": 0.02,
         "minDeterminant": 0.001,
         "minFaceWeight": 0.05,
         "minVolRatio": 0.01,
         "minTriangleTwist": -1,
         "nSmoothScale": 4,
         "errorReduction": 0.75,
         "relaxed": {
            "maxNonOrtho": 75
         }
     }

.. raw:: html

    <hr style="border: 1px dashed;">

**geometry**

.. list-table::
   :widths: 25 20 50
   :header-rows: 1
   :align: left

   * - Sub-Parameter
     - Data Type
     - Description
   * - Data
     - type
     - desc

.. code-block:: javascript

    "geometry": {
         "param": 100000,
     }


.. raw:: html

   <h3>Example</h3>
   <hr>

+--------------------------------------------+--------------------------------------------+
|           **JSON FILE**                    |         **Dictionary**                     |
+--------------------------------------------+--------------------------------------------+
| .. literalinclude:: blockMesh_example.json | .. literalinclude:: blockMesh_example.json |
|   :language: JSON                          |   :language: JSON                          |
|   :linenos:                                |   :linenos:                                |
+--------------------------------------------+--------------------------------------------+

.. raw:: html

   <hr>

