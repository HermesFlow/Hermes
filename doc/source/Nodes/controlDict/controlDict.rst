ControlDict Node
=================

ControlDict is the node manages the settings for the simulation's execution. It defines key parameters such as the start and end times of the simulation, time-step size, solver write intervals, and output control settings (e.g., precision and format of results). Additionally, it specifies whether the simulation runs in steady or transient mode and allows control of optional features like function objects for data sampling and monitoring. Essentially, it serves as the central script for controlling the simulation's runtime behavior.

.. table:: Table of content
   :align: left

   ================= ============================ =======================
   `Type <#type_h>`_  `Execution <#Execution_h>`_ `Example <#Example_h>`_
   ================= ============================ =======================

.. raw:: html

   <h3 id="type_h">Type</h3>
   <hr>

.. code-block:: javascript

    "type" : "openFOAM.system.ControlDict"


.. raw:: html

   <h3 id="Execution_h">Execution</h3>
   <hr>

**input_parameters**

.. list-table::
   :widths: 25 20 250
   :header-rows: 1
   :align: left

   * - Parameter
     - Data Type
     - Description
   * - application
     - string
     - The type of the simulation
   * - startFrom
     - string
     - Controls the start time of the simulation. [firstTime | startTime | latestTime]
   * - startTime
     - number
     - Start time for the simulation. works with startFrom - startTime
   * - stopAt
     - string
     - Controls the end time of the simulation. [endTime | writeNow | noWriteNow]
   * - endTime
     - number
     - End time for the simulation when stopAt 'endTime' is specified.
   * - deltaT
     - number
     - Time step of the simulation.
   * - writeControl
     - string
     - Controls the timing of write output to file. [timeStep | runTime | adjustableRunTime | cpuTime | clockTime]
   * - writeInterval
     - number
     - Scalar used in conjunction with writeControl described above.
   * - runTimeModifiable
     - boolean
     - Switch for whether dictionaries, e.g.controlDict, are re-read during a simulation at the beginning of each time step, allowing the user to modify parameters during a simulation.
   * - interpolate
     - boolean
     - Define whether field data is interpolated from cell centers to face centers during post-processing or function object operations.
   * - adjustTimeStep
     - boolean
     - Switch used by some solvers to adjust the time step during the simulation, usually according to maxCo.
   * - purgeWrite
     - number
     - Integer representing a limit on the number of time directories that are stored by overwriting time directories on a cyclic basis
   * - writeFormat
     - string
     - Specifies the format of the data files [ascii | binary]
   * - writePrecision
     - number
     - Integer used in conjunction with writeFormat described above, 6 by default.
   * - writeCompression
     - boolean
     - Switch to specify whether files are compressed with gzip when written
   * - timeFormat
     - string
     - Choice of format of the naming of the time directories [fixed | scientific | general(default) ]
   * - timePrecision
     - number
     - Integer used in conjunction with timeFormat described above, 6 by default.
   * - maxCo
     - number
     - Maximum Courant number, e.g. 0.5
   * - functions
     - string
     - Dictionary of functions, e.g. probes to be loaded at run-time
   * - libs
     - string
     - List of additional libraries to be loaded at run-time, e.g.("libNew1.so" "libNew2.so")

.. code-block:: javascript

    "input_parameters": {
        "values": {
              "application": "simpleFoam",
              "startFrom": "startTime",
              "startTime": 0,
              "stopAt": "endTime",
              "endTime": 60,
              "deltaT": 1,
              "writeControl": "adjustableRunTime",
              "writeInterval": 0.1,
              "runTimeModifiable": true,
              "interpolate": true,
              "adjustTimeStep": true,
              "purgeWrite": 0,
              "writeFormat": "ascii",
              "writePrecision": 7,
              "writeCompression": false,
              "timeFormat": "general",
              "timePrecision": 6,
              "maxCo": 0.5,
              "functions": [],
              "libs": []
            }
    }

`up <#type_h>`_

.. raw:: html

   <h3 id="Example_h">Example</h3>
   <hr>
   <h4>JSON File  (input) </h4>


.. literalinclude:: controlDict_example.json
   :language: JSON
   :linenos:

.. raw:: html

    <hr style="border: 1px dashed;">
    <h4>OpenFOAM dictionary (output)</h4>

.. literalinclude:: controlDict
   :language: OpenFOAM dictionary
   :linenos:

`up <#type_h>`_

.. raw:: html

   <hr>
