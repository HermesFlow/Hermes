

import shutil
import os
import luigi
import json 
import sys

sys.path.insert(1, "/home/noga/Noga/FreeCad/github/Hermes/master/Hermes")
from hermes.engines.luigi.taskUtils import utils as hermesutils

class CopyDirectory_0(luigi.Task,hermesutils):

    _taskJSON = None
    _workflowJSON = None 
    
    @property 
    def workflowJSON(self):
        return self._workflowJSON
        
    @property 
    def taskJSON(self):
        return self._taskJSON
    
    def __init__(self,*args,**kwargs): 
        super().__init__(*args,**kwargs)
        self._taskJSON ={}
        
        self._workflowJSON = {'workflow': {'root': None, 'Templates': {}, 'nodeList': ['CopyDirectory', 'RunOsCommand'], 'nodes': {'CopyDirectory': {'Execution': {'typeExecution': 'copyDirectory', 'input_parameters': {'Source': '{Properties.Source.current_val}', 'Target': '{Properties.Target.current_val}'}}, 'GUI': {'TypeFC': 'WebGuiNode', 'Properties': {'Source': {'prop': 'Source', 'init_val': '', 'type': 'App::PropertyPath', 'Heading': 'Parameters', 'tooltip': 'The source directory', 'current_val': ''}, 'Target': {'prop': 'Target', 'init_val': '', 'type': 'App::PropertyPath', 'Heading': 'Parameters', 'tooltip': 'The target directory', 'current_val': ''}}, 'WebGui': {}}}, 'RunOsCommand': {'Execution': {'typeExecution': 'RunOsCommand', 'input_parameters': {'Method': '{Properties.ChooseMethod.current_val}', 'Commands': '{Properties.Commands.current_val}', 'batchFile': '{Properties.batchFile.current_val}', 'OS': 'blockmesh -c {CopyDirectory.output.directory}'}}, 'GUI': {'TypeFC': 'WebGuiNode', 'Properties': {'ChooseMethod': {'prop': 'ChooseMethod', 'init_val': ['Commands list', 'batchFile'], 'type': 'App::PropertyEnumeration', 'Heading': 'Parameters', 'tooltip': 'True-commands, False-file', 'current_val': 'Commands list'}, 'Commands': {'prop': 'Commands', 'init_val': [], 'type': 'App::PropertyStringList', 'Heading': 'Parameters', 'tooltip': 'The OS commands to execute', 'current_val': ["echo 'Here is an example of a shell script'", "echo '1a. File listing'", 'ls', "echo ''"]}, 'batchFile': {'prop': 'batchFile', 'init_val': 'Text', 'type': 'App::PropertyFile', 'Heading': 'Parameters', 'tooltip': 'File containing all the OS commands to execute', 'current_val': ''}}, 'WebGui': {}}}, 'finalnode_xx': {'name': 'finalnode_xx', 'Execution': {'typeExecution': 'generalExecuter.parameterExecuter', 'input_parameters': {}}, 'requires': ['CopyDirectory', 'RunOsCommand'], 'GUI': {'TypeFC': {}, 'Properties': {}, 'WebGui': {}}}}}}['workflow']

    def output(self):
        return luigi.LocalTarget("outputsOriginal/CopyDirectory_0.json")

    def requires(self):
        return dict(
                   )

    def run(self):
        target = self.output()
        target.makedirs()
        
        task_executer_mapping = {'Source': '{Properties.Source.current_val}', 'Target': '{Properties.Target.current_val}'}
        
        parameters_from_required = self.get_all_required_outputs()        
        params = dict(parameters_from_required)
        params['formData']   = {}
        params['files']      = {}
        params['Schema']     = {}
        params['uiSchema']   = {}
        params['Properties'] = {'Source': {'prop': 'Source', 'init_val': '', 'type': 'App::PropertyPath', 'Heading': 'Parameters', 'tooltip': 'The source directory', 'current_val': ''}, 'Target': {'prop': 'Target', 'init_val': '', 'type': 'App::PropertyPath', 'Heading': 'Parameters', 'tooltip': 'The target directory', 'current_val': ''}}
        params['WebGui']     = {}

        
        executer_parameters = self.build_executer_parameters(task_executer_mapping, params)
        executer_parameters['WD_path']='/home/noga/Noga/FreeCad/github/Hermes/master/Hermes/examples/RunNCopy'
                    
        from hermes.Resources.executers import copyDirectory  
        output =  copyDirectory(self._taskJSON).run(**executer_parameters)
        
        params['input_parameters'] = executer_parameters 
        params['output'] = output        
        
        out_params = params
        with open(self.output().fn,"w") as outfile:
            json.dump(out_params,outfile)

