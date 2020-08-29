__version__=(1,0,0)

"""
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


from .pipeline.workflow import hermesWorkflow
from .taskwrapper import hermesTaskWrapper
from .Resources.nodeTemplates.templateCenter import templateCenter
from .pipeline.expandWorkflow import expandWorkflow
from .Resources.executers.executerHome import executerHome