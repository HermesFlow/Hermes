

import shutil
import os
import luigi
import json 
import sys

from os.path import expanduser
home = expanduser("~")
dir_path=home+"/Downloads/Check"
sys.path.insert(1, dir_path)

from pyHermes.engines.luigi.taskUtils import utils as hermesutils


class baseParameters_0(luigi.Task,hermesutils):

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
        
        self._workflowJSON = {'workflow': {'root': None, 'nodes': {'baseParameters': {'typeExecution': 'parameters', 'WebGUI': {'formData': {'sourceDir': '/home/blah1'}}, 'parameters': {'basicPath': 'Hello'}, 'input_parameters': {}}, 'node1': {'typeExecution': 'copyDir', 'input_parameters': {'source': '{baseParameters.WebGUI.formData.sourceDir}', 'target': '{WebGUI.formData.target}', 'tester': '{parameters.name}'}, 'parameters': {'name': 'good'}, 'WebGUI': {'formData': {'target': '/home/blah2'}}}, 'node2': {'typeExecution': 'executeScript', 'input_parameters': {'executeDir': '{node1.input_parameters.target}', 'execute': 'runMe {node1.WebGUI.formData.target} {node1.output.copyDir}', 'father': '{node1.baseParameters.parameters.basicPath}'}}, 'node3': {'typeExecution': 'transformTemplate', 'input_parameters': {'templates': '{node2.input_parameters.executeDir}', 'parameters': '{node1.input_parameters.target}'}}, 'finalnode_xx': {'name': 'finalnode_xx', 'typeExecution': 'parameters', 'requires': ['baseParameters', 'node1', 'node2', 'node3'], 'input_parameters': {}}}}}['workflow']

    def output(self):
        return luigi.LocalTarget("outputs/baseParameters_0.json")

    def requires(self):
        return dict(
                   )

    def run(self):
        target = self.output()
        target.makedirs()
        
        task_executer_mapping = {}
        
        parameters_from_required = self.get_all_required_outputs()        
        params = dict(parameters_from_required)
        params['parameters'] = {'basicPath': 'Hello'}
        params['WebGUI']     = {'formData': {'sourceDir': '/home/blah1'}}
        
        executer_parameters = self.build_executer_parameters(task_executer_mapping, params)
                    
        from pyHermes.executers.generalExecuter import parameterExecuter  
        output =  parameterExecuter(self._taskJSON).run(**executer_parameters)
        
        params['input_parameters'] = executer_parameters 
        params['output'] = output        
        
        out_params = params
        with open(self.output().fn,"w") as outfile:
            json.dump(out_params,outfile)

class node1_0(luigi.Task,hermesutils):

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
        
        self._workflowJSON = {'workflow': {'root': None, 'nodes': {'baseParameters': {'typeExecution': 'parameters', 'WebGUI': {'formData': {'sourceDir': '/home/blah1'}}, 'parameters': {'basicPath': 'Hello'}, 'input_parameters': {}}, 'node1': {'typeExecution': 'copyDir', 'input_parameters': {'source': '{baseParameters.WebGUI.formData.sourceDir}', 'target': '{WebGUI.formData.target}', 'tester': '{parameters.name}'}, 'parameters': {'name': 'good'}, 'WebGUI': {'formData': {'target': '/home/blah2'}}}, 'node2': {'typeExecution': 'executeScript', 'input_parameters': {'executeDir': '{node1.input_parameters.target}', 'execute': 'runMe {node1.WebGUI.formData.target} {node1.output.copyDir}', 'father': '{node1.baseParameters.parameters.basicPath}'}}, 'node3': {'typeExecution': 'transformTemplate', 'input_parameters': {'templates': '{node2.input_parameters.executeDir}', 'parameters': '{node1.input_parameters.target}'}}, 'finalnode_xx': {'name': 'finalnode_xx', 'typeExecution': 'parameters', 'requires': ['baseParameters', 'node1', 'node2', 'node3'], 'input_parameters': {}}}}}['workflow']

    def output(self):
        return luigi.LocalTarget("outputs/node1_0.json")

    def requires(self):
        return dict(
                       baseParameters=baseParameters_0()
                   )

    def run(self):
        target = self.output()
        target.makedirs()
        
        task_executer_mapping = {'source': '{baseParameters.WebGUI.formData.sourceDir}', 'target': '{WebGUI.formData.target}', 'tester': '{parameters.name}'}
        
        parameters_from_required = self.get_all_required_outputs()        
        params = dict(parameters_from_required)
        params['parameters'] = {'name': 'good'}
        params['WebGUI']     = {'formData': {'target': '/home/blah2'}}
        
        executer_parameters = self.build_executer_parameters(task_executer_mapping, params)
                    
        from pyHermes.executers.fileSystemExecuter import copyDir  
        output =  copyDir(self._taskJSON).run(**executer_parameters)
        
        params['input_parameters'] = executer_parameters 
        params['output'] = output        
        
        out_params = params
        with open(self.output().fn,"w") as outfile:
            json.dump(out_params,outfile)

