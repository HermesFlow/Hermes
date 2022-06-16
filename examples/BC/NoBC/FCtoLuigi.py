

import shutil
import os
import luigi
import json 
import sys

sys.path.insert(1, "/mnt/build")
from hermes.engines.luigi.taskUtils import utils as hermesutils

class GeometryDefiner_0(luigi.Task,hermesutils):

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
        
        self._workflowJSON = {'workflow': {'root': None, 'Templates': [], 'nodeList': ['BlockMesh', 'GeometryDefiner', 'ControlDict'], 'nodes': {'BlockMesh': {'Execution': {'type': 'jinjaExecuters.BlockMesh', 'input_parameters': {'Properties': '{value.Properties}', 'boundary': '{value.boundary}', 'vertices': '{value.vertices}', 'template': 'openFOAM/simpleFOAM/BlockMesh'}}, 'GUI': {'Type': 'BlockMeshNode', 'Properties': {'Property01': {'prop': 'partName', 'init_val': '', 'type': 'App::PropertyString', 'Heading': 'BasicData', 'tooltip': 'Name of tha part of the blockMesh node ', 'current_val': 'Box'}, 'Property02': {'prop': 'partPath', 'init_val': '', 'type': 'App::PropertyPath', 'Heading': 'BasicData', 'tooltip': 'Path to tha part of the blockMesh node ', 'current_val': ''}, 'Property03': {'prop': 'convertToMeters', 'init_val': 1, 'type': 'App::PropertyFloat', 'Heading': 'BasicData', 'tooltip': 'Link a part to the blockMesh node ', 'current_val': 1.0}, 'Property04': {'prop': 'NumberOfCells', 'init_val': '1 2 3', 'type': 'App::PropertyString', 'Heading': 'Block', 'tooltip': 'Numbers of cells in each direction ', 'current_val': '1 2 3'}, 'Property05': {'prop': 'simpleGradingX', 'init_val': ['1'], 'type': 'App::PropertyStringList', 'Heading': 'Block', 'tooltip': 'simpleGrading in x direction ', 'current_val': ['1']}, 'Property06': {'prop': 'simpleGradingY', 'init_val': ['1'], 'type': 'App::PropertyStringList', 'Heading': 'Block', 'tooltip': 'simpleGrading in y direction ', 'current_val': ['0.2 0.3 4', '0.6 0.4 1', '0.2 0.3 0.25']}, 'Property07': {'prop': 'simpleGradingZ', 'init_val': ['1'], 'type': 'App::PropertyStringList', 'Heading': 'Block', 'tooltip': 'simpleGrading in z direction ', 'current_val': ['1']}}, 'GeometryFaceTypes': {'TypeList': ['wall', 'symmetry', 'patch', 'cyclic'], 'TypeProperties': {'wall': {'Properties': {}}, 'symmetry': {'Properties': {}}, 'patch': {'Properties': {}}, 'cyclic': {'Properties': {'Property01': {'prop': 'neighbourPatch', 'init_val': ['notSet'], 'type': 'App::PropertyEnumeration', 'Heading': 'Neighbour', 'tooltip': 'Neight face name', 'current_val': 'a'}}}}}, 'boundary': [{'Name': 'wall', 'Type': 'wall', 'Properties': {}, 'faces': {'Face6': {'vertices': '4 5 6 7'}}}, {'Name': 'a', 'Type': 'cyclic', 'Properties': {'Property01': {'prop': 'neighbourPatch', 'init_val': ['notSet'], 'type': 'App::PropertyEnumeration', 'Heading': 'Neighbour', 'tooltip': 'Neight face name', 'current_val': 'b'}}, 'faces': {'Face1': {'vertices': '0 4 7 3'}}}, {'Name': 'b', 'Type': 'cyclic', 'Properties': {'Property01': {'prop': 'neighbourPatch', 'init_val': ['notSet'], 'type': 'App::PropertyEnumeration', 'Heading': 'Neighbour', 'tooltip': 'Neight face name', 'current_val': 'a'}}, 'faces': {'Face2': {'vertices': '1 2 6 5'}}}], 'vertices': ['0.0 0.0 0.0 ', '11.0 0.0 0.0 ', '11.0 12.0 0.0 ', '0.0 12.0 0.0 ', '0.0 0.0 13.0 ', '11.0 0.0 13.0 ', '11.0 12.0 13.0 ', '0.0 12.0 13.0 ']}}, 'GeometryDefiner': {'Execution': {'type': 'jinjaExecuters.GeometryDefiner', 'input_parameters': {}}, 'GUI': {'Type': 'GeometryDefinerNode', 'Properties': {'Property1': {'prop': 'IntegerProperty', 'init_val': 10, 'type': 'App::PropertyInteger', 'Heading': 'PropInteger', 'tooltip': 'IntegerProperty', 'current_val': 10}}, 'GeometryFaceTypes': {'TypeList': ['wall', 'symmetry', 'patch', 'boundarylayer'], 'TypeProperties': {'wall': {'Properties': {'Property01': {'prop': 'Ux', 'init_val': '0 m/s', 'type': 'App::PropertySpeed', 'Heading': 'Velocity', 'tooltip': 'Velocity in x direction ', 'current_val': '0 m/s'}, 'Property02': {'prop': 'Uy', 'init_val': '0 m/s', 'type': 'App::PropertySpeed', 'Heading': 'Velocity', 'tooltip': 'Velocity in y direction', 'current_val': '0 m/s'}}}, 'symmetry': {'Properties': {'Property01': {'prop': 'P0', 'init_val': '10 Pa', 'type': 'App::PropertyPressure', 'Heading': 'Pressure', 'tooltip': 'Total Pressure ', 'current_val': '11 Pa'}}}, 'patch': {'Properties': {'Property01': {'prop': 'P0', 'init_val': '10 Pa', 'type': 'App::PropertyPressure', 'Heading': 'Pressure', 'tooltip': 'Total Pressure ', 'current_val': '12 Pa'}}}, 'boundarylayer': {'Properties': {'Property01': {'prop': 'P0', 'init_val': '10 Pa', 'type': 'App::PropertyPressure', 'Heading': 'Pressure', 'tooltip': 'Total Pressure ', 'current_val': '13 Pa'}}}}}, 'GeometryEntityList': {}}}, 'ControlDict': {'Execution': {'type': 'jinjaExecuters.jinja', 'input_parameters': {'values': '{WebGui.formData}', 'template': 'openFOAM/simpleFOAM/ControlDict'}}, 'GUI': {'Type': 'WebGuiNode', 'Properties': {}, 'WebGui': {'Schema': {'title': '', 'description': '', 'type': 'object', 'properties': {'application': {'type': 'string', 'title': 'application'}, 'startFrom': {'type': 'string', 'enum': ['firstTime', 'startTime', 'latestTime'], 'description': 'Controls the start time of the simulation.'}, 'startTime': {'title': 'startTime', 'type': 'number', 'description': 'Start time for the simulation with startFrom startTime'}, 'stopAt': {'type': 'string', 'enum': ['endTime', 'writeNow', 'noWriteNow', 'nextwrite'], 'description': 'Controls the end time of the simulation.'}, 'endTime': {'title': 'endTime', 'type': 'number', 'description': 'End time for the simulation when stopAt endTime; is specified.'}, 'deltaT': {'title': 'deltaT', 'type': 'number', 'description': 'Time step of the simulation.'}, 'writeControl': {'type': 'string', 'enum': ['timeStep', 'runTime', 'adjustableRunTime', 'cpuTime', 'clockTime'], 'description': 'Controls the timing of write output to file.'}, 'writeInterval': {'title': 'writeInterval', 'type': 'integer', 'description': 'Scalar used in conjunction with writeControl described above.'}, 'purgeWrite': {'title': 'purgeWrite', 'type': 'integer', 'description': 'Integer representing a limit on the number of time directories that are stored by overwriting time directories on a cyclic basis.'}, 'writeFormat': {'type': 'string', 'enum': ['ascii', 'binary'], 'description': 'Specifies the format of the data files.'}, 'writePrecision': {'title': 'writePrecision', 'type': 'integer', 'description': 'Integer used in conjunction with writeFormat described above.'}, 'writeCompression': {'type': 'boolean', 'title': 'writeCompression', 'description': 'Switch to specify whether files are compressed with gzip'}, 'timeFormat': {'type': 'string', 'enum': ['fixed', 'scientific', 'general'], 'description': 'Controls the timing of write output to file.'}, 'timePrecision': {'title': 'timePrecision', 'type': 'integer', 'description': 'Integer used in conjunction with timeFormat described above'}, 'runTimeModifiable': {'type': 'boolean', 'title': 'runTimeModifiable', 'description': 'Switch for whether dictionaries, e.g. controlDict, are re-read during a simulation at the beginning of each time step, allowing the user to modify parameters during a simulation.'}, 'graphFormat': {'type': 'string', 'enum': ['no graph', 'raw', 'gnuplot', 'xmgr', 'jplot'], 'description': 'Format for graph data written by an application.'}, 'adjustTimeStep': {'type': 'boolean', 'title': 'adjustTimeStep', 'description': 'Switch used by some solvers to adjust the time step during the simulation, usually according to maxCo.'}, 'maxCo': {'title': 'maxCo', 'type': 'number', 'description': 'Maximum Courant number.'}, 'interpolate': {'type': 'boolean', 'title': 'interpolate'}, 'libs': {'type': 'array', 'title': 'libs', 'items': {'type': 'string', 'description': 'List of additional libraries (on $LD_LIBRARY_PATH) to be loaded at run-time'}}, 'functions': {'type': 'array', 'title': 'functions', 'items': {'type': 'string', 'description': 'Dictionary of functions, e.g.  probes to be loaded at run-time'}}}}, 'uiSchema': {'listOfStrings': {'items': {'ui:emptyValue': ''}}, 'functions': {'items': {'ui:emptyValue': ''}}}, 'formData': {'application': 'simpleFoam', 'startFrom': 'startTime', 'startTime': 0, 'stopAt': 'endTime', 'endTime': 1000, 'deltaT': 1, 'writeControl': 'timeStep', 'writeInterval': 100, 'purgeWrite': 0, 'writeFormat': 'ascii', 'writePrecision': 7, 'writeCompression': 'false', 'timeFormat': 'general', 'timePrecision': 6, 'runTimeModifiable': 'true', 'interpolate': 'true', 'functions': []}}}}, 'finalnode_xx': {'name': 'finalnode_xx', 'Execution': {'type': 'generalExecuters.parameter', 'input_parameters': {}}, 'requires': ['BlockMesh', 'GeometryDefiner', 'ControlDict'], 'GUI': {'TypeFC': {}, 'Properties': {}, 'WebGui': {}}}}}}['workflow']

    def output(self):
        return luigi.LocalTarget("outputsOriginal/GeometryDefiner_0.json")

    def requires(self):
        return dict(
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
        params['Properties'] = {'Property1': {'prop': 'IntegerProperty', 'init_val': 10, 'type': 'App::PropertyInteger', 'Heading': 'PropInteger', 'tooltip': 'IntegerProperty', 'current_val': 10}}
        params['WebGui']     = {}
        
       
        executer_parameters = self.build_executer_parameters(task_executer_mapping, params)
        executer_parameters['WD_path']='/mnt/examples/BC/NoBC'
                    
        from hermes.Resources.executers.jinjaExecuters import GeometryDefinerExecuter  
        output = GeometryDefinerExecuter(self._taskJSON).run(**executer_parameters)
        
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
        
        self._workflowJSON = {'workflow': {'root': None, 'Templates': [], 'nodeList': ['BlockMesh', 'GeometryDefiner', 'ControlDict'], 'nodes': {'BlockMesh': {'Execution': {'type': 'jinjaExecuters.BlockMesh', 'input_parameters': {'Properties': '{value.Properties}', 'boundary': '{value.boundary}', 'vertices': '{value.vertices}', 'template': 'openFOAM/simpleFOAM/BlockMesh'}}, 'GUI': {'Type': 'BlockMeshNode', 'Properties': {'Property01': {'prop': 'partName', 'init_val': '', 'type': 'App::PropertyString', 'Heading': 'BasicData', 'tooltip': 'Name of tha part of the blockMesh node ', 'current_val': 'Box'}, 'Property02': {'prop': 'partPath', 'init_val': '', 'type': 'App::PropertyPath', 'Heading': 'BasicData', 'tooltip': 'Path to tha part of the blockMesh node ', 'current_val': ''}, 'Property03': {'prop': 'convertToMeters', 'init_val': 1, 'type': 'App::PropertyFloat', 'Heading': 'BasicData', 'tooltip': 'Link a part to the blockMesh node ', 'current_val': 1.0}, 'Property04': {'prop': 'NumberOfCells', 'init_val': '1 2 3', 'type': 'App::PropertyString', 'Heading': 'Block', 'tooltip': 'Numbers of cells in each direction ', 'current_val': '1 2 3'}, 'Property05': {'prop': 'simpleGradingX', 'init_val': ['1'], 'type': 'App::PropertyStringList', 'Heading': 'Block', 'tooltip': 'simpleGrading in x direction ', 'current_val': ['1']}, 'Property06': {'prop': 'simpleGradingY', 'init_val': ['1'], 'type': 'App::PropertyStringList', 'Heading': 'Block', 'tooltip': 'simpleGrading in y direction ', 'current_val': ['0.2 0.3 4', '0.6 0.4 1', '0.2 0.3 0.25']}, 'Property07': {'prop': 'simpleGradingZ', 'init_val': ['1'], 'type': 'App::PropertyStringList', 'Heading': 'Block', 'tooltip': 'simpleGrading in z direction ', 'current_val': ['1']}}, 'GeometryFaceTypes': {'TypeList': ['wall', 'symmetry', 'patch', 'cyclic'], 'TypeProperties': {'wall': {'Properties': {}}, 'symmetry': {'Properties': {}}, 'patch': {'Properties': {}}, 'cyclic': {'Properties': {'Property01': {'prop': 'neighbourPatch', 'init_val': ['notSet'], 'type': 'App::PropertyEnumeration', 'Heading': 'Neighbour', 'tooltip': 'Neight face name', 'current_val': 'a'}}}}}, 'boundary': [{'Name': 'wall', 'Type': 'wall', 'Properties': {}, 'faces': {'Face6': {'vertices': '4 5 6 7'}}}, {'Name': 'a', 'Type': 'cyclic', 'Properties': {'Property01': {'prop': 'neighbourPatch', 'init_val': ['notSet'], 'type': 'App::PropertyEnumeration', 'Heading': 'Neighbour', 'tooltip': 'Neight face name', 'current_val': 'b'}}, 'faces': {'Face1': {'vertices': '0 4 7 3'}}}, {'Name': 'b', 'Type': 'cyclic', 'Properties': {'Property01': {'prop': 'neighbourPatch', 'init_val': ['notSet'], 'type': 'App::PropertyEnumeration', 'Heading': 'Neighbour', 'tooltip': 'Neight face name', 'current_val': 'a'}}, 'faces': {'Face2': {'vertices': '1 2 6 5'}}}], 'vertices': ['0.0 0.0 0.0 ', '11.0 0.0 0.0 ', '11.0 12.0 0.0 ', '0.0 12.0 0.0 ', '0.0 0.0 13.0 ', '11.0 0.0 13.0 ', '11.0 12.0 13.0 ', '0.0 12.0 13.0 ']}}, 'GeometryDefiner': {'Execution': {'type': 'jinjaExecuters.GeometryDefiner', 'input_parameters': {}}, 'GUI': {'Type': 'GeometryDefinerNode', 'Properties': {'Property1': {'prop': 'IntegerProperty', 'init_val': 10, 'type': 'App::PropertyInteger', 'Heading': 'PropInteger', 'tooltip': 'IntegerProperty', 'current_val': 10}}, 'GeometryFaceTypes': {'TypeList': ['wall', 'symmetry', 'patch', 'boundarylayer'], 'TypeProperties': {'wall': {'Properties': {'Property01': {'prop': 'Ux', 'init_val': '0 m/s', 'type': 'App::PropertySpeed', 'Heading': 'Velocity', 'tooltip': 'Velocity in x direction ', 'current_val': '0 m/s'}, 'Property02': {'prop': 'Uy', 'init_val': '0 m/s', 'type': 'App::PropertySpeed', 'Heading': 'Velocity', 'tooltip': 'Velocity in y direction', 'current_val': '0 m/s'}}}, 'symmetry': {'Properties': {'Property01': {'prop': 'P0', 'init_val': '10 Pa', 'type': 'App::PropertyPressure', 'Heading': 'Pressure', 'tooltip': 'Total Pressure ', 'current_val': '11 Pa'}}}, 'patch': {'Properties': {'Property01': {'prop': 'P0', 'init_val': '10 Pa', 'type': 'App::PropertyPressure', 'Heading': 'Pressure', 'tooltip': 'Total Pressure ', 'current_val': '12 Pa'}}}, 'boundarylayer': {'Properties': {'Property01': {'prop': 'P0', 'init_val': '10 Pa', 'type': 'App::PropertyPressure', 'Heading': 'Pressure', 'tooltip': 'Total Pressure ', 'current_val': '13 Pa'}}}}}, 'GeometryEntityList': {}}}, 'ControlDict': {'Execution': {'type': 'jinjaExecuters.jinja', 'input_parameters': {'values': '{WebGui.formData}', 'template': 'openFOAM/simpleFOAM/ControlDict'}}, 'GUI': {'Type': 'WebGuiNode', 'Properties': {}, 'WebGui': {'Schema': {'title': '', 'description': '', 'type': 'object', 'properties': {'application': {'type': 'string', 'title': 'application'}, 'startFrom': {'type': 'string', 'enum': ['firstTime', 'startTime', 'latestTime'], 'description': 'Controls the start time of the simulation.'}, 'startTime': {'title': 'startTime', 'type': 'number', 'description': 'Start time for the simulation with startFrom startTime'}, 'stopAt': {'type': 'string', 'enum': ['endTime', 'writeNow', 'noWriteNow', 'nextwrite'], 'description': 'Controls the end time of the simulation.'}, 'endTime': {'title': 'endTime', 'type': 'number', 'description': 'End time for the simulation when stopAt endTime; is specified.'}, 'deltaT': {'title': 'deltaT', 'type': 'number', 'description': 'Time step of the simulation.'}, 'writeControl': {'type': 'string', 'enum': ['timeStep', 'runTime', 'adjustableRunTime', 'cpuTime', 'clockTime'], 'description': 'Controls the timing of write output to file.'}, 'writeInterval': {'title': 'writeInterval', 'type': 'integer', 'description': 'Scalar used in conjunction with writeControl described above.'}, 'purgeWrite': {'title': 'purgeWrite', 'type': 'integer', 'description': 'Integer representing a limit on the number of time directories that are stored by overwriting time directories on a cyclic basis.'}, 'writeFormat': {'type': 'string', 'enum': ['ascii', 'binary'], 'description': 'Specifies the format of the data files.'}, 'writePrecision': {'title': 'writePrecision', 'type': 'integer', 'description': 'Integer used in conjunction with writeFormat described above.'}, 'writeCompression': {'type': 'boolean', 'title': 'writeCompression', 'description': 'Switch to specify whether files are compressed with gzip'}, 'timeFormat': {'type': 'string', 'enum': ['fixed', 'scientific', 'general'], 'description': 'Controls the timing of write output to file.'}, 'timePrecision': {'title': 'timePrecision', 'type': 'integer', 'description': 'Integer used in conjunction with timeFormat described above'}, 'runTimeModifiable': {'type': 'boolean', 'title': 'runTimeModifiable', 'description': 'Switch for whether dictionaries, e.g. controlDict, are re-read during a simulation at the beginning of each time step, allowing the user to modify parameters during a simulation.'}, 'graphFormat': {'type': 'string', 'enum': ['no graph', 'raw', 'gnuplot', 'xmgr', 'jplot'], 'description': 'Format for graph data written by an application.'}, 'adjustTimeStep': {'type': 'boolean', 'title': 'adjustTimeStep', 'description': 'Switch used by some solvers to adjust the time step during the simulation, usually according to maxCo.'}, 'maxCo': {'title': 'maxCo', 'type': 'number', 'description': 'Maximum Courant number.'}, 'interpolate': {'type': 'boolean', 'title': 'interpolate'}, 'libs': {'type': 'array', 'title': 'libs', 'items': {'type': 'string', 'description': 'List of additional libraries (on $LD_LIBRARY_PATH) to be loaded at run-time'}}, 'functions': {'type': 'array', 'title': 'functions', 'items': {'type': 'string', 'description': 'Dictionary of functions, e.g.  probes to be loaded at run-time'}}}}, 'uiSchema': {'listOfStrings': {'items': {'ui:emptyValue': ''}}, 'functions': {'items': {'ui:emptyValue': ''}}}, 'formData': {'application': 'simpleFoam', 'startFrom': 'startTime', 'startTime': 0, 'stopAt': 'endTime', 'endTime': 1000, 'deltaT': 1, 'writeControl': 'timeStep', 'writeInterval': 100, 'purgeWrite': 0, 'writeFormat': 'ascii', 'writePrecision': 7, 'writeCompression': 'false', 'timeFormat': 'general', 'timePrecision': 6, 'runTimeModifiable': 'true', 'interpolate': 'true', 'functions': []}}}}, 'finalnode_xx': {'name': 'finalnode_xx', 'Execution': {'type': 'generalExecuters.parameter', 'input_parameters': {}}, 'requires': ['BlockMesh', 'GeometryDefiner', 'ControlDict'], 'GUI': {'TypeFC': {}, 'Properties': {}, 'WebGui': {}}}}}}['workflow']

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
        params['WebGui']     = {'Schema': {'title': '', 'description': '', 'type': 'object', 'properties': {'application': {'type': 'string', 'title': 'application'}, 'startFrom': {'type': 'string', 'enum': ['firstTime', 'startTime', 'latestTime'], 'description': 'Controls the start time of the simulation.'}, 'startTime': {'title': 'startTime', 'type': 'number', 'description': 'Start time for the simulation with startFrom startTime'}, 'stopAt': {'type': 'string', 'enum': ['endTime', 'writeNow', 'noWriteNow', 'nextwrite'], 'description': 'Controls the end time of the simulation.'}, 'endTime': {'title': 'endTime', 'type': 'number', 'description': 'End time for the simulation when stopAt endTime; is specified.'}, 'deltaT': {'title': 'deltaT', 'type': 'number', 'description': 'Time step of the simulation.'}, 'writeControl': {'type': 'string', 'enum': ['timeStep', 'runTime', 'adjustableRunTime', 'cpuTime', 'clockTime'], 'description': 'Controls the timing of write output to file.'}, 'writeInterval': {'title': 'writeInterval', 'type': 'integer', 'description': 'Scalar used in conjunction with writeControl described above.'}, 'purgeWrite': {'title': 'purgeWrite', 'type': 'integer', 'description': 'Integer representing a limit on the number of time directories that are stored by overwriting time directories on a cyclic basis.'}, 'writeFormat': {'type': 'string', 'enum': ['ascii', 'binary'], 'description': 'Specifies the format of the data files.'}, 'writePrecision': {'title': 'writePrecision', 'type': 'integer', 'description': 'Integer used in conjunction with writeFormat described above.'}, 'writeCompression': {'type': 'boolean', 'title': 'writeCompression', 'description': 'Switch to specify whether files are compressed with gzip'}, 'timeFormat': {'type': 'string', 'enum': ['fixed', 'scientific', 'general'], 'description': 'Controls the timing of write output to file.'}, 'timePrecision': {'title': 'timePrecision', 'type': 'integer', 'description': 'Integer used in conjunction with timeFormat described above'}, 'runTimeModifiable': {'type': 'boolean', 'title': 'runTimeModifiable', 'description': 'Switch for whether dictionaries, e.g. controlDict, are re-read during a simulation at the beginning of each time step, allowing the user to modify parameters during a simulation.'}, 'graphFormat': {'type': 'string', 'enum': ['no graph', 'raw', 'gnuplot', 'xmgr', 'jplot'], 'description': 'Format for graph data written by an application.'}, 'adjustTimeStep': {'type': 'boolean', 'title': 'adjustTimeStep', 'description': 'Switch used by some solvers to adjust the time step during the simulation, usually according to maxCo.'}, 'maxCo': {'title': 'maxCo', 'type': 'number', 'description': 'Maximum Courant number.'}, 'interpolate': {'type': 'boolean', 'title': 'interpolate'}, 'libs': {'type': 'array', 'title': 'libs', 'items': {'type': 'string', 'description': 'List of additional libraries (on $LD_LIBRARY_PATH) to be loaded at run-time'}}, 'functions': {'type': 'array', 'title': 'functions', 'items': {'type': 'string', 'description': 'Dictionary of functions, e.g.  probes to be loaded at run-time'}}}}, 'uiSchema': {'listOfStrings': {'items': {'ui:emptyValue': ''}}, 'functions': {'items': {'ui:emptyValue': ''}}}, 'formData': {'application': 'simpleFoam', 'startFrom': 'startTime', 'startTime': 0, 'stopAt': 'endTime', 'endTime': 1000, 'deltaT': 1, 'writeControl': 'timeStep', 'writeInterval': 100, 'purgeWrite': 0, 'writeFormat': 'ascii', 'writePrecision': 7, 'writeCompression': 'false', 'timeFormat': 'general', 'timePrecision': 6, 'runTimeModifiable': 'true', 'interpolate': 'true', 'functions': []}}
        
       
        executer_parameters = self.build_executer_parameters(task_executer_mapping, params)
        executer_parameters['WD_path']='/mnt/examples/BC/NoBC'
                    
        from hermes.Resources.executers.jinjaExecuters import jinjaExecuter  
        output = jinjaExecuter(self._taskJSON).run(**executer_parameters)
        
        params['input_parameters'] = executer_parameters 
        params['output'] = output        
        
        out_params = params
        with open(self.output().fn, "w") as outfile:
            json.dump(out_params, outfile)

class BlockMesh_0(luigi.Task,hermesutils):

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
        
        self._workflowJSON = {'workflow': {'root': None, 'Templates': [], 'nodeList': ['BlockMesh', 'GeometryDefiner', 'ControlDict'], 'nodes': {'BlockMesh': {'Execution': {'type': 'jinjaExecuters.BlockMesh', 'input_parameters': {'Properties': '{value.Properties}', 'boundary': '{value.boundary}', 'vertices': '{value.vertices}', 'template': 'openFOAM/simpleFOAM/BlockMesh'}}, 'GUI': {'Type': 'BlockMeshNode', 'Properties': {'Property01': {'prop': 'partName', 'init_val': '', 'type': 'App::PropertyString', 'Heading': 'BasicData', 'tooltip': 'Name of tha part of the blockMesh node ', 'current_val': 'Box'}, 'Property02': {'prop': 'partPath', 'init_val': '', 'type': 'App::PropertyPath', 'Heading': 'BasicData', 'tooltip': 'Path to tha part of the blockMesh node ', 'current_val': ''}, 'Property03': {'prop': 'convertToMeters', 'init_val': 1, 'type': 'App::PropertyFloat', 'Heading': 'BasicData', 'tooltip': 'Link a part to the blockMesh node ', 'current_val': 1.0}, 'Property04': {'prop': 'NumberOfCells', 'init_val': '1 2 3', 'type': 'App::PropertyString', 'Heading': 'Block', 'tooltip': 'Numbers of cells in each direction ', 'current_val': '1 2 3'}, 'Property05': {'prop': 'simpleGradingX', 'init_val': ['1'], 'type': 'App::PropertyStringList', 'Heading': 'Block', 'tooltip': 'simpleGrading in x direction ', 'current_val': ['1']}, 'Property06': {'prop': 'simpleGradingY', 'init_val': ['1'], 'type': 'App::PropertyStringList', 'Heading': 'Block', 'tooltip': 'simpleGrading in y direction ', 'current_val': ['0.2 0.3 4', '0.6 0.4 1', '0.2 0.3 0.25']}, 'Property07': {'prop': 'simpleGradingZ', 'init_val': ['1'], 'type': 'App::PropertyStringList', 'Heading': 'Block', 'tooltip': 'simpleGrading in z direction ', 'current_val': ['1']}}, 'GeometryFaceTypes': {'TypeList': ['wall', 'symmetry', 'patch', 'cyclic'], 'TypeProperties': {'wall': {'Properties': {}}, 'symmetry': {'Properties': {}}, 'patch': {'Properties': {}}, 'cyclic': {'Properties': {'Property01': {'prop': 'neighbourPatch', 'init_val': ['notSet'], 'type': 'App::PropertyEnumeration', 'Heading': 'Neighbour', 'tooltip': 'Neight face name', 'current_val': 'a'}}}}}, 'boundary': [{'Name': 'wall', 'Type': 'wall', 'Properties': {}, 'faces': {'Face6': {'vertices': '4 5 6 7'}}}, {'Name': 'a', 'Type': 'cyclic', 'Properties': {'Property01': {'prop': 'neighbourPatch', 'init_val': ['notSet'], 'type': 'App::PropertyEnumeration', 'Heading': 'Neighbour', 'tooltip': 'Neight face name', 'current_val': 'b'}}, 'faces': {'Face1': {'vertices': '0 4 7 3'}}}, {'Name': 'b', 'Type': 'cyclic', 'Properties': {'Property01': {'prop': 'neighbourPatch', 'init_val': ['notSet'], 'type': 'App::PropertyEnumeration', 'Heading': 'Neighbour', 'tooltip': 'Neight face name', 'current_val': 'a'}}, 'faces': {'Face2': {'vertices': '1 2 6 5'}}}], 'vertices': ['0.0 0.0 0.0 ', '11.0 0.0 0.0 ', '11.0 12.0 0.0 ', '0.0 12.0 0.0 ', '0.0 0.0 13.0 ', '11.0 0.0 13.0 ', '11.0 12.0 13.0 ', '0.0 12.0 13.0 ']}}, 'GeometryDefiner': {'Execution': {'type': 'jinjaExecuters.GeometryDefiner', 'input_parameters': {}}, 'GUI': {'Type': 'GeometryDefinerNode', 'Properties': {'Property1': {'prop': 'IntegerProperty', 'init_val': 10, 'type': 'App::PropertyInteger', 'Heading': 'PropInteger', 'tooltip': 'IntegerProperty', 'current_val': 10}}, 'GeometryFaceTypes': {'TypeList': ['wall', 'symmetry', 'patch', 'boundarylayer'], 'TypeProperties': {'wall': {'Properties': {'Property01': {'prop': 'Ux', 'init_val': '0 m/s', 'type': 'App::PropertySpeed', 'Heading': 'Velocity', 'tooltip': 'Velocity in x direction ', 'current_val': '0 m/s'}, 'Property02': {'prop': 'Uy', 'init_val': '0 m/s', 'type': 'App::PropertySpeed', 'Heading': 'Velocity', 'tooltip': 'Velocity in y direction', 'current_val': '0 m/s'}}}, 'symmetry': {'Properties': {'Property01': {'prop': 'P0', 'init_val': '10 Pa', 'type': 'App::PropertyPressure', 'Heading': 'Pressure', 'tooltip': 'Total Pressure ', 'current_val': '11 Pa'}}}, 'patch': {'Properties': {'Property01': {'prop': 'P0', 'init_val': '10 Pa', 'type': 'App::PropertyPressure', 'Heading': 'Pressure', 'tooltip': 'Total Pressure ', 'current_val': '12 Pa'}}}, 'boundarylayer': {'Properties': {'Property01': {'prop': 'P0', 'init_val': '10 Pa', 'type': 'App::PropertyPressure', 'Heading': 'Pressure', 'tooltip': 'Total Pressure ', 'current_val': '13 Pa'}}}}}, 'GeometryEntityList': {}}}, 'ControlDict': {'Execution': {'type': 'jinjaExecuters.jinja', 'input_parameters': {'values': '{WebGui.formData}', 'template': 'openFOAM/simpleFOAM/ControlDict'}}, 'GUI': {'Type': 'WebGuiNode', 'Properties': {}, 'WebGui': {'Schema': {'title': '', 'description': '', 'type': 'object', 'properties': {'application': {'type': 'string', 'title': 'application'}, 'startFrom': {'type': 'string', 'enum': ['firstTime', 'startTime', 'latestTime'], 'description': 'Controls the start time of the simulation.'}, 'startTime': {'title': 'startTime', 'type': 'number', 'description': 'Start time for the simulation with startFrom startTime'}, 'stopAt': {'type': 'string', 'enum': ['endTime', 'writeNow', 'noWriteNow', 'nextwrite'], 'description': 'Controls the end time of the simulation.'}, 'endTime': {'title': 'endTime', 'type': 'number', 'description': 'End time for the simulation when stopAt endTime; is specified.'}, 'deltaT': {'title': 'deltaT', 'type': 'number', 'description': 'Time step of the simulation.'}, 'writeControl': {'type': 'string', 'enum': ['timeStep', 'runTime', 'adjustableRunTime', 'cpuTime', 'clockTime'], 'description': 'Controls the timing of write output to file.'}, 'writeInterval': {'title': 'writeInterval', 'type': 'integer', 'description': 'Scalar used in conjunction with writeControl described above.'}, 'purgeWrite': {'title': 'purgeWrite', 'type': 'integer', 'description': 'Integer representing a limit on the number of time directories that are stored by overwriting time directories on a cyclic basis.'}, 'writeFormat': {'type': 'string', 'enum': ['ascii', 'binary'], 'description': 'Specifies the format of the data files.'}, 'writePrecision': {'title': 'writePrecision', 'type': 'integer', 'description': 'Integer used in conjunction with writeFormat described above.'}, 'writeCompression': {'type': 'boolean', 'title': 'writeCompression', 'description': 'Switch to specify whether files are compressed with gzip'}, 'timeFormat': {'type': 'string', 'enum': ['fixed', 'scientific', 'general'], 'description': 'Controls the timing of write output to file.'}, 'timePrecision': {'title': 'timePrecision', 'type': 'integer', 'description': 'Integer used in conjunction with timeFormat described above'}, 'runTimeModifiable': {'type': 'boolean', 'title': 'runTimeModifiable', 'description': 'Switch for whether dictionaries, e.g. controlDict, are re-read during a simulation at the beginning of each time step, allowing the user to modify parameters during a simulation.'}, 'graphFormat': {'type': 'string', 'enum': ['no graph', 'raw', 'gnuplot', 'xmgr', 'jplot'], 'description': 'Format for graph data written by an application.'}, 'adjustTimeStep': {'type': 'boolean', 'title': 'adjustTimeStep', 'description': 'Switch used by some solvers to adjust the time step during the simulation, usually according to maxCo.'}, 'maxCo': {'title': 'maxCo', 'type': 'number', 'description': 'Maximum Courant number.'}, 'interpolate': {'type': 'boolean', 'title': 'interpolate'}, 'libs': {'type': 'array', 'title': 'libs', 'items': {'type': 'string', 'description': 'List of additional libraries (on $LD_LIBRARY_PATH) to be loaded at run-time'}}, 'functions': {'type': 'array', 'title': 'functions', 'items': {'type': 'string', 'description': 'Dictionary of functions, e.g.  probes to be loaded at run-time'}}}}, 'uiSchema': {'listOfStrings': {'items': {'ui:emptyValue': ''}}, 'functions': {'items': {'ui:emptyValue': ''}}}, 'formData': {'application': 'simpleFoam', 'startFrom': 'startTime', 'startTime': 0, 'stopAt': 'endTime', 'endTime': 1000, 'deltaT': 1, 'writeControl': 'timeStep', 'writeInterval': 100, 'purgeWrite': 0, 'writeFormat': 'ascii', 'writePrecision': 7, 'writeCompression': 'false', 'timeFormat': 'general', 'timePrecision': 6, 'runTimeModifiable': 'true', 'interpolate': 'true', 'functions': []}}}}, 'finalnode_xx': {'name': 'finalnode_xx', 'Execution': {'type': 'generalExecuters.parameter', 'input_parameters': {}}, 'requires': ['BlockMesh', 'GeometryDefiner', 'ControlDict'], 'GUI': {'TypeFC': {}, 'Properties': {}, 'WebGui': {}}}}}}['workflow']

    def output(self):
        return luigi.LocalTarget("outputsOriginal/BlockMesh_0.json")

    def requires(self):
        return dict(
                   )

    def run(self):
        target = self.output()
        target.makedirs()
        
        task_executer_mapping = {'Properties': '{value.Properties}', 'boundary': '{value.boundary}', 'vertices': '{value.vertices}', 'template': 'openFOAM/simpleFOAM/BlockMesh'}
        
        parameters_from_required = self.get_all_required_outputs()        
        params = dict(parameters_from_required)
        params['formData']   = {}
        params['files']      = {}
        params['Schema']     = {}
        params['uiSchema']   = {}
        params['Properties'] = {'Property01': {'prop': 'partName', 'init_val': '', 'type': 'App::PropertyString', 'Heading': 'BasicData', 'tooltip': 'Name of tha part of the blockMesh node ', 'current_val': 'Box'}, 'Property02': {'prop': 'partPath', 'init_val': '', 'type': 'App::PropertyPath', 'Heading': 'BasicData', 'tooltip': 'Path to tha part of the blockMesh node ', 'current_val': ''}, 'Property03': {'prop': 'convertToMeters', 'init_val': 1, 'type': 'App::PropertyFloat', 'Heading': 'BasicData', 'tooltip': 'Link a part to the blockMesh node ', 'current_val': 1.0}, 'Property04': {'prop': 'NumberOfCells', 'init_val': '1 2 3', 'type': 'App::PropertyString', 'Heading': 'Block', 'tooltip': 'Numbers of cells in each direction ', 'current_val': '1 2 3'}, 'Property05': {'prop': 'simpleGradingX', 'init_val': ['1'], 'type': 'App::PropertyStringList', 'Heading': 'Block', 'tooltip': 'simpleGrading in x direction ', 'current_val': ['1']}, 'Property06': {'prop': 'simpleGradingY', 'init_val': ['1'], 'type': 'App::PropertyStringList', 'Heading': 'Block', 'tooltip': 'simpleGrading in y direction ', 'current_val': ['0.2 0.3 4', '0.6 0.4 1', '0.2 0.3 0.25']}, 'Property07': {'prop': 'simpleGradingZ', 'init_val': ['1'], 'type': 'App::PropertyStringList', 'Heading': 'Block', 'tooltip': 'simpleGrading in z direction ', 'current_val': ['1']}}
        params['WebGui']     = {}
        
        params['vertices'] = ['0.0 0.0 0.0 ', '11.0 0.0 0.0 ', '11.0 12.0 0.0 ', '0.0 12.0 0.0 ', '0.0 0.0 13.0 ', '11.0 0.0 13.0 ', '11.0 12.0 13.0 ', '0.0 12.0 13.0 ']
        params['boundary'] = [{'Name': 'wall', 'Type': 'wall', 'Properties': {}, 'faces': {'Face6': {'vertices': '4 5 6 7'}}}, {'Name': 'a', 'Type': 'cyclic', 'Properties': {'Property01': {'prop': 'neighbourPatch', 'init_val': ['notSet'], 'type': 'App::PropertyEnumeration', 'Heading': 'Neighbour', 'tooltip': 'Neight face name', 'current_val': 'b'}}, 'faces': {'Face1': {'vertices': '0 4 7 3'}}}, {'Name': 'b', 'Type': 'cyclic', 'Properties': {'Property01': {'prop': 'neighbourPatch', 'init_val': ['notSet'], 'type': 'App::PropertyEnumeration', 'Heading': 'Neighbour', 'tooltip': 'Neight face name', 'current_val': 'a'}}, 'faces': {'Face2': {'vertices': '1 2 6 5'}}}]

        
        executer_parameters = self.build_executer_parameters(task_executer_mapping, params)
        executer_parameters['WD_path']='/mnt/examples/BC/NoBC'
                    
        from hermes.Resources.executers.jinjaExecuters import BlockMeshExecuter  
        output = BlockMeshExecuter(self._taskJSON).run(**executer_parameters)
        
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
        
        self._workflowJSON = {'workflow': {'root': None, 'Templates': [], 'nodeList': ['BlockMesh', 'GeometryDefiner', 'ControlDict'], 'nodes': {'BlockMesh': {'Execution': {'type': 'jinjaExecuters.BlockMesh', 'input_parameters': {'Properties': '{value.Properties}', 'boundary': '{value.boundary}', 'vertices': '{value.vertices}', 'template': 'openFOAM/simpleFOAM/BlockMesh'}}, 'GUI': {'Type': 'BlockMeshNode', 'Properties': {'Property01': {'prop': 'partName', 'init_val': '', 'type': 'App::PropertyString', 'Heading': 'BasicData', 'tooltip': 'Name of tha part of the blockMesh node ', 'current_val': 'Box'}, 'Property02': {'prop': 'partPath', 'init_val': '', 'type': 'App::PropertyPath', 'Heading': 'BasicData', 'tooltip': 'Path to tha part of the blockMesh node ', 'current_val': ''}, 'Property03': {'prop': 'convertToMeters', 'init_val': 1, 'type': 'App::PropertyFloat', 'Heading': 'BasicData', 'tooltip': 'Link a part to the blockMesh node ', 'current_val': 1.0}, 'Property04': {'prop': 'NumberOfCells', 'init_val': '1 2 3', 'type': 'App::PropertyString', 'Heading': 'Block', 'tooltip': 'Numbers of cells in each direction ', 'current_val': '1 2 3'}, 'Property05': {'prop': 'simpleGradingX', 'init_val': ['1'], 'type': 'App::PropertyStringList', 'Heading': 'Block', 'tooltip': 'simpleGrading in x direction ', 'current_val': ['1']}, 'Property06': {'prop': 'simpleGradingY', 'init_val': ['1'], 'type': 'App::PropertyStringList', 'Heading': 'Block', 'tooltip': 'simpleGrading in y direction ', 'current_val': ['0.2 0.3 4', '0.6 0.4 1', '0.2 0.3 0.25']}, 'Property07': {'prop': 'simpleGradingZ', 'init_val': ['1'], 'type': 'App::PropertyStringList', 'Heading': 'Block', 'tooltip': 'simpleGrading in z direction ', 'current_val': ['1']}}, 'GeometryFaceTypes': {'TypeList': ['wall', 'symmetry', 'patch', 'cyclic'], 'TypeProperties': {'wall': {'Properties': {}}, 'symmetry': {'Properties': {}}, 'patch': {'Properties': {}}, 'cyclic': {'Properties': {'Property01': {'prop': 'neighbourPatch', 'init_val': ['notSet'], 'type': 'App::PropertyEnumeration', 'Heading': 'Neighbour', 'tooltip': 'Neight face name', 'current_val': 'a'}}}}}, 'boundary': [{'Name': 'wall', 'Type': 'wall', 'Properties': {}, 'faces': {'Face6': {'vertices': '4 5 6 7'}}}, {'Name': 'a', 'Type': 'cyclic', 'Properties': {'Property01': {'prop': 'neighbourPatch', 'init_val': ['notSet'], 'type': 'App::PropertyEnumeration', 'Heading': 'Neighbour', 'tooltip': 'Neight face name', 'current_val': 'b'}}, 'faces': {'Face1': {'vertices': '0 4 7 3'}}}, {'Name': 'b', 'Type': 'cyclic', 'Properties': {'Property01': {'prop': 'neighbourPatch', 'init_val': ['notSet'], 'type': 'App::PropertyEnumeration', 'Heading': 'Neighbour', 'tooltip': 'Neight face name', 'current_val': 'a'}}, 'faces': {'Face2': {'vertices': '1 2 6 5'}}}], 'vertices': ['0.0 0.0 0.0 ', '11.0 0.0 0.0 ', '11.0 12.0 0.0 ', '0.0 12.0 0.0 ', '0.0 0.0 13.0 ', '11.0 0.0 13.0 ', '11.0 12.0 13.0 ', '0.0 12.0 13.0 ']}}, 'GeometryDefiner': {'Execution': {'type': 'jinjaExecuters.GeometryDefiner', 'input_parameters': {}}, 'GUI': {'Type': 'GeometryDefinerNode', 'Properties': {'Property1': {'prop': 'IntegerProperty', 'init_val': 10, 'type': 'App::PropertyInteger', 'Heading': 'PropInteger', 'tooltip': 'IntegerProperty', 'current_val': 10}}, 'GeometryFaceTypes': {'TypeList': ['wall', 'symmetry', 'patch', 'boundarylayer'], 'TypeProperties': {'wall': {'Properties': {'Property01': {'prop': 'Ux', 'init_val': '0 m/s', 'type': 'App::PropertySpeed', 'Heading': 'Velocity', 'tooltip': 'Velocity in x direction ', 'current_val': '0 m/s'}, 'Property02': {'prop': 'Uy', 'init_val': '0 m/s', 'type': 'App::PropertySpeed', 'Heading': 'Velocity', 'tooltip': 'Velocity in y direction', 'current_val': '0 m/s'}}}, 'symmetry': {'Properties': {'Property01': {'prop': 'P0', 'init_val': '10 Pa', 'type': 'App::PropertyPressure', 'Heading': 'Pressure', 'tooltip': 'Total Pressure ', 'current_val': '11 Pa'}}}, 'patch': {'Properties': {'Property01': {'prop': 'P0', 'init_val': '10 Pa', 'type': 'App::PropertyPressure', 'Heading': 'Pressure', 'tooltip': 'Total Pressure ', 'current_val': '12 Pa'}}}, 'boundarylayer': {'Properties': {'Property01': {'prop': 'P0', 'init_val': '10 Pa', 'type': 'App::PropertyPressure', 'Heading': 'Pressure', 'tooltip': 'Total Pressure ', 'current_val': '13 Pa'}}}}}, 'GeometryEntityList': {}}}, 'ControlDict': {'Execution': {'type': 'jinjaExecuters.jinja', 'input_parameters': {'values': '{WebGui.formData}', 'template': 'openFOAM/simpleFOAM/ControlDict'}}, 'GUI': {'Type': 'WebGuiNode', 'Properties': {}, 'WebGui': {'Schema': {'title': '', 'description': '', 'type': 'object', 'properties': {'application': {'type': 'string', 'title': 'application'}, 'startFrom': {'type': 'string', 'enum': ['firstTime', 'startTime', 'latestTime'], 'description': 'Controls the start time of the simulation.'}, 'startTime': {'title': 'startTime', 'type': 'number', 'description': 'Start time for the simulation with startFrom startTime'}, 'stopAt': {'type': 'string', 'enum': ['endTime', 'writeNow', 'noWriteNow', 'nextwrite'], 'description': 'Controls the end time of the simulation.'}, 'endTime': {'title': 'endTime', 'type': 'number', 'description': 'End time for the simulation when stopAt endTime; is specified.'}, 'deltaT': {'title': 'deltaT', 'type': 'number', 'description': 'Time step of the simulation.'}, 'writeControl': {'type': 'string', 'enum': ['timeStep', 'runTime', 'adjustableRunTime', 'cpuTime', 'clockTime'], 'description': 'Controls the timing of write output to file.'}, 'writeInterval': {'title': 'writeInterval', 'type': 'integer', 'description': 'Scalar used in conjunction with writeControl described above.'}, 'purgeWrite': {'title': 'purgeWrite', 'type': 'integer', 'description': 'Integer representing a limit on the number of time directories that are stored by overwriting time directories on a cyclic basis.'}, 'writeFormat': {'type': 'string', 'enum': ['ascii', 'binary'], 'description': 'Specifies the format of the data files.'}, 'writePrecision': {'title': 'writePrecision', 'type': 'integer', 'description': 'Integer used in conjunction with writeFormat described above.'}, 'writeCompression': {'type': 'boolean', 'title': 'writeCompression', 'description': 'Switch to specify whether files are compressed with gzip'}, 'timeFormat': {'type': 'string', 'enum': ['fixed', 'scientific', 'general'], 'description': 'Controls the timing of write output to file.'}, 'timePrecision': {'title': 'timePrecision', 'type': 'integer', 'description': 'Integer used in conjunction with timeFormat described above'}, 'runTimeModifiable': {'type': 'boolean', 'title': 'runTimeModifiable', 'description': 'Switch for whether dictionaries, e.g. controlDict, are re-read during a simulation at the beginning of each time step, allowing the user to modify parameters during a simulation.'}, 'graphFormat': {'type': 'string', 'enum': ['no graph', 'raw', 'gnuplot', 'xmgr', 'jplot'], 'description': 'Format for graph data written by an application.'}, 'adjustTimeStep': {'type': 'boolean', 'title': 'adjustTimeStep', 'description': 'Switch used by some solvers to adjust the time step during the simulation, usually according to maxCo.'}, 'maxCo': {'title': 'maxCo', 'type': 'number', 'description': 'Maximum Courant number.'}, 'interpolate': {'type': 'boolean', 'title': 'interpolate'}, 'libs': {'type': 'array', 'title': 'libs', 'items': {'type': 'string', 'description': 'List of additional libraries (on $LD_LIBRARY_PATH) to be loaded at run-time'}}, 'functions': {'type': 'array', 'title': 'functions', 'items': {'type': 'string', 'description': 'Dictionary of functions, e.g.  probes to be loaded at run-time'}}}}, 'uiSchema': {'listOfStrings': {'items': {'ui:emptyValue': ''}}, 'functions': {'items': {'ui:emptyValue': ''}}}, 'formData': {'application': 'simpleFoam', 'startFrom': 'startTime', 'startTime': 0, 'stopAt': 'endTime', 'endTime': 1000, 'deltaT': 1, 'writeControl': 'timeStep', 'writeInterval': 100, 'purgeWrite': 0, 'writeFormat': 'ascii', 'writePrecision': 7, 'writeCompression': 'false', 'timeFormat': 'general', 'timePrecision': 6, 'runTimeModifiable': 'true', 'interpolate': 'true', 'functions': []}}}}, 'finalnode_xx': {'name': 'finalnode_xx', 'Execution': {'type': 'generalExecuters.parameter', 'input_parameters': {}}, 'requires': ['BlockMesh', 'GeometryDefiner', 'ControlDict'], 'GUI': {'TypeFC': {}, 'Properties': {}, 'WebGui': {}}}}}}['workflow']

    def output(self):
        return luigi.LocalTarget("outputsOriginal/finalnode_xx_0.json")

    def requires(self):
        return dict(
                       GeometryDefiner=GeometryDefiner_0(),
                       ControlDict=ControlDict_0(),
                       BlockMesh=BlockMesh_0()
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
        executer_parameters['WD_path']='/mnt/examples/BC/NoBC'
                    
        from hermes.Resources.executers.generalExecuters import parameterExecuter  
        output = parameterExecuter(self._taskJSON).run(**executer_parameters)
        
        params['input_parameters'] = executer_parameters 
        params['output'] = output        
        
        out_params = params
        with open(self.output().fn, "w") as outfile:
            json.dump(out_params, outfile)
