Run a Python Pipeline File
==========================

This page demonstrates how to run a python file that executes a pipeline.

Run With Luigi
--------------

Suppose we have a python pipeline, such as the one introduced in the former page.
This file was built using the luigi builder.
Therefore, it has to be run using the luigi executer.
The run is done like this:

.. code-block:: python

    hermes-Pipeline executeLuigi "/home/ofir/Downloads/Hermes/Hermes_git/examples/simpleFOAM/simpleFOAM"