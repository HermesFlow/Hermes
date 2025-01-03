__version__=(3,4,0)

# Have some initial default logging configuration in case the user hasn't set any
from .utils.logging.helpers import initialize_logging
initialize_logging(disable_existing_loggers=False)


"""
  Version 3.4.0
  -------------
  #118: system command execution - Fixed the code to return the original value, even if the execution of the command fails. 
  Version 3.3.1
  -------------
    - Adding the scalarTransport example. 
    - Fixing bugs in handling the #{ for the coded boundary and parameters. 
    - Jinja: Added function to concat values given as a list. 

  Version 3.3.0
  -------------
    - Adding support for varibles and #calc. 
    - Added a stripped output version in writing. 
    - Updating blockMesh and the snappy jijna
    - Updating the injectors jijna
    - Updating to OF10 by adding the momentum and Physicla properties files.
    - fixing the dependency bugs in the pipeline.

  Version 3.2.0
  -------------

    - Added 'write' capability to the hermes workflow
    - Removed  hera-metadata
    - The empty parameter string '{}' in a parameter path is interpreted as {}.
      This is important for the shell scripts. 
    - Fixed the all run execution.  
    - Added an optional name attribute to the workflow         

  Version 3.1.0
  -------------

    - Adding the build RunAll nodes. 

    - Adding the workflow type to the workflow (#85). 

  Version 3.0.0
  -------------
     
     - Major refactor fo the internal structure of the nodes. 
     
  
  Version 2.0.0
  --------------

    - hermes workflow: Solving the problem of weak-ref in the mongoDB object
    - Adding the special handler {#<token>} in the parsing of the configuration file. 
      The current implementations is: 
            - moduleName that return the name of the current luigi module (i.e workflow name).   
    - Fixed the areference to the old simpleFOAM for the snappy objects. 
    - Updating the workflow object to provede services needed in the 
      running.
    - extended the wrapper to the workflow 
    - Added the jijnaTemplate node. 
    - Changes the target file directory execution to the name of the class. 
    - Changes to the controldict and snappyhexmesh templates.
    - Added location of execution to the tot he run os command node.  

	Version 1.2.0
	-------------
	
	- Restructturing the fvSolution and the fvSchemes inputs 
	- Updating the transport properties and ect. 


	Version 1.1.0
	-------------
	
	- Restructturing the blockMesh and snappyHexMesh. 
	- Extension to the processing of paths (allow lists and dicts). 
	 
    

	Version 1.0.0
	-------------
    
    * Fixed new structure of the nodes. 
            - Execution 
                    - type : the execution type of the node.  
            - GUI 
                    - type : the GUI node type
                    
    * Changed the directory copying and ect to be <class names>Executer 
    * Added the right output to the directory. 
    * Fixed the RunNCopy example. 

	Version 0.0.1
	-------------

	* Finished most of the design. 
    * Executers are not implemented.
           

"""
from .workflow.workflow import workflow
from .taskwrapper import hermesTaskWrapper
from .workflow.expandWorkflow import expandWorkflow
from .Resources.executers.executerHome import executerHome
import os
import json

import logging.config

with open(os.path.join(os.path.dirname(__file__), 'hermesLogging', 'hermesLogging.config'), 'r') as logconfile:
     log_conf_str = logconfile.read().replace("\n","")
     log_conf = json.loads(log_conf_str.replace("{hermespath}",os.path.dirname(__file__)))