class node2_0(luigi.Task,hermesutils):

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
        
        self._workflowJSON = {'workflow': {'root': None, 'nodes': {'baseParameters': {'typeExecution': 'parameters', 'WebGUI': {'formData': {'sourceDir': '/home/blah1'}}, 'parameters': {'basicPath': 'Hello'}, 'input_parameters': {}}, 'node1': {'typeExecution': 'copyDir', 'input_parameters': {'source': '{baseParameters.WebGUI.formData.sourceDir}', 'target': '{WebGUI.formData.target}', 'tester': '{parameters.name}'}, 'parameters': {'name': 'good'}, 'WebGUI': {'formData': {'target': '/home/blah2'}}}, 'node2': {'typeExecution': 'executeScript', 'input_parameters': {'executeDir': '{node1.input_parameters.target}', 'execute': 'runMe {node1.WebGUI.formData.target} {node1.output.copyDir}', 'father': '{node1.baseParameters.parameters.basicPath}'}}, 'node3': {'typeExecution': 'transformTemplate', 'input_parameters': {'templates': '{node2.input_parameters.executeDir}', 'parameters': '{node1.input_parameters.target}'}}, 'finalnode_xx': {'name': 'finalnode_xx', 'typeExecution': 'parameters', 'requires': ['baseParameters', 'node1', 'node2', 'node3'], 'input_parameters': {}}}}}['workflow']

    def output(self):
        return luigi.LocalTarget("outputs/node2_0.json")

    def requires(self):
        return dict(
                       node1=node1_0()
                   )

    def run(self):
        target = self.output()
        target.makedirs()
        
        task_executer_mapping = {'executeDir': '{node1.input_parameters.target}', 'execute': 'runMe {node1.WebGUI.formData.target} {node1.output.copyDir}', 'father': '{node1.baseParameters.parameters.basicPath}'}
        
        parameters_from_required = self.get_all_required_outputs()        
        params = dict(parameters_from_required)
        params['parameters'] = {}
        params['WebGUI']     = {}
        
        executer_parameters = self.build_executer_parameters(task_executer_mapping, params)
                    
        from pyHermes.executers.fileSystemExecuter import executeScript  
        output =  executeScript(self._taskJSON).run(**executer_parameters)
        
        params['input_parameters'] = executer_parameters 
        params['output'] = output        
        
        out_params = params
        with open(self.output().fn,"w") as outfile:
            json.dump(out_params,outfile)

