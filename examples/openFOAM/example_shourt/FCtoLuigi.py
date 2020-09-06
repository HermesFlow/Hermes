

import shutil
import os
import luigi
import json 
import sys

sys.path.insert(1, "/home/noga/Noga/FreeCad/github/Hermes/master/Hermes")
from hermes.engines.luigi.taskUtils import utils as hermesutils

class FvSchemes_0(luigi.Task,hermesutils):

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
        
        self._workflowJSON = {'workflow': {'root': None, 'Templates': {}, 'nodeList': ['ControlDict', 'FvSchemes', 'FileWriter'], 'nodes': {'ControlDict': {'Execution': {'type': 'jinjaExecuters.jinja', 'input_parameters': {'values': '{WebGui.formData}', 'template': 'openFOAM/simpleFOAM/ControlDict'}}, 'GUI': {'Type': 'WebGuiNode', 'Properties': {}, 'WebGui': {'Schema': {'title': '', 'description': '', 'type': 'object', 'properties': {'application': {'type': 'string', 'title': 'application'}, 'startFrom': {'type': 'string', 'enum': ['firstTime', 'startTime', 'latestTime'], 'description': 'Controls the start time of the simulation.'}, 'startTime': {'title': 'startTime', 'type': 'number', 'description': 'Start time for the simulation with startFrom startTime'}, 'stopAt': {'type': 'string', 'enum': ['endTime', 'writeNow', 'noWriteNow', 'nextwrite'], 'description': 'Controls the end time of the simulation.'}, 'endTime': {'title': 'endTime', 'type': 'number', 'description': 'End time for the simulation when stopAt endTime; is specified.'}, 'deltaT': {'title': 'deltaT', 'type': 'number', 'description': 'Time step of the simulation.'}, 'writeControl': {'type': 'string', 'enum': ['timeStep', 'runTime', 'adjustableRunTime', 'cpuTime', 'clockTime'], 'description': 'Controls the timing of write output to file.'}, 'writeInterval': {'title': 'writeInterval', 'type': 'integer', 'description': 'Scalar used in conjunction with writeControl described above.'}, 'purgeWrite': {'title': 'purgeWrite', 'type': 'integer', 'description': 'Integer representing a limit on the number of time directories that are stored by overwriting time directories on a cyclic basis.'}, 'writeFormat': {'type': 'string', 'enum': ['ascii', 'binary'], 'description': 'Specifies the format of the data files.'}, 'writePrecision': {'title': 'writePrecision', 'type': 'integer', 'description': 'Integer used in conjunction with writeFormat described above.'}, 'writeCompression': {'type': 'boolean', 'title': 'writeCompression', 'description': 'Switch to specify whether files are compressed with gzip'}, 'timeFormat': {'type': 'string', 'enum': ['fixed', 'scientific', 'general'], 'description': 'Controls the timing of write output to file.'}, 'timePrecision': {'title': 'timePrecision', 'type': 'integer', 'description': 'Integer used in conjunction with timeFormat described above'}, 'runTimeModifiable': {'type': 'boolean', 'title': 'runTimeModifiable', 'description': 'Switch for whether dictionaries, e.g. controlDict, are re-read during a simulation at the beginning of each time step, allowing the user to modify parameters during a simulation.'}, 'graphFormat': {'type': 'string', 'enum': ['no graph', 'raw', 'gnuplot', 'xmgr', 'jplot'], 'description': 'Format for graph data written by an application.'}, 'adjustTimeStep': {'type': 'boolean', 'title': 'adjustTimeStep', 'description': 'Switch used by some solvers to adjust the time step during the simulation, usually according to maxCo.'}, 'maxCo': {'title': 'maxCo', 'type': 'number', 'description': 'Maximum Courant number.'}, 'interpolate': {'type': 'boolean', 'title': 'interpolate'}, 'libs': {'type': 'array', 'title': 'libs', 'items': {'type': 'string', 'description': 'List of additional libraries (on $LD_LIBRARY_PATH) to be loaded at run-time'}}, 'functions': {'type': 'array', 'title': 'functions', 'items': {'type': 'string', 'description': 'Dictionary of functions, e.g.  probes to be loaded at run-time'}}}}, 'uiSchema': {'listOfStrings': {'items': {'ui:emptyValue': ''}}, 'functions': {'items': {'ui:emptyValue': ''}}}, 'formData': {'application': 'simpleFoam', 'startFrom': 'startTime', 'startTime': 0, 'stopAt': 'endTime', 'endTime': 1000, 'deltaT': 1, 'writeControl': 'timeStep', 'writeInterval': 100, 'purgeWrite': 0, 'writeFormat': 'ascii', 'writePrecision': 7, 'writeCompression': False, 'timeFormat': 'general', 'timePrecision': 6, 'runTimeModifiable': True, 'interpolate': True, 'functions': ['probes.txt']}}}}, 'FvSchemes': {'Execution': {'type': 'jinjaExecuters.jinja', 'input_parameters': {'values': '{WebGui.formData}', 'template': 'openFOAM/simpleFOAM/FvSchemes'}}, 'GUI': {'Type': 'WebGuiNode', 'Properties': {}, 'WebGui': {'Schema': {'type': 'object', 'properties': {'ddtSchemes': {'type': 'object', 'title': 'timeScheme', 'properties': {'default': {'type': 'string', 'enum': ['steadyState', 'Euler', 'backward', 'CrankNicolson', 'localEuler'], 'description': 'The discretisation schemes for each term can be selected from those listed below.'}}}, 'gradSchemes': {'type': 'object', 'title': 'gradSchemes', 'properties': {'default': {'type': 'string', 'title': 'default', 'enum': ['Gauss linear', 'leastSquares', 'Gauss'], 'description': 'The discretisation scheme'}, 'gradU': {'type': 'string', 'title': 'grad(U)', 'description': 'discretisation of velocity gradient terms is overridden to improve boundedness and stability'}, 'gradK': {'type': 'string', 'title': 'grad(k)', 'description': 'discretisation of k gradient terms is overridden to improve boundedness and stability'}, 'gradEpsilon': {'type': 'string', 'title': 'grad(epsilon)', 'description': 'discretisation of epsilon gradient terms is overridden to improve boundedness and stability'}}}, 'divSchemes': {'type': 'object', 'title': 'divSchemes', 'properties': {'default': {'type': 'string', 'title': 'default', 'description': 'contains divergence terms.'}, 'divPhiU': {'type': 'string', 'title': 'div(phi,U)'}, 'divPhiK': {'type': 'string', 'title': 'div(phi,k)'}, 'divPhiEpsilon': {'type': 'string', 'title': 'div(phi,epsilon)'}, 'divPhiE': {'type': 'string', 'title': 'div(phi,e)'}, 'divPhiOmega': {'type': 'string', 'title': 'div(phi,omega)'}, 'moreDivSchemesProperties': {'type': 'object', 'additionalProperties': {'type': 'string'}}}}, 'laplacianSchemes': {'type': 'object', 'title': 'laplacianSchemes', 'description': 'Laplacian terms.', 'properties': {'default': {'type': 'string', 'title': 'default'}}}, 'interpolationSchemes': {'type': 'object', 'title': 'interpolationSchemes', 'description': 'terms that are interpolations of values typically from cell centres to face centres', 'properties': {'default': {'type': 'string', 'title': 'default'}}}, 'snGradSchemes': {'type': 'object', 'title': 'snGradSchemes', 'description': 'contains surface normal gradient terms', 'properties': {'default': {'type': 'string', 'title': 'default'}}}, 'wallDist': {'type': 'object', 'title': 'wallDist', 'properties': {'method': {'type': 'string', 'title': 'method'}}}, 'fluxRequired': {'type': 'object', 'title': 'fluxRequired', 'properties': {'default': {'type': 'string', 'title': 'default'}}}}}, 'uiSchema': {}, 'formData': {'ddtSchemes': {'default': 'steadyState'}, 'gradSchemes': {'default': 'Gauss linear', 'gradU': 'cellLimited Gauss linear 1', 'gradK': 'cellLimited Gauss linear 1', 'gradEpsilon': 'cellLimited Gauss linear 1'}, 'divSchemes': {'moreDivSchemesProperties': {'divNuEff': 'Gauss linear'}, 'default': 'none', 'divPhiU': 'bounded Gauss upwind', 'divPhiK': 'bounded Gauss upwind', 'divPhiEpsilon': 'bounded Gauss upwind', 'divPhiOmega': 'bounded Gauss upwind'}, 'laplacianSchemes': {'default': 'Gauss linear corrected'}, 'interpolationSchemes': {'default': 'linear'}, 'snGradSchemes': {'default': 'corrected'}, 'wallDist': {'method': 'meshWave'}}}}}, 'FileWriter': {'Execution': {'type': 'generalExecuters.FilesWriter', 'input_parameters': {'casePath': 'OpenFOAMfiles/', 'Files': {'system/controlDict': '{ControlDict.output.openFOAMfile}', 'system/fvSchemes': '{FvSchemes.output.openFOAMfile}'}}}, 'GUI': {'Type': 'WebGuiNode', 'Properties': {}, 'WebGui': {}}}, 'finalnode_xx': {'name': 'finalnode_xx', 'Execution': {'type': 'generalExecuters.parameter', 'input_parameters': {}}, 'requires': ['ControlDict', 'FvSchemes', 'FileWriter'], 'GUI': {'TypeFC': {}, 'Properties': {}, 'WebGui': {}}}}}}['workflow']

    def output(self):
        return luigi.LocalTarget("outputsOriginal/FvSchemes_0.json")

    def requires(self):
        return dict(
                   )

    def run(self):
        target = self.output()
        target.makedirs()
        
        task_executer_mapping = {'values': '{WebGui.formData}', 'template': 'openFOAM/simpleFOAM/FvSchemes'}
        
        parameters_from_required = self.get_all_required_outputs()        
        params = dict(parameters_from_required)
        params['formData']   = {}
        params['files']      = {}
        params['Schema']     = {}
        params['uiSchema']   = {}
        params['Properties'] = {}
        params['WebGui']     = {'Schema': {'type': 'object', 'properties': {'ddtSchemes': {'type': 'object', 'title': 'timeScheme', 'properties': {'default': {'type': 'string', 'enum': ['steadyState', 'Euler', 'backward', 'CrankNicolson', 'localEuler'], 'description': 'The discretisation schemes for each term can be selected from those listed below.'}}}, 'gradSchemes': {'type': 'object', 'title': 'gradSchemes', 'properties': {'default': {'type': 'string', 'title': 'default', 'enum': ['Gauss linear', 'leastSquares', 'Gauss'], 'description': 'The discretisation scheme'}, 'gradU': {'type': 'string', 'title': 'grad(U)', 'description': 'discretisation of velocity gradient terms is overridden to improve boundedness and stability'}, 'gradK': {'type': 'string', 'title': 'grad(k)', 'description': 'discretisation of k gradient terms is overridden to improve boundedness and stability'}, 'gradEpsilon': {'type': 'string', 'title': 'grad(epsilon)', 'description': 'discretisation of epsilon gradient terms is overridden to improve boundedness and stability'}}}, 'divSchemes': {'type': 'object', 'title': 'divSchemes', 'properties': {'default': {'type': 'string', 'title': 'default', 'description': 'contains divergence terms.'}, 'divPhiU': {'type': 'string', 'title': 'div(phi,U)'}, 'divPhiK': {'type': 'string', 'title': 'div(phi,k)'}, 'divPhiEpsilon': {'type': 'string', 'title': 'div(phi,epsilon)'}, 'divPhiE': {'type': 'string', 'title': 'div(phi,e)'}, 'divPhiOmega': {'type': 'string', 'title': 'div(phi,omega)'}, 'moreDivSchemesProperties': {'type': 'object', 'additionalProperties': {'type': 'string'}}}}, 'laplacianSchemes': {'type': 'object', 'title': 'laplacianSchemes', 'description': 'Laplacian terms.', 'properties': {'default': {'type': 'string', 'title': 'default'}}}, 'interpolationSchemes': {'type': 'object', 'title': 'interpolationSchemes', 'description': 'terms that are interpolations of values typically from cell centres to face centres', 'properties': {'default': {'type': 'string', 'title': 'default'}}}, 'snGradSchemes': {'type': 'object', 'title': 'snGradSchemes', 'description': 'contains surface normal gradient terms', 'properties': {'default': {'type': 'string', 'title': 'default'}}}, 'wallDist': {'type': 'object', 'title': 'wallDist', 'properties': {'method': {'type': 'string', 'title': 'method'}}}, 'fluxRequired': {'type': 'object', 'title': 'fluxRequired', 'properties': {'default': {'type': 'string', 'title': 'default'}}}}}, 'uiSchema': {}, 'formData': {'ddtSchemes': {'default': 'steadyState'}, 'gradSchemes': {'default': 'Gauss linear', 'gradU': 'cellLimited Gauss linear 1', 'gradK': 'cellLimited Gauss linear 1', 'gradEpsilon': 'cellLimited Gauss linear 1'}, 'divSchemes': {'moreDivSchemesProperties': {'divNuEff': 'Gauss linear'}, 'default': 'none', 'divPhiU': 'bounded Gauss upwind', 'divPhiK': 'bounded Gauss upwind', 'divPhiEpsilon': 'bounded Gauss upwind', 'divPhiOmega': 'bounded Gauss upwind'}, 'laplacianSchemes': {'default': 'Gauss linear corrected'}, 'interpolationSchemes': {'default': 'linear'}, 'snGradSchemes': {'default': 'corrected'}, 'wallDist': {'method': 'meshWave'}}}
        
       
        executer_parameters = self.build_executer_parameters(task_executer_mapping, params)
        executer_parameters['WD_path']='/home/noga/Noga/FreeCad/github/Hermes/master/Hermes/examples/openFOAM/example_shourt'
                    
        from hermes.Resources.executers.jinjaExecuters import jinjaExecuter  
        output = jinjaExecuter(self._taskJSON).run(**executer_parameters)
        
        params['input_parameters'] = executer_parameters 
        params['output'] = output        
        
        out_params = params
        with open(self.output().fn, "w") as outfile:
            json.dump(out_params, outfile)

