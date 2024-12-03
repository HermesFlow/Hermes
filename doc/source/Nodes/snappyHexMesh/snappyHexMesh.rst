SnappyHexMesh Node
===================

SnappyHexMesh node is used for automated mesh generation. Its primary purpose is to create
high-quality computational meshes for solving problems in computational fluid dynamics (CFD) and other fields. It’s particularly well-suited for complex geometries and supports adaptive refinement, making it a powerful alternative to manual meshing.

.. table:: Table of content
   :align: left

   ================= ============================ =======================
   `Type <#type_h>`_  `Execution <#Execution_h>`_ `Example <#Example_h>`_
   ================= ============================ =======================


.. raw:: html

   <h3 id="type_h">Type</h3>
   <hr>

.. code-block:: javascript

    "type" : "openFOAM.mesh.SnappyHexMesh"


.. raw:: html

   <h3 id="Execution_h">Execution</h3>
   <hr>
   <h4 id="input_parameters_h">input_parameters</h4>

The main parameters for the SnappyHexMesh node.

.. list-table::
   :widths: 25 50
   :header-rows: 1
   :align: left

   * - Parameter
     - Description
   * - `modules <#modules_h>`_
     - Define general parameters of SnappyHexMesh
   * - `castellatedMeshControls <#castellatedMeshControls_h>`_
     - To switch on creation of the castellated mesh
   * - `snapControls <#snapControls_h>`_
     - To switch on surface snapping stage
   * - `addLayersControls <#addLayersControls_h>`_
     - To switch on surface layer insertion.
   * - `meshQualityControls <#meshQualityControls_h>`_
     - Controls for mesh quality.
   * - `geometry <#geometry_h>`_
     - Define all surface geometry used.

.. raw:: html

    <hr style="border: 1px dashed;">
    <h5 id="modules_h">modules</h5>


The modules section is responsible for the general properties of the SnappyHexMesh node.

.. list-table::
   :widths: 25 20 250
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

*Example*

.. code-block:: javascript

    "modules": {
        "castellatedMesh": true,
        "snap": true,
        "layers": true,
        "mergeTolerance": 1e-6
    }

`up <#type_h>`_

.. raw:: html

    <hr style="border: 1px dashed;">
    <h5 id="castellatedMeshControls_h">castellatedMeshControls</h5>


The castellatedMeshControls define the properties to switch on creation of the castellated mesh

.. list-table::
   :widths: 25 25 250
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

*Example*

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

`up <#type_h>`_

.. raw:: html

    <hr style="border: 1px dashed;">
    <h5 id="snapControls_h">snapControls</h5>


.. list-table::
   :widths: 25 20 250
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

*Example*

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

`up <#type_h>`_

.. raw:: html

    <hr style="border: 1px dashed;">
    <h5 id="addLayersControls_h">addLayersControls</h5>


.. list-table::
   :widths: 25 20 250
   :header-rows: 1
   :align: left

   * - Sub-Parameter
     - Data Type
     - Description
   * - relativeSizes
     - boolean
     -  switch that sets whether the specified layer thicknesses are relative to undistorted cell size outside layer or absolute
   * - expansionRatio
     - number
     - expansion factor for layer mesh, increase in size from one layer to the next.
   * - finalLayerThickness
     - number
     - thickness of layer nearest the wall, usually in combination with absolute sizes according to the relativeSizes entry.
   * - minThickness
     - number
     - minimum thickness of cell layer, either relative or absolute (as above).
   * - featureAngle
     - number
     - angle above which surface is not extruded.
   * - slipFeatureAngle
     - number
     - controls how the mesh resolves sharp features in the geometry, particularly when "slip" features are involved.
   * - nLayerIter
     - number
     - overall max number of layer addition iterations (typically 50).
   * - nRelaxedIter
     - number
     - max number of iterations after which the controls in the relaxed sub dictionary of meshQuality are used (typically 20).
   * - nRelaxIter
     - number
     - maximum number of snapping relaxation iterations (typcially 5).
   * - nGrow
     - number
     - number of layers of connected faces that are not grown if points do not get extruded; helps convergence of layer addition close to features.
   * - nSmoothSurfaceNormals
     - number
     - number of smoothing iterations of surface normals (typically 1).
   * - nSmoothNormals
     - number
     - number of smoothing iterations of interior mesh movement direction (typically 3).
   * - nSmoothThickness
     - number
     - smooth layer thickness over surface patches (typically 10).
   * - maxFaceThicknessRatio
     - number
     - stop layer growth on highly warped cells (typically 0.5).
   * - maxThicknessToMedialRatio
     - number
     - reduce layer growth where ratio thickness to medial distance is large (typically 0.3)
   * - minMedianAxisAngle
     - number
     - angle used to pick up medial axis points (typically 90).
   * - nMedialAxisIter
     - number
     - Controls the number of iterations for medial axis refinement during the snapping process.
   * - nBufferCellsNoExtrude
     - number
     - create buffer region for new layer terminations (typically 0).
   * - additionalReporting
     - boolean
     - Enables extra output during the meshing process for debugging or analysis.