class node3_0(luigi.Task,hermesutils):

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
        
        self._workflowJSON = {'workflow': {'root': None, 'nodes': {'baseParameters': {'typeExecution': 'parameters', 'WebGUI': {'formData': {'sourceDir': '/home/blah1'}}, 'parameters': {'basicPath': 'Hello'}, 'input_parameters': {}}, 'node1': {'typeExecution': 'copyDir', 'input_parameters': {'source': '{baseParameters.WebGUI.formData.sourceDir}', 'target': '{WebGUI.formData.target}', 'tester': '{parameters.name}'}, 'parameters': {'name': 'good'}, 'WebGUI': {'formData': {'target': '/home/blah2'}}}, 'node2': {'typeExecution': 'executeScript', 'input_parameters': {'executeDir': '{node1.input_parameters.target}', 'execute': 'runMe {node1.WebGUI.formData.target} {node1.output.copyDir}', 'father': '{node1.baseParameters.parameters.basicPath}'}}, 'node3': {'typeExecution': 'transformTemplate', 'input_parameters': {'templates': '{node2.input_parameters.executeDir}', 'parameters': '{node1.input_parameters.target}'}}, 'finalnode_xx': {'name': 'finalnode_xx', 'typeExecution': 'parameters', 'requires': ['baseParameters', 'node1', 'node2', 'node3'], 'input_parameters': {}}}}}['workflow']

    def output(self):
        return luigi.LocalTarget("outputs/node3_0.json")

    def requires(self):
        return dict(
                       node1=node1_0(),
                       node2=node2_0()
                   )

    def run(self):
        target = self.output()
        target.makedirs()
        
        task_executer_mapping = {'templates': '{node2.input_parameters.executeDir}', 'parameters': '{node1.input_parameters.target}'}
        
        parameters_from_required = self.get_all_required_outputs()        
        params = dict(parameters_from_required)
        params['parameters'] = {}
        params['WebGUI']     = {}
        
        executer_parameters = self.build_executer_parameters(task_executer_mapping, params)
                    
        from pyHermes.executers.generalExecuter import transformTemplate  
        output =  transformTemplate(self._taskJSON).run(**executer_parameters)
        
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
        
        self._workflowJSON = {'workflow': {'root': None, 'nodes': {'baseParameters': {'typeExecution': 'parameters', 'WebGUI': {'formData': {'sourceDir': '/home/blah1'}}, 'parameters': {'basicPath': 'Hello'}, 'input_parameters': {}}, 'node1': {'typeExecution': 'copyDir', 'input_parameters': {'source': '{baseParameters.WebGUI.formData.sourceDir}', 'target': '{WebGUI.formData.target}', 'tester': '{parameters.name}'}, 'parameters': {'name': 'good'}, 'WebGUI': {'formData': {'target': '/home/blah2'}}}, 'node2': {'typeExecution': 'executeScript', 'input_parameters': {'executeDir': '{node1.input_parameters.target}', 'execute': 'runMe {node1.WebGUI.formData.target} {node1.output.copyDir}', 'father': '{node1.baseParameters.parameters.basicPath}'}}, 'node3': {'typeExecution': 'transformTemplate', 'input_parameters': {'templates': '{node2.input_parameters.executeDir}', 'parameters': '{node1.input_parameters.target}'}}, 'finalnode_xx': {'name': 'finalnode_xx', 'typeExecution': 'parameters', 'requires': ['baseParameters', 'node1', 'node2', 'node3'], 'input_parameters': {}}}}}['workflow']

    def output(self):
        return luigi.LocalTarget("outputs/finalnode_xx_0.json")

    def requires(self):
        return dict(
                       node1=node1_0(),
                       node3=node3_0(),
                       baseParameters=baseParameters_0(),
                       node2=node2_0()
                   )

    def run(self):
        target = self.output()
        target.makedirs()
        
        task_executer_mapping = {}
        
        parameters_from_required = self.get_all_required_outputs()        
        params = dict(parameters_from_required)
        params['parameters'] = {}
        params['WebGUI']     = {}
        
        executer_parameters = self.build_executer_parameters(task_executer_mapping, params)
                    
        from pyHermes.executers.generalExecuter import parameterExecuter  
        output =  parameterExecuter(self._taskJSON).run(**executer_parameters)
        
        params['input_parameters'] = executer_parameters 
        params['output'] = output        
        
        out_params = params
        with open(self.output().fn,"w") as outfile:
            json.dump(out_params,outfile)
