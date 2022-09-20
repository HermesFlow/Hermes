__version__=(3,0,0)

"""
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
from .Resources.nodeTemplates.templateCenter import templateCenter
from .workflow.expandWorkflow import expandWorkflow
from .Resources.executers.executerHome import executerHome
import os
import json

import logging.config

with open(os.path.join(os.path.dirname(__file__), 'hermesLogging', 'hermesLogging.config'), 'r') as logconfile:
     log_conf_str = logconfile.read().replace("\n","")
     log_conf = json.loads(log_conf_str.replace("{hermespath}",os.path.dirname(__file__)))

EXECUTION = 15
logging.addLevelName(EXECUTION, 'EXECUTION')


def execution(self, message, *args, **kws):
    self.log(EXECUTION, message, *args, **kws)

logging.Logger.execution = execution

# logging.config.dictConfig(log_conf)

