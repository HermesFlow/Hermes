__version__=(0,0,1) 

"""
	Version 0.0.1
	-------------

	* Finished most of the design. 
    * Executers are not implemented.
           

"""


from hermes.pipline.workflow import hermesWorkflow
from .taskwrapper import hermesTaskWrapper
from .Resources.nodeTemplates.templateCenter import templateCenter
from .pipline.expandPipeline import expandPipeline
from .Resources.executers.executerHome import executerHome