class ControlDict_0(luigi.Task,hermesutils):

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
        
        self._workflowJSON = {'workflow': {'root': None, 'Templates': {}, 'nodeList': ['ControlDict', 'FvSchemes', 'FileWriter'], 'nodes': {'ControlDict': {'Execution': {'type': 'jinjaExecuters.jinja', 'input_parameters': {'values': '{WebGui.formData}', 'template': 'openFOAM/simpleFOAM/ControlDict'}}, 'GUI': {'Type': 'WebGuiNode', 'Properties': {}, 'WebGui': {'Schema': {'title': '', 'description': '', 'type': 'object', 'properties': {'application': {'type': 'string', 'title': 'application'}, 'startFrom': {'type': 'string', 'enum': ['firstTime', 'startTime', 'latestTime'], 'description': 'Controls the start time of the simulation.'}, 'startTime': {'title': 'startTime', 'type': 'number', 'description': 'Start time for the simulation with startFrom startTime'}, 'stopAt': {'type': 'string', 'enum': ['endTime', 'writeNow', 'noWriteNow', 'nextwrite'], 'description': 'Controls the end time of the simulation.'}, 'endTime': {'title': 'endTime', 'type': 'number', 'description': 'End time for the simulation when stopAt endTime; is specified.'}, 'deltaT': {'title': 'deltaT', 'type': 'number', 'description': 'Time step of the simulation.'}, 'writeControl': {'type': 'string', 'enum': ['timeStep', 'runTime', 'adjustableRunTime', 'cpuTime', 'clockTime'], 'description': 'Controls the timing of write output to file.'}, 'writeInterval': {'title': 'writeInterval', 'type': 'integer', 'description': 'Scalar used in conjunction with writeControl described above.'}, 'purgeWrite': {'title': 'purgeWrite', 'type': 'integer', 'description': 'Integer representing a limit on the number of time directories that are stored by overwriting time directories on a cyclic basis.'}, 'writeFormat': {'type': 'string', 'enum': ['ascii', 'binary'], 'description': 'Specifies the format of the data files.'}, 'writePrecision': {'title': 'writePrecision', 'type': 'integer', 'description': 'Integer used in conjunction with writeFormat described above.'}, 'writeCompression': {'type': 'boolean', 'title': 'writeCompression', 'description': 'Switch to specify whether files are compressed with gzip'}, 'timeFormat': {'type': 'string', 'enum': ['fixed', 'scientific', 'general'], 'description': 'Controls the timing of write output to file.'}, 'timePrecision': {'title': 'timePrecision', 'type': 'integer', 'description': 'Integer used in conjunction with timeFormat described above'}, 'runTimeModifiable': {'type': 'boolean', 'title': 'runTimeModifiable', 'description': 'Switch for whether dictionaries, e.g. controlDict, are re-read during a simulation at the beginning of each time step, allowing the user to modify parameters during a simulation.'}, 'graphFormat': {'type': 'string', 'enum': ['no graph', 'raw', 'gnuplot', 'xmgr', 'jplot'], 'description': 'Format for graph data written by an application.'}, 'adjustTimeStep': {'type': 'boolean', 'title': 'adjustTimeStep', 'description': 'Switch used by some solvers to adjust the time step during the simulation, usually according to maxCo.'}, 'maxCo': {'title': 'maxCo', 'type': 'number', 'description': 'Maximum Courant number.'}, 'interpolate': {'type': 'boolean', 'title': 'interpolate'}, 'libs': {'type': 'array', 'title': 'libs', 'items': {'type': 'string', 'description': 'List of additional libraries (on $LD_LIBRARY_PATH) to be loaded at run-time'}}, 'functions': {'type': 'array', 'title': 'functions', 'items': {'type': 'string', 'description': 'Dictionary of functions, e.g.  probes to be loaded at run-time'}}}}, 'uiSchema': {'listOfStrings': {'items': {'ui:emptyValue': ''}}, 'functions': {'items': {'ui:emptyValue': ''}}}, 'formData': {'application': 'simpleFoam', 'startFrom': 'startTime', 'startTime': 0, 'stopAt': 'endTime', 'endTime': 1000, 'deltaT': 1, 'writeControl': 'timeStep', 'writeInterval': 100, 'purgeWrite': 0, 'writeFormat': 'ascii', 'writePrecision': 7, 'writeCompression': False, 'timeFormat': 'general', 'timePrecision': 6, 'runTimeModifiable': True, 'interpolate': True, 'functions': ['probes.txt']}}}}, 'FvSchemes': {'Execution': {'type': 'jinjaExecuters.jinja', 'input_parameters': {'values': '{WebGui.formData}', 'template': 'openFOAM/simpleFOAM/FvSchemes'}}, 'GUI': {'Type': 'WebGuiNode', 'Properties': {}, 'WebGui': {'Schema': {'type': 'object', 'properties': {'ddtSchemes': {'type': 'object', 'title': 'timeScheme', 'properties': {'default': {'type': 'string', 'enum': ['steadyState', 'Euler', 'backward', 'CrankNicolson', 'localEuler'], 'description': 'The discretisation schemes for each term can be selected from those listed below.'}}}, 'gradSchemes': {'type': 'object', 'title': 'gradSchemes', 'properties': {'default': {'type': 'string', 'title': 'default', 'enum': ['Gauss linear', 'leastSquares', 'Gauss'], 'description': 'The discretisation scheme'}, 'gradU': {'type': 'string', 'title': 'grad(U)', 'description': 'discretisation of velocity gradient terms is overridden to improve boundedness and stability'}, 'gradK': {'type': 'string', 'title': 'grad(k)', 'description': 'discretisation of k gradient terms is overridden to improve boundedness and stability'}, 'gradEpsilon': {'type': 'string', 'title': 'grad(epsilon)', 'description': 'discretisation of epsilon gradient terms is overridden to improve boundedness and stability'}}}, 'divSchemes': {'type': 'object', 'title': 'divSchemes', 'properties': {'default': {'type': 'string', 'title': 'default', 'description': 'contains divergence terms.'}, 'divPhiU': {'type': 'string', 'title': 'div(phi,U)'}, 'divPhiK': {'type': 'string', 'title': 'div(phi,k)'}, 'divPhiEpsilon': {'type': 'string', 'title': 'div(phi,epsilon)'}, 'divPhiE': {'type': 'string', 'title': 'div(phi,e)'}, 'divPhiOmega': {'type': 'string', 'title': 'div(phi,omega)'}, 'moreDivSchemesProperties': {'type': 'object', 'additionalProperties': {'type': 'string'}}}}, 'laplacianSchemes': {'type': 'object', 'title': 'laplacianSchemes', 'description': 'Laplacian terms.', 'properties': {'default': {'type': 'string', 'title': 'default'}}}, 'interpolationSchemes': {'type': 'object', 'title': 'interpolationSchemes', 'description': 'terms that are interpolations of values typically from cell centres to face centres', 'properties': {'default': {'type': 'string', 'title': 'default'}}}, 'snGradSchemes': {'type': 'object', 'title': 'snGradSchemes', 'description': 'contains surface normal gradient terms', 'properties': {'default': {'type': 'string', 'title': 'default'}}}, 'wallDist': {'type': 'object', 'title': 'wallDist', 'properties': {'method': {'type': 'string', 'title': 'method'}}}, 'fluxRequired': {'type': 'object', 'title': 'fluxRequired', 'properties': {'default': {'type': 'string', 'title': 'default'}}}}}, 'uiSchema': {}, 'formData': {'ddtSchemes': {'default': 'steadyState'}, 'gradSchemes': {'default': 'Gauss linear', 'gradU': 'cellLimited Gauss linear 1', 'gradK': 'cellLimited Gauss linear 1', 'gradEpsilon': 'cellLimited Gauss linear 1'}, 'divSchemes': {'moreDivSchemesProperties': {'divNuEff': 'Gauss linear'}, 'default': 'none', 'divPhiU': 'bounded Gauss upwind', 'divPhiK': 'bounded Gauss upwind', 'divPhiEpsilon': 'bounded Gauss upwind', 'divPhiOmega': 'bounded Gauss upwind'}, 'laplacianSchemes': {'default': 'Gauss linear corrected'}, 'interpolationSchemes': {'default': 'linear'}, 'snGradSchemes': {'default': 'corrected'}, 'wallDist': {'method': 'meshWave'}}}}}, 'FileWriter': {'Execution': {'type': 'generalExecuters.FilesWriter', 'input_parameters': {'casePath': 'OpenFOAMfiles/', 'Files': {'system/controlDict': '{ControlDict.output.openFOAMfile}', 'system/fvSchemes': '{FvSchemes.output.openFOAMfile}'}}}, 'GUI': {'Type': 'WebGuiNode', 'Properties': {}, 'WebGui': {}}}, 'finalnode_xx': {'name': 'finalnode_xx', 'Execution': {'type': 'generalExecuters.parameter', 'input_parameters': {}}, 'requires': ['ControlDict', 'FvSchemes', 'FileWriter'], 'GUI': {'TypeFC': {}, 'Properties': {}, 'WebGui': {}}}}}}['workflow']

    def output(self):
        return luigi.LocalTarget("outputsOriginal/ControlDict_0.json")

    def requires(self):
        return dict(
                   )

    def run(self):
        target = self.output()
        target.makedirs()
        
        task_executer_mapping = {'values': '{WebGui.formData}', 'template': 'openFOAM/simpleFOAM/ControlDict'}
        
        parameters_from_required = self.get_all_required_outputs()        
        params = dict(parameters_from_required)
        params['formData']   = {}
        params['files']      = {}
        params['Schema']     = {}
        params['uiSchema']   = {}
        params['Properties'] = {}
        params['WebGui']     = {'Schema': {'title': '', 'description': '', 'type': 'object', 'properties': {'application': {'type': 'string', 'title': 'application'}, 'startFrom': {'type': 'string', 'enum': ['firstTime', 'startTime', 'latestTime'], 'description': 'Controls the start time of the simulation.'}, 'startTime': {'title': 'startTime', 'type': 'number', 'description': 'Start time for the simulation with startFrom startTime'}, 'stopAt': {'type': 'string', 'enum': ['endTime', 'writeNow', 'noWriteNow', 'nextwrite'], 'description': 'Controls the end time of the simulation.'}, 'endTime': {'title': 'endTime', 'type': 'number', 'description': 'End time for the simulation when stopAt endTime; is specified.'}, 'deltaT': {'title': 'deltaT', 'type': 'number', 'description': 'Time step of the simulation.'}, 'writeControl': {'type': 'string', 'enum': ['timeStep', 'runTime', 'adjustableRunTime', 'cpuTime', 'clockTime'], 'description': 'Controls the timing of write output to file.'}, 'writeInterval': {'title': 'writeInterval', 'type': 'integer', 'description': 'Scalar used in conjunction with writeControl described above.'}, 'purgeWrite': {'title': 'purgeWrite', 'type': 'integer', 'description': 'Integer representing a limit on the number of time directories that are stored by overwriting time directories on a cyclic basis.'}, 'writeFormat': {'type': 'string', 'enum': ['ascii', 'binary'], 'description': 'Specifies the format of the data files.'}, 'writePrecision': {'title': 'writePrecision', 'type': 'integer', 'description': 'Integer used in conjunction with writeFormat described above.'}, 'writeCompression': {'type': 'boolean', 'title': 'writeCompression', 'description': 'Switch to specify whether files are compressed with gzip'}, 'timeFormat': {'type': 'string', 'enum': ['fixed', 'scientific', 'general'], 'description': 'Controls the timing of write output to file.'}, 'timePrecision': {'title': 'timePrecision', 'type': 'integer', 'description': 'Integer used in conjunction with timeFormat described above'}, 'runTimeModifiable': {'type': 'boolean', 'title': 'runTimeModifiable', 'description': 'Switch for whether dictionaries, e.g. controlDict, are re-read during a simulation at the beginning of each time step, allowing the user to modify parameters during a simulation.'}, 'graphFormat': {'type': 'string', 'enum': ['no graph', 'raw', 'gnuplot', 'xmgr', 'jplot'], 'description': 'Format for graph data written by an application.'}, 'adjustTimeStep': {'type': 'boolean', 'title': 'adjustTimeStep', 'description': 'Switch used by some solvers to adjust the time step during the simulation, usually according to maxCo.'}, 'maxCo': {'title': 'maxCo', 'type': 'number', 'description': 'Maximum Courant number.'}, 'interpolate': {'type': 'boolean', 'title': 'interpolate'}, 'libs': {'type': 'array', 'title': 'libs', 'items': {'type': 'string', 'description': 'List of additional libraries (on $LD_LIBRARY_PATH) to be loaded at run-time'}}, 'functions': {'type': 'array', 'title': 'functions', 'items': {'type': 'string', 'description': 'Dictionary of functions, e.g.  probes to be loaded at run-time'}}}}, 'uiSchema': {'listOfStrings': {'items': {'ui:emptyValue': ''}}, 'functions': {'items': {'ui:emptyValue': ''}}}, 'formData': {'application': 'simpleFoam', 'startFrom': 'startTime', 'startTime': 0, 'stopAt': 'endTime', 'endTime': 1000, 'deltaT': 1, 'writeControl': 'timeStep', 'writeInterval': 100, 'purgeWrite': 0, 'writeFormat': 'ascii', 'writePrecision': 7, 'writeCompression': False, 'timeFormat': 'general', 'timePrecision': 6, 'runTimeModifiable': True, 'interpolate': True, 'functions': ['probes.txt']}}
        
       
        executer_parameters = self.build_executer_parameters(task_executer_mapping, params)
        executer_parameters['WD_path']='/home/noga/Noga/FreeCad/github/Hermes/master/Hermes/examples/openFOAM/example_shourt'
                    
        from hermes.Resources.executers.jinjaExecuters import jinjaExecuter  
        output = jinjaExecuter(self._taskJSON).run(**executer_parameters)
        
        params['input_parameters'] = executer_parameters 
        params['output'] = output        
        
        out_params = params
        with open(self.output().fn, "w") as outfile:
            json.dump(out_params, outfile)

