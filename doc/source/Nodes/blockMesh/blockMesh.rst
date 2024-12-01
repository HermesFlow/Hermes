blockMesh
==========
BlockMesh is used to generate structured hexahedral meshes for computational domains. It specifies the geometry,
topology, and properties of the mesh. blockmesh is ideal for creating straightforward, structured meshes for
simulations where the domain can be broken down into simple geometric blocks.

.. table:: Table of content
   :align: left

   ================= ============================ =======================
   `Type <#type_h>`_  `Execution <#Execution_h>`_ `Example <#Example_h>`_
   ================= ============================ =======================


.. raw:: html

   <h3 id="type_h">Type</h3>
   <hr>

.. code-block:: javascript

    "type" : "openFOAM.mesh.BlockMesh"


.. raw:: html

   <h3 id="Execution_h">Execution</h3>
   <hr>
   <h4 id="input_parameters_h">input_parameters</h4>

The main parameters for the blockmesh node.

.. list-table::
   :widths: 25 50
   :header-rows: 1
   :align: left

   * - Parameter
     - Description
   * - `geometry <#geo_header>`_
     - Define the geometry properties
   * - `boundary  <#boundary_header>`_
     - A list of the Boundary conditions
   * - `vertices  <#vertices_header>`_
     - A list of coordinates of 8 vertices [ x, y, z]
   * - `blocks  <#blocks_header>`_
     - Define the general block properties



.. raw:: html

    <hr style="border: 1px dashed;">
    <h5 id="geo_header">geometry</h5>


The geometry section is responsible for the general properties of the blockmesh geometry. The geometry parameters may
remain empty, and the default values will be used.

.. list-table::
   :widths: 25 50
   :header-rows: 1
   :align: left

   * - Sub-Parameter
     - Description
   * - convertToMeters(scale*)
     - Scaling factor for the vertex coordinates, e.g. 0.001 scales to mm.
   * - cellCount
     - A vector [x,y,z], define the numbers of cells in each direction.
   * - grading
     - A vector [x,y,z], define the cell expansion ratios.


.. code-block:: javascript

    "geometry": {
        "convertToMeters": "0.01",
        "cellCount": [200, 100, 30],
        "grading": [1, 1, 1]
    }

`up <#type_h>`_

.. raw:: html

    <hr style="border: 1px dashed;">
    <h5 id="boundary_header">boundary</h5>

The boundary section contains a list of the boandries of the blockMesh. Each boundary will have 3 parameters: name,
type and a list of faces.

.. list-table::
   :widths: 25 50
   :header-rows: 1
   :align: left

   * - Sub-Parameter
     - Description
   * - name
     - The name of the boundary
   * - type
     - The type of the Boundary: patch | wall | other(?)
   * - faces
     - A list of faces, each face is defined by 4 vertices (from the 8 vertices of the blockMesh hexahedral)


.. code-block:: javascript

    "boundary": [
       {
          "name": "domain_east",
          "type": "patch",
          "faces": [ [3, 7, 6, 2] ]
       },
       {
          "name": "domain_west",
          "type": "patch",
          "faces": [ [1, 5, 4, 8] ]
       },
       ...
    ]

`up <#type_h>`_

.. raw:: html

    <hr style="border: 1px dashed;">
    <h5 id="vertices_header">vertices</h5>


The vertices section contains a list of 8 vertices of the blockMesh hexahedral. Each vertex coordinate is defined by
[x, y, z].


.. code-block:: javascript

    "vertices": [
       [ -0.5025, -0.5025, -0.001 ],
       [  0.5025, -0.5025, -0.001 ],
       [  0.5025,  0.5025, -0.001 ],
       [ -0.5025,  0.5025, -0.001 ],
       [ -0.5025, -0.5025,  0.15  ],
       [  0.5025, -0.5025,  0.15  ],
       [  0.5025,  0.5025,  0.15  ],
       [ -0.5025,  0.5025   0.15  ]
    ]

`up <#type_h>`_

.. raw:: html

    <hr style="border: 1px dashed;">
    <h5 id="blocks_header">blocks</h5>


The blocks section is responsible for the general properties of the block geometry. The geometry parameters may remain
empty, and the default values will be used.

.. list-table::
   :widths: 25 50
   :header-rows: 1
   :align: left

   * - Sub-Parameter
     - Description
   * - hex
     - define the vertex numbers
   * - cellCount
     - A vector [x,y,z], define the numbers of cells in each direction.
   * - grading
     - A vector [x,y,z], define the cell expansion ratios.


.. code-block:: javascript

    "blocks": {
        "hex": [0, 1, 2, 3, 4, 5, 6, 7],
        "cellCount": [200, 100, 30],
        "grading": [1, 1, 1]
    }

`up <#type_h>`_

.. raw:: html

   <h3 id="Example_h">Example</h3>
   <hr>
   <h4>JSON File  (input) </h4>


.. literalinclude:: blockMesh_example.json
   :language: JSON
   :linenos:

.. raw:: html

    <hr style="border: 1px dashed;">
    <h4>OpenFOAM dictionary (output)</h4>

.. literalinclude:: blockMeshDict
   :language: OpenFOAM dictionary
   :linenos:

`up <#type_h>`_

.. raw:: html

   <hr>