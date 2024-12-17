Hermes Nodes
============

The openFOAM nodes in Hermes are mainly responsible for creating text files from templates. The templates are adjust
to the openFOAM input dictionaries structures.

In Addition there is an buildAllRun which responsible for

The types of openFOAM nodes are:

.. code-block:: javascript

     "openFOAM.BuildAllrun"
     "openFOAM.mesh.BlockMesh"
     "openFOAM.mesh.SnappyHexMesh"
     "openFOAM.system.ControlDict"
     "openFOAM.system.FvSchemes"
     "openFOAM.system.FvSolution"
     "openFOAM.constant.physicalProperties"
     "openFOAM.constant.momentumTransport"
     "openFOAM.system.ChangeDictionary"

|

.. toctree::
   :maxdepth: 2
   :caption: The Open FOAM Nodes

   buildAllRun/buildAllRun.rst
   blockMesh/blockMesh.rst
   snappyHexMesh/snappyHexMesh.rst
   controlDict/controlDict.rst
   fvSchemes/fvSchemes.rst
   fvSolution/fvSolution.rst
   physicalProperties/physicalProperties.rst
   momentumTransport/momentumTransport.rst
   bc/defineNewBoundaryConditions.rst