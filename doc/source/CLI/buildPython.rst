Built a Python File
===================

This page demonstrates how to make a python file using a pipeline json file.

Suppose we have an expanded pipeline, such as the one introduced in the former page.
We can build the python file using the hermes-Pipeline command line.

.. code-block:: python

    hermes-Pipeline buildPython "/home/ofir/Downloads/Hermes/Hermes_git/examples/simpleFOAM/simpleFOAMexpanded.json"
                           "/home/ofir/Downloads/Hermes/Hermes_git/examples/simpleFOAM/simpleFOAM.py"

The default working directory is the directory of the python file.
If one desires to choose another one, one can add it is a third argument:

.. code-block:: python

    hermes-Pipeline buildPython "/home/ofir/Downloads/Hermes/Hermes_git/examples/simpleFOAM/simpleFOAMexpanded.json"
                           "/home/ofir/Downloads/Hermes/Hermes_git/examples/simpleFOAM/simpleFOAM.py"
                           "/AnotherWorkingDirectory"

The default builder is luigi.
If one desires to choose another one, one can add it is a fourth argument:

.. code-block:: python

    hermes-Pipeline buildPython "/home/ofir/Downloads/Hermes/Hermes_git/examples/simpleFOAM/simpleFOAMexpanded.json"
                           "/home/ofir/Downloads/Hermes/Hermes_git/examples/simpleFOAM/simpleFOAM.py"
                           "/AnotherWorkingDirectory"
                           "AnotherBuilder"