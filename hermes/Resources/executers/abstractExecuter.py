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

class abstractExecuter(object):
    """
        An abstract executer that defines the general interfaces of the executers:

        - Load webGUI from a file (in a relative webGUI directory).
        - List all inputs.
        - List all outputsOriginal.

    """

    _parameters = None

    def __init__(self,JSON):
        """
            Initialize the file and override with the JSON parameters.

        :param JSON:
            the json that overrides the default parameters.
        """

        defaultparameters = self._defaultParameters()
        self._parameters  = defaultparameters.update(JSON)

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
