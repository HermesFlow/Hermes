General Nodes
==============

The general nodes in Hermes are responsible for:

    * creating files or directories
    * copying or moving files or directories
    * executing OS command or python script
    * writing the output of a node to a file.

The types of generals nodes are:

.. code-block:: javascript

     "general.RunOsCommand"
     "general.CopyFile"
     "general.Parameters"
     "general.RunPythonCode"

|

.. toctree::
   :maxdepth: 2
   :caption: Examples of General Nodes

   parameters.rst
   createEmptyCase.rst
   copyObjectToCase.rst
   copyBuildingObject.rst
   fileWriter/fileWriter.rst