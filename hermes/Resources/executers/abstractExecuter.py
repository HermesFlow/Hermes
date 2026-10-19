"""
Executer
---------

A class that is responsible for the execution of the different nodes in the Hermes system.

To define an executer we need to implement the interface of the execution.

The interface defines the:
        - WebGui - the default webGUI for the executer.
                   [ The interface can expose simple interface to read a file and return it as its GUI].

        - inputs  - The inputs to the executer (will be used in the mapping).
        - outputsOriginal - The outputsOriginal of the executer.

    The JSON file that is used to initiate the executioner can override this definitions.

Example executers:

    File System related:

            - Copy directory
            - Copy file
            - Execute OS command.


    Python executers:

            - Execute python script.
            - Execute Jinja2 transformation

    Sensitivity analysis:

            - spanParameters


            [ should be defined against a DB interface (TBD)].

    OpenFOAM
            - writing a dictionary
            - writing a value file.

"""
import abc
import logging
import os
from typing import Any

from geopandas import GeoDataFrame

from hermes.hermesLogging.loggingObject import loggedObject


class abstractExecuter(loggedObject):
    """
        An abstract executer that defines the mesh interfaces of the executers:

        - Load webGUI from a file (in a relative webGUI directory).
        - List all inputs.
        - List all outputsOriginal.

    """

    DASK_TREES_FOLDER = ".dask_trees"
    GEOPANDAS_FOLDER = ".geopandas"

    parameters = None

    version = None # The version of the OF template.

    @property
    def executerType(self):
        return self.parameters['type']

    @property
    def taskJSON(self):
        return self.parameters['Execution']

    def __init__(self,JSON):
        """
            Initialize the file and override with the JSON parameters.

        :param JSON:
            the json that overrides the default parameters.
        """
        super().__init__()
        self.parameters  = self._defaultParameters()
        self.parameters.update(JSON)
        self.version = 1

    @abc.abstractmethod
    def _defaultParameters(self):
        """
            Defines the default parameters of the class.
            Used in the initialization of the class

            must define the default:
                outputsOriginal
                inputs
                webGUI file (if exists)
                other parameters.

        :return:
            A map with the default parameters values.

        """
        return {}


    @abc.abstractmethod
    def run(self, **inputs):
        """
            runs the execution of the node.

        :param metadata:
            Meta data of the execution. The name of the calling node and
            other parameters that might be useful to the execution.

        :param inputs:
                The inputs needed for the execution.

        :return:
                a dict with the outputsOriginal->values.
        """
        pass


    @staticmethod
    def isReference(s:Any)->bool:
        return isinstance(s,str) and s.startswith("{") and s.endswith('}')

    @staticmethod
    def testParamValues(params: dict[str, Any]) -> tuple[bool, str]:
        """
            tests a set of parameter against node implementation.

        :param inputs:
                The inputs needed for the execution.

        :return:
                tuple where first value indicates if parameters are valid and second is an error message when params are invalid.
        """
        return True, ""

    @staticmethod
    def getValuesForParam(self):
        """
            Tries to get possible values for node params.

        :param inputs:
                The inputs needed for the execution.

        :return:
                tuple where first value indicates if parameters are valid and second is an error message when params are invalid.
        """
        return dict()

    def json(self):
        """
            Returns the JSON definiton of this executioner
            taken form the parameters.

        :return:
            A JSON object (a dict) with the definiton of this executioner
        """
        return {}

    @property
    def outputs(self):
        """
            Returns a list of outputsOriginal of this executer

        :return:
            A list of output names
        """
        return []

    @property
    def inputs(self):
        """
            Returns a list of inputs of this executer.

        :return:
            A list of executer
        """
        return []


    @property
    def webGUI(self):
        """
            Return the webGUI of the executioner.

        :return:
            A webGUI JSON.
        """
        pass


    @staticmethod
    def isParamTestable(params, param_name):
        return param_name in params and not abstractExecuter.isReference(params[param_name])
    
    @staticmethod
    def checkParamType(params: dict[str, Any], param_name: str, type: type | tuple[type, ...], required: bool = False) -> tuple[bool, str]:
        if param_name not in params.keys():
            if required:
                return False, f"{param_name} is missing"
            return True, ""
        if abstractExecuter.isReference(params[param_name]):
            return True, ""
        if not isinstance(params[param_name], type):
            return False, f"{param_name} must be type({type})"
        return True, ""
    
    @staticmethod
    def checkParamAgainstList(params, param_name, availableValues, required=False):
        if param_name not in params.keys():
            return (False, f"{param_name} is missing") if required else (True, "")
        if abstractExecuter.isParamTestable(params, param_name):
            if params[param_name] not in availableValues:
                return False, f"{param_name.title()} '{params[param_name]}' doesn't exists, choose one of: {', '.join(availableValues)}"
        return True, ""

    @staticmethod
    def save_dask_tree(project, dask_tree):
        """Serializes the dask-task-tree with cloudpickle"""
        import pathlib

        import cloudpickle
        from dask.tokenize import tokenize
        dask_tree_serialized = cloudpickle.dumps(dask_tree)

        # to avoid duplicate pickles we compute the hash and name the files based on the first chars of the hash
        try:
            serialization_hash = tokenize(dask_tree, ensure_deterministic=True) # sha256(dask_tree_serialized).hexdigest()[:32] 
        except tokenize.TokenizationError:
            serialization_hash = tokenize(dask_tree)
            logger = logging.getLoggerClass("luigi-interface")
            logger.warning("The dask tree couldn't be deterministically tokenized! this means duplicate runs will take more disk space")

        trees_folder = pathlib.Path(project.filesDirectory) / abstractExecuter.DASK_TREES_FOLDER
        os.makedirs(trees_folder, exist_ok=True)
        serialized_tree_file_path = trees_folder/f"{serialization_hash}.pkl"
        with open(serialized_tree_file_path, "wb") as f:
            f.write(dask_tree_serialized)
        return serialized_tree_file_path

    @staticmethod
    def save_geopandas(project, saved_obj: GeoDataFrame, filename):
        """Serializes the dask-task-tree with cloudpickle"""
        import pathlib

        # to avoid duplicate pickles we compute the hash and name the files based on the first chars of the hash
        geopandas_folder = pathlib.Path(project.filesDirectory) / abstractExecuter.GEOPANDAS_FOLDER
        os.makedirs(geopandas_folder, exist_ok=True)
        serialized_geopandas_file_path = geopandas_folder/f"geopanda-{filename}.parquet"
        saved_obj.to_parquet(serialized_geopandas_file_path)
        return serialized_geopandas_file_path


    @staticmethod
    def load_xarray(path:str):
        """checks if the path contains the pickled dask task and loads it correctly if it is. Returns xarray and True if path is a pickle, otehrwise False. Raises if neither"""
        import cloudpickle
        import magic
        import xarray
        mimetype=magic.from_file(path, mime=True)

        if mimetype in ['application/x-netcdf', 'application/x-hdf']:
            return xarray.open_mfdataset(path, combine='by_coords'), False
        elif mimetype in ["application/x-pickle", "application/octet-stream"]:
            with open(path, "rb") as f:
                dask_tree_deserialized = cloudpickle.load(f)
                return dask_tree_deserialized, True
        else:
            raise Exception(f"Expected file to be either netcdf or pickle but got {mimetype}")