*Example*

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

`up <#type_h>`_

.. raw:: html

    <hr style="border: 1px dashed;">
    <h5 id="meshQualityControls_h">meshQualityControls</h5>

.. list-table::
   :widths: 25 20 250
   :header-rows: 1
   :align: left

   * - Sub-Parameter
     - Data Type
     - Description
   * - maxBoundarySkewness
     - number
     - max boundary face skewness allowed (typically 20).
   * - maxInternalSkewness
     - number
     - max internal face skewness allowed (typically 4).
   * - maxConcave
     - number
     - max concaveness allowed (typically 80).
   * - minVol
     - number
     - minimum cell pyramid volume (typically 1e-13, large negative number disables).
   * - minTetQuality
     - number
     - minimum quality of tetrahedral cells from cell decomposition; generally deactivated by setting large negative number since v5.0 when new barycentric tracking was introduced, which could handle negative tets.
   * - minArea
     - number
     - minimum face area (typically -1).
   * - minTwist
     - number
     - minimum face twist (typically 0.05).
   * - minDeterminant
     - number
     - minimum normalised cell determinant; 1 = \relax \special {t4ht= hex; ≤ \relax \special {t4ht= 0 = illegal cell (typically 0.001).
   * - minFaceWeight
     - number
     - between 0-0.5 (typically 0.05).
   * - minVolRatio
     - number
     - dbetween 0-1.0 (typically 0.01).
   * - minTriangleTwist
     - number
     - 0 for Fluent compatibility (typically -1).
   * - nSmoothScale
     - number
     - number of error distribution iterations (typically 4).
   * - errorReduction
     - number
     - amount to scale back displacement at error points (typically 0.75).
   * - relaxed
     - structure
     - sub-dictionary that can include modified values for the above keyword entries to be used when nRelaxedIter is exceeded in the layer addition process.
   * - maxNonOrtho
     - number
     - Specifies the maximum acceptable non-orthogonality of mesh cells during the meshing process.

*Example*

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

`up <#type_h>`_

.. raw:: html

    <hr style="border: 1px dashed;">
    <h5 id="geometry_h">geometry</h5>

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

*Example*

.. code-block:: javascript

    "geometry": {
       "objects": {
           "building": {
               "objectName": "building",
               "objectType": "obj",
               "levels": "1",
               "refinementRegions": {},
               "refinementSurfaces": {
                  "levels": [ 0, 0 ],
                  "patchType": "wall"
               },
               "regions": {
                  "Walls": {
                     "name": "Walls",
                     "type": "wall",
                     "refinementRegions": {
                        "mode": "distance",
                         "levels": [
                            [ 0.1, 2 ]
                          ]
                     },
                     "refinementSurfaceLevels": [ 0, 0 ]
                  },
                  "inlet": {
                       "name": "inlet",
                       "type": "patch"
                  },
                  "outlet": {
                      "name": "outlet",
                      "type": "patch"
                  }
               },
               "layers": {
                  "nSurfaceLayers": 10
               }
           }
       },
       "gemeotricalEntities": {}
    }

`up <#type_h>`_


.. raw:: html

   <h3 id="Example_h">Example</h3>
   <hr>
   <h4>JSON File  (input) </h4>


.. literalinclude:: snappyHexMesh_example.json
   :language: JSON
   :linenos:

.. raw:: html

    <hr style="border: 1px dashed;">
    <h4>OpenFOAM dictionary (output)</h4>

.. literalinclude:: snappyHexMeshDict
   :language: none
   :linenos:

`up <#type_h>`_

.. raw:: html

   <hr>