class FileWriter_0(luigi.Task,hermesutils):

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
        
        self._workflowJSON = {'workflow': {'root': None, 'Templates': {}, 'nodeList': ['ControlDict', 'FvSchemes', 'FileWriter'], 'nodes': {'ControlDict': {'Execution': {'type': 'jinjaExecuters.jinja', 'input_parameters': {'values': '{WebGui.formData}', 'template': 'openFOAM/simpleFOAM/ControlDict'}}, 'GUI': {'Type': 'WebGuiNode', 'Properties': {}, 'WebGui': {'Schema': {'title': '', 'description': '', 'type': 'object', 'properties': {'application': {'type': 'string', 'title': 'application'}, 'startFrom': {'type': 'string', 'enum': ['firstTime', 'startTime', 'latestTime'], 'description': 'Controls the start time of the simulation.'}, 'startTime': {'title': 'startTime', 'type': 'number', 'description': 'Start time for the simulation with startFrom startTime'}, 'stopAt': {'type': 'string', 'enum': ['endTime', 'writeNow', 'noWriteNow', 'nextwrite'], 'description': 'Controls the end time of the simulation.'}, 'endTime': {'title': 'endTime', 'type': 'number', 'description': 'End time for the simulation when stopAt endTime; is specified.'}, 'deltaT': {'title': 'deltaT', 'type': 'number', 'description': 'Time step of the simulation.'}, 'writeControl': {'type': 'string', 'enum': ['timeStep', 'runTime', 'adjustableRunTime', 'cpuTime', 'clockTime'], 'description': 'Controls the timing of write output to file.'}, 'writeInterval': {'title': 'writeInterval', 'type': 'integer', 'description': 'Scalar used in conjunction with writeControl described above.'}, 'purgeWrite': {'title': 'purgeWrite', 'type': 'integer', 'description': 'Integer representing a limit on the number of time directories that are stored by overwriting time directories on a cyclic basis.'}, 'writeFormat': {'type': 'string', 'enum': ['ascii', 'binary'], 'description': 'Specifies the format of the data files.'}, 'writePrecision': {'title': 'writePrecision', 'type': 'integer', 'description': 'Integer used in conjunction with writeFormat described above.'}, 'writeCompression': {'type': 'boolean', 'title': 'writeCompression', 'description': 'Switch to specify whether files are compressed with gzip'}, 'timeFormat': {'type': 'string', 'enum': ['fixed', 'scientific', 'general'], 'description': 'Controls the timing of write output to file.'}, 'timePrecision': {'title': 'timePrecision', 'type': 'integer', 'description': 'Integer used in conjunction with timeFormat described above'}, 'runTimeModifiable': {'type': 'boolean', 'title': 'runTimeModifiable', 'description': 'Switch for whether dictionaries, e.g. controlDict, are re-read during a simulation at the beginning of each time step, allowing the user to modify parameters during a simulation.'}, 'graphFormat': {'type': 'string', 'enum': ['no graph', 'raw', 'gnuplot', 'xmgr', 'jplot'], 'description': 'Format for graph data written by an application.'}, 'adjustTimeStep': {'type': 'boolean', 'title': 'adjustTimeStep', 'description': 'Switch used by some solvers to adjust the time step during the simulation, usually according to maxCo.'}, 'maxCo': {'title': 'maxCo', 'type': 'number', 'description': 'Maximum Courant number.'}, 'interpolate': {'type': 'boolean', 'title': 'interpolate'}, 'libs': {'type': 'array', 'title': 'libs', 'items': {'type': 'string', 'description': 'List of additional libraries (on $LD_LIBRARY_PATH) to be loaded at run-time'}}, 'functions': {'type': 'array', 'title': 'functions', 'items': {'type': 'string', 'description': 'Dictionary of functions, e.g.  probes to be loaded at run-time'}}}}, 'uiSchema': {'listOfStrings': {'items': {'ui:emptyValue': ''}}, 'functions': {'items': {'ui:emptyValue': ''}}}, 'formData': {'application': 'simpleFoam', 'startFrom': 'startTime', 'startTime': 0, 'stopAt': 'endTime', 'endTime': 1000, 'deltaT': 1, 'writeControl': 'timeStep', 'writeInterval': 100, 'purgeWrite': 0, 'writeFormat': 'ascii', 'writePrecision': 7, 'writeCompression': False, 'timeFormat': 'general', 'timePrecision': 6, 'runTimeModifiable': True, 'interpolate': True, 'functions': ['probes.txt']}}}}, 'FvSchemes': {'Execution': {'type': 'jinjaExecuters.jinja', 'input_parameters': {'values': '{WebGui.formData}', 'template': 'openFOAM/simpleFOAM/FvSchemes'}}, 'GUI': {'Type': 'WebGuiNode', 'Properties': {}, 'WebGui': {'Schema': {'type': 'object', 'properties': {'ddtSchemes': {'type': 'object', 'title': 'timeScheme', 'properties': {'default': {'type': 'string', 'enum': ['steadyState', 'Euler', 'backward', 'CrankNicolson', 'localEuler'], 'description': 'The discretisation schemes for each term can be selected from those listed below.'}}}, 'gradSchemes': {'type': 'object', 'title': 'gradSchemes', 'properties': {'default': {'type': 'string', 'title': 'default', 'enum': ['Gauss linear', 'leastSquares', 'Gauss'], 'description': 'The discretisation scheme'}, 'gradU': {'type': 'string', 'title': 'grad(U)', 'description': 'discretisation of velocity gradient terms is overridden to improve boundedness and stability'}, 'gradK': {'type': 'string', 'title': 'grad(k)', 'description': 'discretisation of k gradient terms is overridden to improve boundedness and stability'}, 'gradEpsilon': {'type': 'string', 'title': 'grad(epsilon)', 'description': 'discretisation of epsilon gradient terms is overridden to improve boundedness and stability'}}}, 'divSchemes': {'type': 'object', 'title': 'divSchemes', 'properties': {'default': {'type': 'string', 'title': 'default', 'description': 'contains divergence terms.'}, 'divPhiU': {'type': 'string', 'title': 'div(phi,U)'}, 'divPhiK': {'type': 'string', 'title': 'div(phi,k)'}, 'divPhiEpsilon': {'type': 'string', 'title': 'div(phi,epsilon)'}, 'divPhiE': {'type': 'string', 'title': 'div(phi,e)'}, 'divPhiOmega': {'type': 'string', 'title': 'div(phi,omega)'}, 'moreDivSchemesProperties': {'type': 'object', 'additionalProperties': {'type': 'string'}}}}, 'laplacianSchemes': {'type': 'object', 'title': 'laplacianSchemes', 'description': 'Laplacian terms.', 'properties': {'default': {'type': 'string', 'title': 'default'}}}, 'interpolationSchemes': {'type': 'object', 'title': 'interpolationSchemes', 'description': 'terms that are interpolations of values typically from cell centres to face centres', 'properties': {'default': {'type': 'string', 'title': 'default'}}}, 'snGradSchemes': {'type': 'object', 'title': 'snGradSchemes', 'description': 'contains surface normal gradient terms', 'properties': {'default': {'type': 'string', 'title': 'default'}}}, 'wallDist': {'type': 'object', 'title': 'wallDist', 'properties': {'method': {'type': 'string', 'title': 'method'}}}, 'fluxRequired': {'type': 'object', 'title': 'fluxRequired', 'properties': {'default': {'type': 'string', 'title': 'default'}}}}}, 'uiSchema': {}, 'formData': {'ddtSchemes': {'default': 'steadyState'}, 'gradSchemes': {'default': 'Gauss linear', 'gradU': 'cellLimited Gauss linear 1', 'gradK': 'cellLimited Gauss linear 1', 'gradEpsilon': 'cellLimited Gauss linear 1'}, 'divSchemes': {'moreDivSchemesProperties': {'divNuEff': 'Gauss linear'}, 'default': 'none', 'divPhiU': 'bounded Gauss upwind', 'divPhiK': 'bounded Gauss upwind', 'divPhiEpsilon': 'bounded Gauss upwind', 'divPhiOmega': 'bounded Gauss upwind'}, 'laplacianSchemes': {'default': 'Gauss linear corrected'}, 'interpolationSchemes': {'default': 'linear'}, 'snGradSchemes': {'default': 'corrected'}, 'wallDist': {'method': 'meshWave'}}}}}, 'FileWriter': {'Execution': {'type': 'generalExecuters.FilesWriter', 'input_parameters': {'casePath': 'OpenFOAMfiles/', 'Files': {'system/controlDict': '{ControlDict.output.openFOAMfile}', 'system/fvSchemes': '{FvSchemes.output.openFOAMfile}'}}}, 'GUI': {'Type': 'WebGuiNode', 'Properties': {}, 'WebGui': {}}}, 'finalnode_xx': {'name': 'finalnode_xx', 'Execution': {'type': 'generalExecuters.parameter', 'input_parameters': {}}, 'requires': ['ControlDict', 'FvSchemes', 'FileWriter'], 'GUI': {'TypeFC': {}, 'Properties': {}, 'WebGui': {}}}}}}['workflow']

    def output(self):
        return luigi.LocalTarget("outputsOriginal/FileWriter_0.json")

    def requires(self):
        return dict(
                       FvSchemes=FvSchemes_0(),
                       ControlDict=ControlDict_0()
                   )

    def run(self):
        target = self.output()
        target.makedirs()
        
        task_executer_mapping = {'casePath': 'OpenFOAMfiles/', 'Files': {'system/controlDict': '{ControlDict.output.openFOAMfile}', 'system/fvSchemes': '{FvSchemes.output.openFOAMfile}'}}
        
        parameters_from_required = self.get_all_required_outputs()        
        params = dict(parameters_from_required)
        params['formData']   = {}
        params['files']      = {}
        params['Schema']     = {}
        params['uiSchema']   = {}
        params['Properties'] = {}
        params['WebGui']     = {}
        
       
        executer_parameters = self.build_executer_parameters(task_executer_mapping, params)
        executer_parameters['WD_path']='/home/noga/Noga/FreeCad/github/Hermes/master/Hermes/examples/openFOAM/example_shourt'
                    
        from hermes.Resources.executers.generalExecuters import FilesWriterExecuter  
        output = FilesWriterExecuter(self._taskJSON).run(**executer_parameters)
        
        params['input_parameters'] = executer_parameters 
        params['output'] = output        
        
        out_params = params
        with open(self.output().fn, "w") as outfile:
            json.dump(out_params, outfile)

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
        
        self._workflowJSON = {'workflow': {'root': None, 'Templates': {}, 'nodeList': ['ControlDict', 'FvSchemes', 'FileWriter'], 'nodes': {'ControlDict': {'Execution': {'type': 'jinjaExecuters.jinja', 'input_parameters': {'values': '{WebGui.formData}', 'template': 'openFOAM/simpleFOAM/ControlDict'}}, 'GUI': {'Type': 'WebGuiNode', 'Properties': {}, 'WebGui': {'Schema': {'title': '', 'description': '', 'type': 'object', 'properties': {'application': {'type': 'string', 'title': 'application'}, 'startFrom': {'type': 'string', 'enum': ['firstTime', 'startTime', 'latestTime'], 'description': 'Controls the start time of the simulation.'}, 'startTime': {'title': 'startTime', 'type': 'number', 'description': 'Start time for the simulation with startFrom startTime'}, 'stopAt': {'type': 'string', 'enum': ['endTime', 'writeNow', 'noWriteNow', 'nextwrite'], 'description': 'Controls the end time of the simulation.'}, 'endTime': {'title': 'endTime', 'type': 'number', 'description': 'End time for the simulation when stopAt endTime; is specified.'}, 'deltaT': {'title': 'deltaT', 'type': 'number', 'description': 'Time step of the simulation.'}, 'writeControl': {'type': 'string', 'enum': ['timeStep', 'runTime', 'adjustableRunTime', 'cpuTime', 'clockTime'], 'description': 'Controls the timing of write output to file.'}, 'writeInterval': {'title': 'writeInterval', 'type': 'integer', 'description': 'Scalar used in conjunction with writeControl described above.'}, 'purgeWrite': {'title': 'purgeWrite', 'type': 'integer', 'description': 'Integer representing a limit on the number of time directories that are stored by overwriting time directories on a cyclic basis.'}, 'writeFormat': {'type': 'string', 'enum': ['ascii', 'binary'], 'description': 'Specifies the format of the data files.'}, 'writePrecision': {'title': 'writePrecision', 'type': 'integer', 'description': 'Integer used in conjunction with writeFormat described above.'}, 'writeCompression': {'type': 'boolean', 'title': 'writeCompression', 'description': 'Switch to specify whether files are compressed with gzip'}, 'timeFormat': {'type': 'string', 'enum': ['fixed', 'scientific', 'general'], 'description': 'Controls the timing of write output to file.'}, 'timePrecision': {'title': 'timePrecision', 'type': 'integer', 'description': 'Integer used in conjunction with timeFormat described above'}, 'runTimeModifiable': {'type': 'boolean', 'title': 'runTimeModifiable', 'description': 'Switch for whether dictionaries, e.g. controlDict, are re-read during a simulation at the beginning of each time step, allowing the user to modify parameters during a simulation.'}, 'graphFormat': {'type': 'string', 'enum': ['no graph', 'raw', 'gnuplot', 'xmgr', 'jplot'], 'description': 'Format for graph data written by an application.'}, 'adjustTimeStep': {'type': 'boolean', 'title': 'adjustTimeStep', 'description': 'Switch used by some solvers to adjust the time step during the simulation, usually according to maxCo.'}, 'maxCo': {'title': 'maxCo', 'type': 'number', 'description': 'Maximum Courant number.'}, 'interpolate': {'type': 'boolean', 'title': 'interpolate'}, 'libs': {'type': 'array', 'title': 'libs', 'items': {'type': 'string', 'description': 'List of additional libraries (on $LD_LIBRARY_PATH) to be loaded at run-time'}}, 'functions': {'type': 'array', 'title': 'functions', 'items': {'type': 'string', 'description': 'Dictionary of functions, e.g.  probes to be loaded at run-time'}}}}, 'uiSchema': {'listOfStrings': {'items': {'ui:emptyValue': ''}}, 'functions': {'items': {'ui:emptyValue': ''}}}, 'formData': {'application': 'simpleFoam', 'startFrom': 'startTime', 'startTime': 0, 'stopAt': 'endTime', 'endTime': 1000, 'deltaT': 1, 'writeControl': 'timeStep', 'writeInterval': 100, 'purgeWrite': 0, 'writeFormat': 'ascii', 'writePrecision': 7, 'writeCompression': False, 'timeFormat': 'general', 'timePrecision': 6, 'runTimeModifiable': True, 'interpolate': True, 'functions': ['probes.txt']}}}}, 'FvSchemes': {'Execution': {'type': 'jinjaExecuters.jinja', 'input_parameters': {'values': '{WebGui.formData}', 'template': 'openFOAM/simpleFOAM/FvSchemes'}}, 'GUI': {'Type': 'WebGuiNode', 'Properties': {}, 'WebGui': {'Schema': {'type': 'object', 'properties': {'ddtSchemes': {'type': 'object', 'title': 'timeScheme', 'properties': {'default': {'type': 'string', 'enum': ['steadyState', 'Euler', 'backward', 'CrankNicolson', 'localEuler'], 'description': 'The discretisation schemes for each term can be selected from those listed below.'}}}, 'gradSchemes': {'type': 'object', 'title': 'gradSchemes', 'properties': {'default': {'type': 'string', 'title': 'default', 'enum': ['Gauss linear', 'leastSquares', 'Gauss'], 'description': 'The discretisation scheme'}, 'gradU': {'type': 'string', 'title': 'grad(U)', 'description': 'discretisation of velocity gradient terms is overridden to improve boundedness and stability'}, 'gradK': {'type': 'string', 'title': 'grad(k)', 'description': 'discretisation of k gradient terms is overridden to improve boundedness and stability'}, 'gradEpsilon': {'type': 'string', 'title': 'grad(epsilon)', 'description': 'discretisation of epsilon gradient terms is overridden to improve boundedness and stability'}}}, 'divSchemes': {'type': 'object', 'title': 'divSchemes', 'properties': {'default': {'type': 'string', 'title': 'default', 'description': 'contains divergence terms.'}, 'divPhiU': {'type': 'string', 'title': 'div(phi,U)'}, 'divPhiK': {'type': 'string', 'title': 'div(phi,k)'}, 'divPhiEpsilon': {'type': 'string', 'title': 'div(phi,epsilon)'}, 'divPhiE': {'type': 'string', 'title': 'div(phi,e)'}, 'divPhiOmega': {'type': 'string', 'title': 'div(phi,omega)'}, 'moreDivSchemesProperties': {'type': 'object', 'additionalProperties': {'type': 'string'}}}}, 'laplacianSchemes': {'type': 'object', 'title': 'laplacianSchemes', 'description': 'Laplacian terms.', 'properties': {'default': {'type': 'string', 'title': 'default'}}}, 'interpolationSchemes': {'type': 'object', 'title': 'interpolationSchemes', 'description': 'terms that are interpolations of values typically from cell centres to face centres', 'properties': {'default': {'type': 'string', 'title': 'default'}}}, 'snGradSchemes': {'type': 'object', 'title': 'snGradSchemes', 'description': 'contains surface normal gradient terms', 'properties': {'default': {'type': 'string', 'title': 'default'}}}, 'wallDist': {'type': 'object', 'title': 'wallDist', 'properties': {'method': {'type': 'string', 'title': 'method'}}}, 'fluxRequired': {'type': 'object', 'title': 'fluxRequired', 'properties': {'default': {'type': 'string', 'title': 'default'}}}}}, 'uiSchema': {}, 'formData': {'ddtSchemes': {'default': 'steadyState'}, 'gradSchemes': {'default': 'Gauss linear', 'gradU': 'cellLimited Gauss linear 1', 'gradK': 'cellLimited Gauss linear 1', 'gradEpsilon': 'cellLimited Gauss linear 1'}, 'divSchemes': {'moreDivSchemesProperties': {'divNuEff': 'Gauss linear'}, 'default': 'none', 'divPhiU': 'bounded Gauss upwind', 'divPhiK': 'bounded Gauss upwind', 'divPhiEpsilon': 'bounded Gauss upwind', 'divPhiOmega': 'bounded Gauss upwind'}, 'laplacianSchemes': {'default': 'Gauss linear corrected'}, 'interpolationSchemes': {'default': 'linear'}, 'snGradSchemes': {'default': 'corrected'}, 'wallDist': {'method': 'meshWave'}}}}}, 'FileWriter': {'Execution': {'type': 'generalExecuters.FilesWriter', 'input_parameters': {'casePath': 'OpenFOAMfiles/', 'Files': {'system/controlDict': '{ControlDict.output.openFOAMfile}', 'system/fvSchemes': '{FvSchemes.output.openFOAMfile}'}}}, 'GUI': {'Type': 'WebGuiNode', 'Properties': {}, 'WebGui': {}}}, 'finalnode_xx': {'name': 'finalnode_xx', 'Execution': {'type': 'generalExecuters.parameter', 'input_parameters': {}}, 'requires': ['ControlDict', 'FvSchemes', 'FileWriter'], 'GUI': {'TypeFC': {}, 'Properties': {}, 'WebGui': {}}}}}}['workflow']

    def output(self):
        return luigi.LocalTarget("outputsOriginal/finalnode_xx_0.json")

    def requires(self):
        return dict(
                       FileWriter=FileWriter_0(),
                       FvSchemes=FvSchemes_0(),
                       ControlDict=ControlDict_0()
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
        executer_parameters['WD_path']='/home/noga/Noga/FreeCad/github/Hermes/master/Hermes/examples/openFOAM/example_shourt'
                    
        from hermes.Resources.executers.generalExecuters import parameterExecuter  
        output = parameterExecuter(self._taskJSON).run(**executer_parameters)
        
        params['input_parameters'] = executer_parameters 
        params['output'] = output        
        
        out_params = params
        with open(self.output().fn, "w") as outfile:
            json.dump(out_params, outfile)
