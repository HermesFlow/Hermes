

import shutil
import os
import luigi
import json 
import sys

sys.path.insert(1, "/home/noga/Noga/FreeCad/github/Hermes/master/Hermes")
from hermes.engines.luigi.taskUtils import utils as hermesutils

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
        
        self._workflowJSON = {'workflow': {'root': None, 'Templates': [], 'nodeList': ['BlockMesh', 'GeometryDefiner', 'FileWriter'], 'nodes': {'BlockMesh': {'Execution': {'type': 'jinjaExecuters.BlockMesh', 'input_parameters': {'Properties': '{value.Properties}', 'boundary': '{value.boundary}', 'vertices': '{value.vertices}', 'template': 'openFOAM/simpleFOAM/BlockMesh'}}, 'GUI': {'Type': 'BlockMeshNode', 'Properties': {'Property01': {'prop': 'partName', 'init_val': '', 'type': 'App::PropertyString', 'Heading': 'BasicData', 'tooltip': 'Name of tha part of the blockMesh node ', 'current_val': ''}, 'Property02': {'prop': 'partPath', 'init_val': '', 'type': 'App::PropertyPath', 'Heading': 'BasicData', 'tooltip': 'Path to tha part of the blockMesh node ', 'current_val': ''}, 'Property03': {'prop': 'convertToMeters', 'init_val': 1, 'type': 'App::PropertyFloat', 'Heading': 'BasicData', 'tooltip': 'Link a part to the blockMesh node ', 'current_val': 1.0}, 'Property04': {'prop': 'NumberOfCells', 'init_val': '1 2 3', 'type': 'App::PropertyString', 'Heading': 'Block', 'tooltip': 'Numbers of cells in each direction ', 'current_val': '1 2 3'}, 'Property05': {'prop': 'simpleGradingX', 'init_val': ['1'], 'type': 'App::PropertyStringList', 'Heading': 'Block', 'tooltip': 'simpleGrading in x direction ', 'current_val': ['1']}, 'Property06': {'prop': 'simpleGradingY', 'init_val': ['1'], 'type': 'App::PropertyStringList', 'Heading': 'Block', 'tooltip': 'simpleGrading in y direction ', 'current_val': ['0.2 0.3 4', '0.6 0.4 1', '0.2 0.3 0.25']}, 'Property07': {'prop': 'simpleGradingZ', 'init_val': ['1'], 'type': 'App::PropertyStringList', 'Heading': 'Block', 'tooltip': 'simpleGrading in z direction ', 'current_val': ['1']}}, 'GeometryFaceTypes': {'TypeList': ['wall', 'symmetry', 'patch', 'boundarylayer'], 'TypeProperties': {'wall': {'Properties': {'Property01': {'prop': 'Ux', 'init_val': '0 m/s', 'type': 'App::PropertySpeed', 'Heading': 'Velocity', 'tooltip': 'Velocity in x direction ', 'current_val': '0 m/s'}, 'Property02': {'prop': 'Uy', 'init_val': '0 m/s', 'type': 'App::PropertySpeed', 'Heading': 'Velocity', 'tooltip': 'Velocity in y direction', 'current_val': '0 m/s'}}}, 'symmetry': {'Properties': {'Property01': {'prop': 'P0', 'init_val': '10 Pa', 'type': 'App::PropertyPressure', 'Heading': 'Pressure', 'tooltip': 'Total Pressure ', 'current_val': '11 Pa'}}}, 'patch': {'Properties': {'Property01': {'prop': 'P0', 'init_val': '10 Pa', 'type': 'App::PropertyPressure', 'Heading': 'Pressure', 'tooltip': 'Total Pressure ', 'current_val': '12 Pa'}}}, 'boundarylayer': {'Properties': {'Property01': {'prop': 'P0', 'init_val': '10 Pa', 'type': 'App::PropertyPressure', 'Heading': 'Pressure', 'tooltip': 'Total Pressure ', 'current_val': '13 Pa'}}}}}, 'boundary': [], 'vertices': []}}, 'GeometryDefiner': {'Execution': {'type': 'pythonExecuters.python', 'input_parameters': {}}, 'GUI': {'Type': 'GeometryDefinerNode', 'Properties': {'Property1': {'prop': 'IntegerProperty', 'init_val': 10, 'type': 'App::PropertyInteger', 'Heading': 'PropInteger', 'tooltip': 'IntegerProperty', 'current_val': 10}}, 'GeometryFaceTypes': {'TypeList': ['wall', 'symmetry', 'patch', 'boundarylayer'], 'TypeProperties': {'wall': {'Properties': {'Property01': {'prop': 'Ux', 'init_val': '0 m/s', 'type': 'App::PropertySpeed', 'Heading': 'Velocity', 'tooltip': 'Velocity in x direction ', 'current_val': '0 m/s'}, 'Property02': {'prop': 'Uy', 'init_val': '0 m/s', 'type': 'App::PropertySpeed', 'Heading': 'Velocity', 'tooltip': 'Velocity in y direction', 'current_val': '0 m/s'}}}, 'symmetry': {'Properties': {'Property01': {'prop': 'P0', 'init_val': '10 Pa', 'type': 'App::PropertyPressure', 'Heading': 'Pressure', 'tooltip': 'Total Pressure ', 'current_val': '11 Pa'}}}, 'patch': {'Properties': {'Property01': {'prop': 'P0', 'init_val': '10 Pa', 'type': 'App::PropertyPressure', 'Heading': 'Pressure', 'tooltip': 'Total Pressure ', 'current_val': '12 Pa'}}}, 'boundarylayer': {'Properties': {'Property01': {'prop': 'P0', 'init_val': '10 Pa', 'type': 'App::PropertyPressure', 'Heading': 'Pressure', 'tooltip': 'Total Pressure ', 'current_val': '13 Pa'}}}}}, 'GeometryEntityList': {'GE1': {'Name': 'wall', 'Type': 'wall', 'Properties': {'Property01': {'prop': 'Ux', 'init_val': '0 m/s', 'type': 'App::PropertySpeed', 'Heading': 'Velocity', 'tooltip': 'Velocity in x direction ', 'current_val': '0 mm/s'}, 'Property02': {'prop': 'Uy', 'init_val': '0 m/s', 'type': 'App::PropertySpeed', 'Heading': 'Velocity', 'tooltip': 'Velocity in y direction', 'current_val': '0 mm/s'}}, 'faceList': {'Part1': {'Name': 'Cube', 'Path': '/', 'faces': ['Face1', 'Face2']}}}, 'GE2': {'Name': 'symmetry', 'Type': 'symmetry', 'Properties': {'Property01': {'prop': 'P0', 'init_val': '10 Pa', 'type': 'App::PropertyPressure', 'Heading': 'Pressure', 'tooltip': 'Total Pressure ', 'current_val': '0.01 kg/(mm*s^2)'}}, 'faceList': {'Part1': {'Name': 'Cube', 'Path': '/', 'faces': ['Face3', 'Face4']}}}}}}, 'FileWriter': {'Execution': {'type': 'generalExecuters.FilesWriter', 'input_parameters': {'casePath': 'OpenFOAMfiles/', 'Files': {'system/BlockMesh': '{BlockMesh.output.openFOAMfile}'}}}, 'GUI': {'Type': 'WebGuiNode', 'Properties': {}, 'WebGui': {}}}, 'finalnode_xx': {'name': 'finalnode_xx', 'Execution': {'type': 'generalExecuters.parameter', 'input_parameters': {}}, 'requires': ['BlockMesh', 'GeometryDefiner', 'FileWriter'], 'GUI': {'TypeFC': {}, 'Properties': {}, 'WebGui': {}}}}}}['workflow']

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
        params['Properties'] = {'Property01': {'prop': 'partName', 'init_val': '', 'type': 'App::PropertyString', 'Heading': 'BasicData', 'tooltip': 'Name of tha part of the blockMesh node ', 'current_val': ''}, 'Property02': {'prop': 'partPath', 'init_val': '', 'type': 'App::PropertyPath', 'Heading': 'BasicData', 'tooltip': 'Path to tha part of the blockMesh node ', 'current_val': ''}, 'Property03': {'prop': 'convertToMeters', 'init_val': 1, 'type': 'App::PropertyFloat', 'Heading': 'BasicData', 'tooltip': 'Link a part to the blockMesh node ', 'current_val': 1.0}, 'Property04': {'prop': 'NumberOfCells', 'init_val': '1 2 3', 'type': 'App::PropertyString', 'Heading': 'Block', 'tooltip': 'Numbers of cells in each direction ', 'current_val': '1 2 3'}, 'Property05': {'prop': 'simpleGradingX', 'init_val': ['1'], 'type': 'App::PropertyStringList', 'Heading': 'Block', 'tooltip': 'simpleGrading in x direction ', 'current_val': ['1']}, 'Property06': {'prop': 'simpleGradingY', 'init_val': ['1'], 'type': 'App::PropertyStringList', 'Heading': 'Block', 'tooltip': 'simpleGrading in y direction ', 'current_val': ['0.2 0.3 4', '0.6 0.4 1', '0.2 0.3 0.25']}, 'Property07': {'prop': 'simpleGradingZ', 'init_val': ['1'], 'type': 'App::PropertyStringList', 'Heading': 'Block', 'tooltip': 'simpleGrading in z direction ', 'current_val': ['1']}}
        params['WebGui']     = {}
        
        params['vertices'] = []
        params['boundary'] = []

        
        executer_parameters = self.build_executer_parameters(task_executer_mapping, params)
        executer_parameters['WD_path']='/home/noga/Noga/FreeCad/github/Hermes/master/Hermes/examples/BlockMesh/example_template'
                    
        from hermes.Resources.executers.jinjaExecuters import BlockMeshExecuter  
        output = BlockMeshExecuter(self._taskJSON).run(**executer_parameters)
        
        params['input_parameters'] = executer_parameters 
        params['output'] = output        
        
        out_params = params
        with open(self.output().fn,"w") as outfile:
            json.dump(out_params,outfile)

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
        
        self._workflowJSON = {'workflow': {'root': None, 'Templates': [], 'nodeList': ['BlockMesh', 'GeometryDefiner', 'FileWriter'], 'nodes': {'BlockMesh': {'Execution': {'type': 'jinjaExecuters.BlockMesh', 'input_parameters': {'Properties': '{value.Properties}', 'boundary': '{value.boundary}', 'vertices': '{value.vertices}', 'template': 'openFOAM/simpleFOAM/BlockMesh'}}, 'GUI': {'Type': 'BlockMeshNode', 'Properties': {'Property01': {'prop': 'partName', 'init_val': '', 'type': 'App::PropertyString', 'Heading': 'BasicData', 'tooltip': 'Name of tha part of the blockMesh node ', 'current_val': ''}, 'Property02': {'prop': 'partPath', 'init_val': '', 'type': 'App::PropertyPath', 'Heading': 'BasicData', 'tooltip': 'Path to tha part of the blockMesh node ', 'current_val': ''}, 'Property03': {'prop': 'convertToMeters', 'init_val': 1, 'type': 'App::PropertyFloat', 'Heading': 'BasicData', 'tooltip': 'Link a part to the blockMesh node ', 'current_val': 1.0}, 'Property04': {'prop': 'NumberOfCells', 'init_val': '1 2 3', 'type': 'App::PropertyString', 'Heading': 'Block', 'tooltip': 'Numbers of cells in each direction ', 'current_val': '1 2 3'}, 'Property05': {'prop': 'simpleGradingX', 'init_val': ['1'], 'type': 'App::PropertyStringList', 'Heading': 'Block', 'tooltip': 'simpleGrading in x direction ', 'current_val': ['1']}, 'Property06': {'prop': 'simpleGradingY', 'init_val': ['1'], 'type': 'App::PropertyStringList', 'Heading': 'Block', 'tooltip': 'simpleGrading in y direction ', 'current_val': ['0.2 0.3 4', '0.6 0.4 1', '0.2 0.3 0.25']}, 'Property07': {'prop': 'simpleGradingZ', 'init_val': ['1'], 'type': 'App::PropertyStringList', 'Heading': 'Block', 'tooltip': 'simpleGrading in z direction ', 'current_val': ['1']}}, 'GeometryFaceTypes': {'TypeList': ['wall', 'symmetry', 'patch', 'boundarylayer'], 'TypeProperties': {'wall': {'Properties': {'Property01': {'prop': 'Ux', 'init_val': '0 m/s', 'type': 'App::PropertySpeed', 'Heading': 'Velocity', 'tooltip': 'Velocity in x direction ', 'current_val': '0 m/s'}, 'Property02': {'prop': 'Uy', 'init_val': '0 m/s', 'type': 'App::PropertySpeed', 'Heading': 'Velocity', 'tooltip': 'Velocity in y direction', 'current_val': '0 m/s'}}}, 'symmetry': {'Properties': {'Property01': {'prop': 'P0', 'init_val': '10 Pa', 'type': 'App::PropertyPressure', 'Heading': 'Pressure', 'tooltip': 'Total Pressure ', 'current_val': '11 Pa'}}}, 'patch': {'Properties': {'Property01': {'prop': 'P0', 'init_val': '10 Pa', 'type': 'App::PropertyPressure', 'Heading': 'Pressure', 'tooltip': 'Total Pressure ', 'current_val': '12 Pa'}}}, 'boundarylayer': {'Properties': {'Property01': {'prop': 'P0', 'init_val': '10 Pa', 'type': 'App::PropertyPressure', 'Heading': 'Pressure', 'tooltip': 'Total Pressure ', 'current_val': '13 Pa'}}}}}, 'boundary': [], 'vertices': []}}, 'GeometryDefiner': {'Execution': {'type': 'pythonExecuters.python', 'input_parameters': {}}, 'GUI': {'Type': 'GeometryDefinerNode', 'Properties': {'Property1': {'prop': 'IntegerProperty', 'init_val': 10, 'type': 'App::PropertyInteger', 'Heading': 'PropInteger', 'tooltip': 'IntegerProperty', 'current_val': 10}}, 'GeometryFaceTypes': {'TypeList': ['wall', 'symmetry', 'patch', 'boundarylayer'], 'TypeProperties': {'wall': {'Properties': {'Property01': {'prop': 'Ux', 'init_val': '0 m/s', 'type': 'App::PropertySpeed', 'Heading': 'Velocity', 'tooltip': 'Velocity in x direction ', 'current_val': '0 m/s'}, 'Property02': {'prop': 'Uy', 'init_val': '0 m/s', 'type': 'App::PropertySpeed', 'Heading': 'Velocity', 'tooltip': 'Velocity in y direction', 'current_val': '0 m/s'}}}, 'symmetry': {'Properties': {'Property01': {'prop': 'P0', 'init_val': '10 Pa', 'type': 'App::PropertyPressure', 'Heading': 'Pressure', 'tooltip': 'Total Pressure ', 'current_val': '11 Pa'}}}, 'patch': {'Properties': {'Property01': {'prop': 'P0', 'init_val': '10 Pa', 'type': 'App::PropertyPressure', 'Heading': 'Pressure', 'tooltip': 'Total Pressure ', 'current_val': '12 Pa'}}}, 'boundarylayer': {'Properties': {'Property01': {'prop': 'P0', 'init_val': '10 Pa', 'type': 'App::PropertyPressure', 'Heading': 'Pressure', 'tooltip': 'Total Pressure ', 'current_val': '13 Pa'}}}}}, 'GeometryEntityList': {'GE1': {'Name': 'wall', 'Type': 'wall', 'Properties': {'Property01': {'prop': 'Ux', 'init_val': '0 m/s', 'type': 'App::PropertySpeed', 'Heading': 'Velocity', 'tooltip': 'Velocity in x direction ', 'current_val': '0 mm/s'}, 'Property02': {'prop': 'Uy', 'init_val': '0 m/s', 'type': 'App::PropertySpeed', 'Heading': 'Velocity', 'tooltip': 'Velocity in y direction', 'current_val': '0 mm/s'}}, 'faceList': {'Part1': {'Name': 'Cube', 'Path': '/', 'faces': ['Face1', 'Face2']}}}, 'GE2': {'Name': 'symmetry', 'Type': 'symmetry', 'Properties': {'Property01': {'prop': 'P0', 'init_val': '10 Pa', 'type': 'App::PropertyPressure', 'Heading': 'Pressure', 'tooltip': 'Total Pressure ', 'current_val': '0.01 kg/(mm*s^2)'}}, 'faceList': {'Part1': {'Name': 'Cube', 'Path': '/', 'faces': ['Face3', 'Face4']}}}}}}, 'FileWriter': {'Execution': {'type': 'generalExecuters.FilesWriter', 'input_parameters': {'casePath': 'OpenFOAMfiles/', 'Files': {'system/BlockMesh': '{BlockMesh.output.openFOAMfile}'}}}, 'GUI': {'Type': 'WebGuiNode', 'Properties': {}, 'WebGui': {}}}, 'finalnode_xx': {'name': 'finalnode_xx', 'Execution': {'type': 'generalExecuters.parameter', 'input_parameters': {}}, 'requires': ['BlockMesh', 'GeometryDefiner', 'FileWriter'], 'GUI': {'TypeFC': {}, 'Properties': {}, 'WebGui': {}}}}}}['workflow']

    def output(self):
        return luigi.LocalTarget("outputsOriginal/FileWriter_0.json")

    def requires(self):
        return dict(
                       BlockMesh=BlockMesh_0()
                   )

    def run(self):
        target = self.output()
        target.makedirs()
        
        task_executer_mapping = {'casePath': 'OpenFOAMfiles/', 'Files': {'system/BlockMesh': '{BlockMesh.output.openFOAMfile}'}}
        
        parameters_from_required = self.get_all_required_outputs()        
        params = dict(parameters_from_required)
        params['formData']   = {}
        params['files']      = {}
        params['Schema']     = {}
        params['uiSchema']   = {}
        params['Properties'] = {}
        params['WebGui']     = {}
        
       
        executer_parameters = self.build_executer_parameters(task_executer_mapping, params)
        executer_parameters['WD_path']='/home/noga/Noga/FreeCad/github/Hermes/master/Hermes/examples/BlockMesh/example_template'
                    
        from hermes.Resources.executers.generalExecuters import FilesWriterExecuter  
        output = FilesWriterExecuter(self._taskJSON).run(**executer_parameters)
        
        params['input_parameters'] = executer_parameters 
        params['output'] = output        
        
        out_params = params
        with open(self.output().fn, "w") as outfile:
            json.dump(out_params, outfile)

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
        
        self._workflowJSON = {'workflow': {'root': None, 'Templates': [], 'nodeList': ['BlockMesh', 'GeometryDefiner', 'FileWriter'], 'nodes': {'BlockMesh': {'Execution': {'type': 'jinjaExecuters.BlockMesh', 'input_parameters': {'Properties': '{value.Properties}', 'boundary': '{value.boundary}', 'vertices': '{value.vertices}', 'template': 'openFOAM/simpleFOAM/BlockMesh'}}, 'GUI': {'Type': 'BlockMeshNode', 'Properties': {'Property01': {'prop': 'partName', 'init_val': '', 'type': 'App::PropertyString', 'Heading': 'BasicData', 'tooltip': 'Name of tha part of the blockMesh node ', 'current_val': ''}, 'Property02': {'prop': 'partPath', 'init_val': '', 'type': 'App::PropertyPath', 'Heading': 'BasicData', 'tooltip': 'Path to tha part of the blockMesh node ', 'current_val': ''}, 'Property03': {'prop': 'convertToMeters', 'init_val': 1, 'type': 'App::PropertyFloat', 'Heading': 'BasicData', 'tooltip': 'Link a part to the blockMesh node ', 'current_val': 1.0}, 'Property04': {'prop': 'NumberOfCells', 'init_val': '1 2 3', 'type': 'App::PropertyString', 'Heading': 'Block', 'tooltip': 'Numbers of cells in each direction ', 'current_val': '1 2 3'}, 'Property05': {'prop': 'simpleGradingX', 'init_val': ['1'], 'type': 'App::PropertyStringList', 'Heading': 'Block', 'tooltip': 'simpleGrading in x direction ', 'current_val': ['1']}, 'Property06': {'prop': 'simpleGradingY', 'init_val': ['1'], 'type': 'App::PropertyStringList', 'Heading': 'Block', 'tooltip': 'simpleGrading in y direction ', 'current_val': ['0.2 0.3 4', '0.6 0.4 1', '0.2 0.3 0.25']}, 'Property07': {'prop': 'simpleGradingZ', 'init_val': ['1'], 'type': 'App::PropertyStringList', 'Heading': 'Block', 'tooltip': 'simpleGrading in z direction ', 'current_val': ['1']}}, 'GeometryFaceTypes': {'TypeList': ['wall', 'symmetry', 'patch', 'boundarylayer'], 'TypeProperties': {'wall': {'Properties': {'Property01': {'prop': 'Ux', 'init_val': '0 m/s', 'type': 'App::PropertySpeed', 'Heading': 'Velocity', 'tooltip': 'Velocity in x direction ', 'current_val': '0 m/s'}, 'Property02': {'prop': 'Uy', 'init_val': '0 m/s', 'type': 'App::PropertySpeed', 'Heading': 'Velocity', 'tooltip': 'Velocity in y direction', 'current_val': '0 m/s'}}}, 'symmetry': {'Properties': {'Property01': {'prop': 'P0', 'init_val': '10 Pa', 'type': 'App::PropertyPressure', 'Heading': 'Pressure', 'tooltip': 'Total Pressure ', 'current_val': '11 Pa'}}}, 'patch': {'Properties': {'Property01': {'prop': 'P0', 'init_val': '10 Pa', 'type': 'App::PropertyPressure', 'Heading': 'Pressure', 'tooltip': 'Total Pressure ', 'current_val': '12 Pa'}}}, 'boundarylayer': {'Properties': {'Property01': {'prop': 'P0', 'init_val': '10 Pa', 'type': 'App::PropertyPressure', 'Heading': 'Pressure', 'tooltip': 'Total Pressure ', 'current_val': '13 Pa'}}}}}, 'boundary': [], 'vertices': []}}, 'GeometryDefiner': {'Execution': {'type': 'pythonExecuters.python', 'input_parameters': {}}, 'GUI': {'Type': 'GeometryDefinerNode', 'Properties': {'Property1': {'prop': 'IntegerProperty', 'init_val': 10, 'type': 'App::PropertyInteger', 'Heading': 'PropInteger', 'tooltip': 'IntegerProperty', 'current_val': 10}}, 'GeometryFaceTypes': {'TypeList': ['wall', 'symmetry', 'patch', 'boundarylayer'], 'TypeProperties': {'wall': {'Properties': {'Property01': {'prop': 'Ux', 'init_val': '0 m/s', 'type': 'App::PropertySpeed', 'Heading': 'Velocity', 'tooltip': 'Velocity in x direction ', 'current_val': '0 m/s'}, 'Property02': {'prop': 'Uy', 'init_val': '0 m/s', 'type': 'App::PropertySpeed', 'Heading': 'Velocity', 'tooltip': 'Velocity in y direction', 'current_val': '0 m/s'}}}, 'symmetry': {'Properties': {'Property01': {'prop': 'P0', 'init_val': '10 Pa', 'type': 'App::PropertyPressure', 'Heading': 'Pressure', 'tooltip': 'Total Pressure ', 'current_val': '11 Pa'}}}, 'patch': {'Properties': {'Property01': {'prop': 'P0', 'init_val': '10 Pa', 'type': 'App::PropertyPressure', 'Heading': 'Pressure', 'tooltip': 'Total Pressure ', 'current_val': '12 Pa'}}}, 'boundarylayer': {'Properties': {'Property01': {'prop': 'P0', 'init_val': '10 Pa', 'type': 'App::PropertyPressure', 'Heading': 'Pressure', 'tooltip': 'Total Pressure ', 'current_val': '13 Pa'}}}}}, 'GeometryEntityList': {'GE1': {'Name': 'wall', 'Type': 'wall', 'Properties': {'Property01': {'prop': 'Ux', 'init_val': '0 m/s', 'type': 'App::PropertySpeed', 'Heading': 'Velocity', 'tooltip': 'Velocity in x direction ', 'current_val': '0 mm/s'}, 'Property02': {'prop': 'Uy', 'init_val': '0 m/s', 'type': 'App::PropertySpeed', 'Heading': 'Velocity', 'tooltip': 'Velocity in y direction', 'current_val': '0 mm/s'}}, 'faceList': {'Part1': {'Name': 'Cube', 'Path': '/', 'faces': ['Face1', 'Face2']}}}, 'GE2': {'Name': 'symmetry', 'Type': 'symmetry', 'Properties': {'Property01': {'prop': 'P0', 'init_val': '10 Pa', 'type': 'App::PropertyPressure', 'Heading': 'Pressure', 'tooltip': 'Total Pressure ', 'current_val': '0.01 kg/(mm*s^2)'}}, 'faceList': {'Part1': {'Name': 'Cube', 'Path': '/', 'faces': ['Face3', 'Face4']}}}}}}, 'FileWriter': {'Execution': {'type': 'generalExecuters.FilesWriter', 'input_parameters': {'casePath': 'OpenFOAMfiles/', 'Files': {'system/BlockMesh': '{BlockMesh.output.openFOAMfile}'}}}, 'GUI': {'Type': 'WebGuiNode', 'Properties': {}, 'WebGui': {}}}, 'finalnode_xx': {'name': 'finalnode_xx', 'Execution': {'type': 'generalExecuters.parameter', 'input_parameters': {}}, 'requires': ['BlockMesh', 'GeometryDefiner', 'FileWriter'], 'GUI': {'TypeFC': {}, 'Properties': {}, 'WebGui': {}}}}}}['workflow']

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
        executer_parameters['WD_path']='/home/noga/Noga/FreeCad/github/Hermes/master/Hermes/examples/BlockMesh/example_template'
                    
        from hermes.Resources.executers.pythonExecuters import pythonExecuter  
        output = pythonExecuter(self._taskJSON).run(**executer_parameters)
        
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
        
        self._workflowJSON = {'workflow': {'root': None, 'Templates': [], 'nodeList': ['BlockMesh', 'GeometryDefiner', 'FileWriter'], 'nodes': {'BlockMesh': {'Execution': {'type': 'jinjaExecuters.BlockMesh', 'input_parameters': {'Properties': '{value.Properties}', 'boundary': '{value.boundary}', 'vertices': '{value.vertices}', 'template': 'openFOAM/simpleFOAM/BlockMesh'}}, 'GUI': {'Type': 'BlockMeshNode', 'Properties': {'Property01': {'prop': 'partName', 'init_val': '', 'type': 'App::PropertyString', 'Heading': 'BasicData', 'tooltip': 'Name of tha part of the blockMesh node ', 'current_val': ''}, 'Property02': {'prop': 'partPath', 'init_val': '', 'type': 'App::PropertyPath', 'Heading': 'BasicData', 'tooltip': 'Path to tha part of the blockMesh node ', 'current_val': ''}, 'Property03': {'prop': 'convertToMeters', 'init_val': 1, 'type': 'App::PropertyFloat', 'Heading': 'BasicData', 'tooltip': 'Link a part to the blockMesh node ', 'current_val': 1.0}, 'Property04': {'prop': 'NumberOfCells', 'init_val': '1 2 3', 'type': 'App::PropertyString', 'Heading': 'Block', 'tooltip': 'Numbers of cells in each direction ', 'current_val': '1 2 3'}, 'Property05': {'prop': 'simpleGradingX', 'init_val': ['1'], 'type': 'App::PropertyStringList', 'Heading': 'Block', 'tooltip': 'simpleGrading in x direction ', 'current_val': ['1']}, 'Property06': {'prop': 'simpleGradingY', 'init_val': ['1'], 'type': 'App::PropertyStringList', 'Heading': 'Block', 'tooltip': 'simpleGrading in y direction ', 'current_val': ['0.2 0.3 4', '0.6 0.4 1', '0.2 0.3 0.25']}, 'Property07': {'prop': 'simpleGradingZ', 'init_val': ['1'], 'type': 'App::PropertyStringList', 'Heading': 'Block', 'tooltip': 'simpleGrading in z direction ', 'current_val': ['1']}}, 'GeometryFaceTypes': {'TypeList': ['wall', 'symmetry', 'patch', 'boundarylayer'], 'TypeProperties': {'wall': {'Properties': {'Property01': {'prop': 'Ux', 'init_val': '0 m/s', 'type': 'App::PropertySpeed', 'Heading': 'Velocity', 'tooltip': 'Velocity in x direction ', 'current_val': '0 m/s'}, 'Property02': {'prop': 'Uy', 'init_val': '0 m/s', 'type': 'App::PropertySpeed', 'Heading': 'Velocity', 'tooltip': 'Velocity in y direction', 'current_val': '0 m/s'}}}, 'symmetry': {'Properties': {'Property01': {'prop': 'P0', 'init_val': '10 Pa', 'type': 'App::PropertyPressure', 'Heading': 'Pressure', 'tooltip': 'Total Pressure ', 'current_val': '11 Pa'}}}, 'patch': {'Properties': {'Property01': {'prop': 'P0', 'init_val': '10 Pa', 'type': 'App::PropertyPressure', 'Heading': 'Pressure', 'tooltip': 'Total Pressure ', 'current_val': '12 Pa'}}}, 'boundarylayer': {'Properties': {'Property01': {'prop': 'P0', 'init_val': '10 Pa', 'type': 'App::PropertyPressure', 'Heading': 'Pressure', 'tooltip': 'Total Pressure ', 'current_val': '13 Pa'}}}}}, 'boundary': [], 'vertices': []}}, 'GeometryDefiner': {'Execution': {'type': 'pythonExecuters.python', 'input_parameters': {}}, 'GUI': {'Type': 'GeometryDefinerNode', 'Properties': {'Property1': {'prop': 'IntegerProperty', 'init_val': 10, 'type': 'App::PropertyInteger', 'Heading': 'PropInteger', 'tooltip': 'IntegerProperty', 'current_val': 10}}, 'GeometryFaceTypes': {'TypeList': ['wall', 'symmetry', 'patch', 'boundarylayer'], 'TypeProperties': {'wall': {'Properties': {'Property01': {'prop': 'Ux', 'init_val': '0 m/s', 'type': 'App::PropertySpeed', 'Heading': 'Velocity', 'tooltip': 'Velocity in x direction ', 'current_val': '0 m/s'}, 'Property02': {'prop': 'Uy', 'init_val': '0 m/s', 'type': 'App::PropertySpeed', 'Heading': 'Velocity', 'tooltip': 'Velocity in y direction', 'current_val': '0 m/s'}}}, 'symmetry': {'Properties': {'Property01': {'prop': 'P0', 'init_val': '10 Pa', 'type': 'App::PropertyPressure', 'Heading': 'Pressure', 'tooltip': 'Total Pressure ', 'current_val': '11 Pa'}}}, 'patch': {'Properties': {'Property01': {'prop': 'P0', 'init_val': '10 Pa', 'type': 'App::PropertyPressure', 'Heading': 'Pressure', 'tooltip': 'Total Pressure ', 'current_val': '12 Pa'}}}, 'boundarylayer': {'Properties': {'Property01': {'prop': 'P0', 'init_val': '10 Pa', 'type': 'App::PropertyPressure', 'Heading': 'Pressure', 'tooltip': 'Total Pressure ', 'current_val': '13 Pa'}}}}}, 'GeometryEntityList': {'GE1': {'Name': 'wall', 'Type': 'wall', 'Properties': {'Property01': {'prop': 'Ux', 'init_val': '0 m/s', 'type': 'App::PropertySpeed', 'Heading': 'Velocity', 'tooltip': 'Velocity in x direction ', 'current_val': '0 mm/s'}, 'Property02': {'prop': 'Uy', 'init_val': '0 m/s', 'type': 'App::PropertySpeed', 'Heading': 'Velocity', 'tooltip': 'Velocity in y direction', 'current_val': '0 mm/s'}}, 'faceList': {'Part1': {'Name': 'Cube', 'Path': '/', 'faces': ['Face1', 'Face2']}}}, 'GE2': {'Name': 'symmetry', 'Type': 'symmetry', 'Properties': {'Property01': {'prop': 'P0', 'init_val': '10 Pa', 'type': 'App::PropertyPressure', 'Heading': 'Pressure', 'tooltip': 'Total Pressure ', 'current_val': '0.01 kg/(mm*s^2)'}}, 'faceList': {'Part1': {'Name': 'Cube', 'Path': '/', 'faces': ['Face3', 'Face4']}}}}}}, 'FileWriter': {'Execution': {'type': 'generalExecuters.FilesWriter', 'input_parameters': {'casePath': 'OpenFOAMfiles/', 'Files': {'system/BlockMesh': '{BlockMesh.output.openFOAMfile}'}}}, 'GUI': {'Type': 'WebGuiNode', 'Properties': {}, 'WebGui': {}}}, 'finalnode_xx': {'name': 'finalnode_xx', 'Execution': {'type': 'generalExecuters.parameter', 'input_parameters': {}}, 'requires': ['BlockMesh', 'GeometryDefiner', 'FileWriter'], 'GUI': {'TypeFC': {}, 'Properties': {}, 'WebGui': {}}}}}}['workflow']

    def output(self):
        return luigi.LocalTarget("outputsOriginal/finalnode_xx_0.json")

    def requires(self):
        return dict(
                       BlockMesh=BlockMesh_0(),
                       FileWriter=FileWriter_0(),
                       GeometryDefiner=GeometryDefiner_0()
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
        executer_parameters['WD_path']='/home/noga/Noga/FreeCad/github/Hermes/master/Hermes/examples/BlockMesh/example_template'
                    
        from hermes.Resources.executers.generalExecuters import parameterExecuter  
        output = parameterExecuter(self._taskJSON).run(**executer_parameters)
        
        params['input_parameters'] = executer_parameters 
        params['output'] = output        
        
        out_params = params
        with open(self.output().fn, "w") as outfile:
            json.dump(out_params, outfile)
