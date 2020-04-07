
class executerHome(object):
    """
        Creates an executer from a configuration.


    TODO:
        For now read a predefined configuration.
        convert it to JSON in future versions.
    """

    _executers_mapping = None

    def __getitem__(self, item):
        return self._executers_mapping[item]

    def __init__(self):
        self._executers_mapping = dict(
            copyDir="hermes.Resources.executers.fileSystemExecuter.copyDir",
            copyDirectory="hermes.Resources.executers.fileSystemExecuter.copyDirectory",
            copyFile="hermes.Resources.executers.fileSystemExecuter.copyFile",
            executeScript="hermes.Resources.executers.fileSystemExecuter.executeScript",
            RunOsCommand="hermes.Resources.executers.fileSystemExecuter.RunOsCommand",
            executerPython="hermes.Resources.executers.pythonExecuter.pythonExecuter",
            RunPythonScript="hermes.Resources.executers.pythonExecuter.RunPythonScript",
            parameters = "hermes.Resources.executers.generalExecuter.parameterExecuter",
            transformTemplate="hermes.Resources.executers.generalExecuter.transformTemplate",
            nogaExec = "hermes.Resources.executers.pythonExecuter.nogaExec",
            snappyHexMesh = "hermes.Resources.executers.pythonExecuter.snappyHexMesh",
            controlDict = "hermes.Resources.executers.pythonExecuter.controlDict",
            fvSchemes = "hermes.Resources.executers.pythonExecuter.fvSchemes",
            fvSolution = "hermes.Resources.executers.pythonExecuter.fvSolution",
            transportProperties = "hermes.Resources.executers.pythonExecuter.transportProperties",
            RASProperties = "hermes.Resources.executers.pythonExecuter.RASProperties"
        )
