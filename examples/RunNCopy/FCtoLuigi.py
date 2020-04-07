

import shutil
import os
import luigi
import json 
import sys

sys.path.insert(1, "/home/noga/Noga/FreeCad/github/Hermes/master/Hermes")
from hermes.engines.luigi.taskUtils import utils as hermesutils

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
        
        self._workflowJSON = {'workflow': {'root': None, 'Templates': {'importJsonfromfile': {'path': '../../hermes/Resources/nodeTemplates/templates.json'}}, 'nodeList': ['CopyDirectory', 'RunOsCommand'], 'nodes': {'CopyDirectory': {'typeExecution': 'copyDirectory', 'TypeFC': 'WebGuiNode', 'input_parameters': {'Source': '{Properties.Source.current_val}', 'Target': '{Properties.Target.current_val}'}, 'Properties': {'Source': {'prop': 'Source', 'init_val': '', 'type': 'App::PropertyPath', 'Heading': 'Parameters', 'tooltip': 'The source directory', 'current_val': '/home/noga/Noga/FreeCad/github/Hermes/master/Hermes/examples/RunNCopy/source/dir1'}, 'Target': {'prop': 'Target', 'init_val': '', 'type': 'App::PropertyPath', 'Heading': 'Parameters', 'tooltip': 'The target directory', 'current_val': '/home/noga/Noga/FreeCad/github/Hermes/master/Hermes/examples/RunNCopy/target/dir2'}}, 'WebGui': {}}, 'RunOsCommand': {'typeExecution': 'RunOsCommand', 'TypeFC': 'WebGuiNode', 'input_parameters': {'Method': '{Properties.ChooseMethod.current_val}', 'Commands': '{Properties.Commands.current_val}', 'batchFile': '{Properties.batchFile.current_val}'}, 'Properties': {'ChooseMethod': {'prop': 'ChooseMethod', 'init_val': ['Commands list', 'batchFile'], 'type': 'App::PropertyEnumeration', 'Heading': 'Parameters', 'tooltip': 'True-commands, False-file', 'current_val': 'Commands list'}, 'Commands': {'prop': 'Commands', 'init_val': [], 'type': 'App::PropertyStringList', 'Heading': 'Parameters', 'tooltip': 'The OS commands to execute', 'current_val': ["echo 'Here is an example of a shell script'", "echo '1a. File listing'", 'ls', "echo ''"]}, 'batchFile': {'prop': 'batchFile', 'init_val': 'Text', 'type': 'App::PropertyFile', 'Heading': 'Parameters', 'tooltip': 'File containing all the OS commands to execute', 'current_val': ''}}, 'WebGui': {}}, 'finalnode_xx': {'name': 'finalnode_xx', 'typeExecution': 'parameters', 'requires': ['CopyDirectory', 'RunOsCommand'], 'input_parameters': {}}}}}['workflow']

    def output(self):
        return luigi.LocalTarget("outputs/RunOsCommand_0.json")

    def requires(self):
        return dict(
                   )

    def run(self):
        target = self.output()
        target.makedirs()
        
        task_executer_mapping = {'Method': '{Properties.ChooseMethod.current_val}', 'Commands': '{Properties.Commands.current_val}', 'batchFile': '{Properties.batchFile.current_val}'}
        
        parameters_from_required = self.get_all_required_outputs()        
        params = dict(parameters_from_required)
        params['parameters'] = {}
        params['WebGUI']     = {}
        params['Properties'] = {'ChooseMethod': {'prop': 'ChooseMethod', 'init_val': ['Commands list', 'batchFile'], 'type': 'App::PropertyEnumeration', 'Heading': 'Parameters', 'tooltip': 'True-commands, False-file', 'current_val': 'Commands list'}, 'Commands': {'prop': 'Commands', 'init_val': [], 'type': 'App::PropertyStringList', 'Heading': 'Parameters', 'tooltip': 'The OS commands to execute', 'current_val': ["echo 'Here is an example of a shell script'", "echo '1a. File listing'", 'ls', "echo ''"]}, 'batchFile': {'prop': 'batchFile', 'init_val': 'Text', 'type': 'App::PropertyFile', 'Heading': 'Parameters', 'tooltip': 'File containing all the OS commands to execute', 'current_val': ''}}
        params['WebGui']     = {}
        
        executer_parameters = self.build_executer_parameters(task_executer_mapping, params)
        executer_parameters['WD_path']='/home/noga/Noga/FreeCad/github/Hermes/master/Hermes/examples/RunNCopy'
                    
        from hermes.Resources.executers.fileSystemExecuter import RunOsCommand  
        output =  RunOsCommand(self._taskJSON).run(**executer_parameters)
        
        params['input_parameters'] = executer_parameters 
        params['output'] = output        
        
        out_params = params
        with open(self.output().fn,"w") as outfile:
            json.dump(out_params,outfile)

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
        
        self._workflowJSON = {'workflow': {'root': None, 'Templates': {'importJsonfromfile': {'path': '../../hermes/Resources/nodeTemplates/templates.json'}}, 'nodeList': ['CopyDirectory', 'RunOsCommand'], 'nodes': {'CopyDirectory': {'typeExecution': 'copyDirectory', 'TypeFC': 'WebGuiNode', 'input_parameters': {'Source': '{Properties.Source.current_val}', 'Target': '{Properties.Target.current_val}'}, 'Properties': {'Source': {'prop': 'Source', 'init_val': '', 'type': 'App::PropertyPath', 'Heading': 'Parameters', 'tooltip': 'The source directory', 'current_val': '/home/noga/Noga/FreeCad/github/Hermes/master/Hermes/examples/RunNCopy/source/dir1'}, 'Target': {'prop': 'Target', 'init_val': '', 'type': 'App::PropertyPath', 'Heading': 'Parameters', 'tooltip': 'The target directory', 'current_val': '/home/noga/Noga/FreeCad/github/Hermes/master/Hermes/examples/RunNCopy/target/dir2'}}, 'WebGui': {}}, 'RunOsCommand': {'typeExecution': 'RunOsCommand', 'TypeFC': 'WebGuiNode', 'input_parameters': {'Method': '{Properties.ChooseMethod.current_val}', 'Commands': '{Properties.Commands.current_val}', 'batchFile': '{Properties.batchFile.current_val}'}, 'Properties': {'ChooseMethod': {'prop': 'ChooseMethod', 'init_val': ['Commands list', 'batchFile'], 'type': 'App::PropertyEnumeration', 'Heading': 'Parameters', 'tooltip': 'True-commands, False-file', 'current_val': 'Commands list'}, 'Commands': {'prop': 'Commands', 'init_val': [], 'type': 'App::PropertyStringList', 'Heading': 'Parameters', 'tooltip': 'The OS commands to execute', 'current_val': ["echo 'Here is an example of a shell script'", "echo '1a. File listing'", 'ls', "echo ''"]}, 'batchFile': {'prop': 'batchFile', 'init_val': 'Text', 'type': 'App::PropertyFile', 'Heading': 'Parameters', 'tooltip': 'File containing all the OS commands to execute', 'current_val': ''}}, 'WebGui': {}}, 'finalnode_xx': {'name': 'finalnode_xx', 'typeExecution': 'parameters', 'requires': ['CopyDirectory', 'RunOsCommand'], 'input_parameters': {}}}}}['workflow']

    def output(self):
        return luigi.LocalTarget("outputs/CopyDirectory_0.json")

    def requires(self):
        return dict(
                   )

    def run(self):
        target = self.output()
        target.makedirs()
        
        task_executer_mapping = {'Source': '{Properties.Source.current_val}', 'Target': '{Properties.Target.current_val}'}
        
        parameters_from_required = self.get_all_required_outputs()        
        params = dict(parameters_from_required)
        params['parameters'] = {}
        params['WebGUI']     = {}
        params['Properties'] = {'Source': {'prop': 'Source', 'init_val': '', 'type': 'App::PropertyPath', 'Heading': 'Parameters', 'tooltip': 'The source directory', 'current_val': '/home/noga/Noga/FreeCad/github/Hermes/master/Hermes/examples/RunNCopy/source/dir1'}, 'Target': {'prop': 'Target', 'init_val': '', 'type': 'App::PropertyPath', 'Heading': 'Parameters', 'tooltip': 'The target directory', 'current_val': '/home/noga/Noga/FreeCad/github/Hermes/master/Hermes/examples/RunNCopy/target/dir2'}}
        params['WebGui']     = {}
        
        executer_parameters = self.build_executer_parameters(task_executer_mapping, params)
        executer_parameters['WD_path']='/home/noga/Noga/FreeCad/github/Hermes/master/Hermes/examples/RunNCopy'
                    
        from hermes.Resources.executers.fileSystemExecuter import copyDirectory  
        output =  copyDirectory(self._taskJSON).run(**executer_parameters)
        
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
        
        self._workflowJSON = {'workflow': {'root': None, 'Templates': {'importJsonfromfile': {'path': '../../hermes/Resources/nodeTemplates/templates.json'}}, 'nodeList': ['CopyDirectory', 'RunOsCommand'], 'nodes': {'CopyDirectory': {'typeExecution': 'copyDirectory', 'TypeFC': 'WebGuiNode', 'input_parameters': {'Source': '{Properties.Source.current_val}', 'Target': '{Properties.Target.current_val}'}, 'Properties': {'Source': {'prop': 'Source', 'init_val': '', 'type': 'App::PropertyPath', 'Heading': 'Parameters', 'tooltip': 'The source directory', 'current_val': '/home/noga/Noga/FreeCad/github/Hermes/master/Hermes/examples/RunNCopy/source/dir1'}, 'Target': {'prop': 'Target', 'init_val': '', 'type': 'App::PropertyPath', 'Heading': 'Parameters', 'tooltip': 'The target directory', 'current_val': '/home/noga/Noga/FreeCad/github/Hermes/master/Hermes/examples/RunNCopy/target/dir2'}}, 'WebGui': {}}, 'RunOsCommand': {'typeExecution': 'RunOsCommand', 'TypeFC': 'WebGuiNode', 'input_parameters': {'Method': '{Properties.ChooseMethod.current_val}', 'Commands': '{Properties.Commands.current_val}', 'batchFile': '{Properties.batchFile.current_val}'}, 'Properties': {'ChooseMethod': {'prop': 'ChooseMethod', 'init_val': ['Commands list', 'batchFile'], 'type': 'App::PropertyEnumeration', 'Heading': 'Parameters', 'tooltip': 'True-commands, False-file', 'current_val': 'Commands list'}, 'Commands': {'prop': 'Commands', 'init_val': [], 'type': 'App::PropertyStringList', 'Heading': 'Parameters', 'tooltip': 'The OS commands to execute', 'current_val': ["echo 'Here is an example of a shell script'", "echo '1a. File listing'", 'ls', "echo ''"]}, 'batchFile': {'prop': 'batchFile', 'init_val': 'Text', 'type': 'App::PropertyFile', 'Heading': 'Parameters', 'tooltip': 'File containing all the OS commands to execute', 'current_val': ''}}, 'WebGui': {}}, 'finalnode_xx': {'name': 'finalnode_xx', 'typeExecution': 'parameters', 'requires': ['CopyDirectory', 'RunOsCommand'], 'input_parameters': {}}}}}['workflow']

    def output(self):
        return luigi.LocalTarget("outputs/finalnode_xx_0.json")

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
        params['parameters'] = {}
        params['WebGUI']     = {}
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
