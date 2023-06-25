.. Hermes documentation master file, created by
   sphinx-quickstart on Thu Dec  5 12:11:55 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Hermes's documentation!
==================================

Hermes is a package that aims to simplify the batch operation of programs. Different than
other packages (..), the workflow is specified in JSON format, which allows queries and comparison of different workflows
using MongoDB.

The workflow is defined as a series of nodes, and the input to one node can be defined as the output of
another node. The hermes engine builds a python workflow using the luigi package which allows the
concomitant execution of all the node withc respect to their depencies.

An additional workbench was programmed using the opensource CAD program FreeCAD, so simplify the definition of
boundary conditions and complex objects in the simulation.


.. include:: About/Tutrial10Min.rst


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   FreeCAD/FreeCAD.rst
   simpleWorkflow/intro.rst
   Json/JsonStructure.rst
   CLI/CLI.rst


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