class RunOsCommand_0(luigi.Task,hermesutils):

    _taskJSON = None
    _workflowJSON = None 
    
    @property 
    def workflowJSON(self):
        return self._workflowJSON
        
    @property 
    def taskJSON(self):
        return self._taskJSON
    
    def __init__(self,*args,**kwargs): 
        super().__init__(*args,**kwargs)
        self._taskJSON ={}
        
        self._workflowJSON = {'workflow': {'root': None, 'Templates': {}, 'nodeList': ['CopyDirectory', 'RunOsCommand'], 'nodes': {'CopyDirectory': {'Execution': {'typeExecution': 'copyDirectory', 'input_parameters': {'Source': '{Properties.Source.current_val}', 'Target': '{Properties.Target.current_val}'}}, 'GUI': {'TypeFC': 'WebGuiNode', 'Properties': {'Source': {'prop': 'Source', 'init_val': '', 'type': 'App::PropertyPath', 'Heading': 'Parameters', 'tooltip': 'The source directory', 'current_val': ''}, 'Target': {'prop': 'Target', 'init_val': '', 'type': 'App::PropertyPath', 'Heading': 'Parameters', 'tooltip': 'The target directory', 'current_val': ''}}, 'WebGui': {}}}, 'RunOsCommand': {'Execution': {'typeExecution': 'RunOsCommand', 'input_parameters': {'Method': '{Properties.ChooseMethod.current_val}', 'Commands': '{Properties.Commands.current_val}', 'batchFile': '{Properties.batchFile.current_val}', 'OS': 'blockmesh -c {CopyDirectory.output.directory}'}}, 'GUI': {'TypeFC': 'WebGuiNode', 'Properties': {'ChooseMethod': {'prop': 'ChooseMethod', 'init_val': ['Commands list', 'batchFile'], 'type': 'App::PropertyEnumeration', 'Heading': 'Parameters', 'tooltip': 'True-commands, False-file', 'current_val': 'Commands list'}, 'Commands': {'prop': 'Commands', 'init_val': [], 'type': 'App::PropertyStringList', 'Heading': 'Parameters', 'tooltip': 'The OS commands to execute', 'current_val': ["echo 'Here is an example of a shell script'", "echo '1a. File listing'", 'ls', "echo ''"]}, 'batchFile': {'prop': 'batchFile', 'init_val': 'Text', 'type': 'App::PropertyFile', 'Heading': 'Parameters', 'tooltip': 'File containing all the OS commands to execute', 'current_val': ''}}, 'WebGui': {}}}, 'finalnode_xx': {'name': 'finalnode_xx', 'Execution': {'typeExecution': 'generalExecuter.parameterExecuter', 'input_parameters': {}}, 'requires': ['CopyDirectory', 'RunOsCommand'], 'GUI': {'TypeFC': {}, 'Properties': {}, 'WebGui': {}}}}}}['workflow']

    def output(self):
        return luigi.LocalTarget("outputsOriginal/RunOsCommand_0.json")

    def requires(self):
        return dict(
                       CopyDirectory=CopyDirectory_0()
                   )

    def run(self):
        target = self.output()
        target.makedirs()
        
        task_executer_mapping = {'Method': '{Properties.ChooseMethod.current_val}', 'Commands': '{Properties.Commands.current_val}', 'batchFile': '{Properties.batchFile.current_val}', 'OS': 'blockmesh -c {CopyDirectory.output.directory}'}
        
        parameters_from_required = self.get_all_required_outputs()        
        params = dict(parameters_from_required)
        params['formData']   = {}
        params['files']      = {}
        params['Schema']     = {}
        params['uiSchema']   = {}
        params['Properties'] = {'ChooseMethod': {'prop': 'ChooseMethod', 'init_val': ['Commands list', 'batchFile'], 'type': 'App::PropertyEnumeration', 'Heading': 'Parameters', 'tooltip': 'True-commands, False-file', 'current_val': 'Commands list'}, 'Commands': {'prop': 'Commands', 'init_val': [], 'type': 'App::PropertyStringList', 'Heading': 'Parameters', 'tooltip': 'The OS commands to execute', 'current_val': ["echo 'Here is an example of a shell script'", "echo '1a. File listing'", 'ls', "echo ''"]}, 'batchFile': {'prop': 'batchFile', 'init_val': 'Text', 'type': 'App::PropertyFile', 'Heading': 'Parameters', 'tooltip': 'File containing all the OS commands to execute', 'current_val': ''}}
        params['WebGui']     = {}

        
        executer_parameters = self.build_executer_parameters(task_executer_mapping, params)
        executer_parameters['WD_path']='/home/noga/Noga/FreeCad/github/Hermes/master/Hermes/examples/RunNCopy'
                    
        from hermes.Resources.executers import RunOsCommand  
        output =  RunOsCommand(self._taskJSON).run(**executer_parameters)
        
        params['input_parameters'] = executer_parameters 
        params['output'] = output        
        
        out_params = params
        with open(self.output().fn,"w") as outfile:
            json.dump(out_params,outfile)

class finalnode_xx_0(luigi.Task,hermesutils):

    _taskJSON = None
    _workflowJSON = None 
    
    @property 
    def workflowJSON(self):
        return self._workflowJSON
        
    @property 
    def taskJSON(self):
        return self._taskJSON
    
    def __init__(self,*args,**kwargs): 
        super().__init__(*args,**kwargs)
        self._taskJSON ={}
        
        self._workflowJSON = {'workflow': {'root': None, 'Templates': {}, 'nodeList': ['CopyDirectory', 'RunOsCommand'], 'nodes': {'CopyDirectory': {'Execution': {'typeExecution': 'copyDirectory', 'input_parameters': {'Source': '{Properties.Source.current_val}', 'Target': '{Properties.Target.current_val}'}}, 'GUI': {'TypeFC': 'WebGuiNode', 'Properties': {'Source': {'prop': 'Source', 'init_val': '', 'type': 'App::PropertyPath', 'Heading': 'Parameters', 'tooltip': 'The source directory', 'current_val': ''}, 'Target': {'prop': 'Target', 'init_val': '', 'type': 'App::PropertyPath', 'Heading': 'Parameters', 'tooltip': 'The target directory', 'current_val': ''}}, 'WebGui': {}}}, 'RunOsCommand': {'Execution': {'typeExecution': 'RunOsCommand', 'input_parameters': {'Method': '{Properties.ChooseMethod.current_val}', 'Commands': '{Properties.Commands.current_val}', 'batchFile': '{Properties.batchFile.current_val}', 'OS': 'blockmesh -c {CopyDirectory.output.directory}'}}, 'GUI': {'TypeFC': 'WebGuiNode', 'Properties': {'ChooseMethod': {'prop': 'ChooseMethod', 'init_val': ['Commands list', 'batchFile'], 'type': 'App::PropertyEnumeration', 'Heading': 'Parameters', 'tooltip': 'True-commands, False-file', 'current_val': 'Commands list'}, 'Commands': {'prop': 'Commands', 'init_val': [], 'type': 'App::PropertyStringList', 'Heading': 'Parameters', 'tooltip': 'The OS commands to execute', 'current_val': ["echo 'Here is an example of a shell script'", "echo '1a. File listing'", 'ls', "echo ''"]}, 'batchFile': {'prop': 'batchFile', 'init_val': 'Text', 'type': 'App::PropertyFile', 'Heading': 'Parameters', 'tooltip': 'File containing all the OS commands to execute', 'current_val': ''}}, 'WebGui': {}}}, 'finalnode_xx': {'name': 'finalnode_xx', 'Execution': {'typeExecution': 'generalExecuter.parameterExecuter', 'input_parameters': {}}, 'requires': ['CopyDirectory', 'RunOsCommand'], 'GUI': {'TypeFC': {}, 'Properties': {}, 'WebGui': {}}}}}}['workflow']

    def output(self):
        return luigi.LocalTarget("outputsOriginal/finalnode_xx_0.json")

    def requires(self):
        return dict(
                       RunOsCommand=RunOsCommand_0(),
                       CopyDirectory=CopyDirectory_0()
                   )

    def run(self):
        target = self.output()
        target.makedirs()
        
        task_executer_mapping = {}
        
        parameters_from_required = self.get_all_required_outputs()        
        params = dict(parameters_from_required)
        params['formData']   = {}
        params['files']      = {}
        params['Schema']     = {}
        params['uiSchema']   = {}
        params['Properties'] = {}
        params['WebGui']     = {}

        
        executer_parameters = self.build_executer_parameters(task_executer_mapping, params)
        executer_parameters['WD_path']='/home/noga/Noga/FreeCad/github/Hermes/master/Hermes/examples/RunNCopy'
                    
        from hermes.Resources.executers.generalExecuter import parameterExecuter  
        output =  parameterExecuter(self._taskJSON).run(**executer_parameters)
        
        params['input_parameters'] = executer_parameters 
        params['output'] = output        
        
        out_params = params
        with open(self.output().fn,"w") as outfile:
            json.dump(out_params,outfile)
