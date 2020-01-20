
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
            copyDir="pyHermes.executers.fileSystemExecuter.copyDir",
            copyDirectory="pyHermes.executers.fileSystemExecuter.copyDirectory",
            copyFile="pyHermes.executers.fileSystemExecuter.copyFile",
            executeScript="pyHermes.executers.fileSystemExecuter.executeScript",
            RunOsCommand="pyHermes.executers.fileSystemExecuter.RunOsCommand",
            executerPython="pyHermes.executers.pythonExecuter.pythonExecuter",
            RunPythonScript="pyHermes.executers.pythonExecuter.RunPythonScript",
            parameters = "pyHermes.executers.generalExecuter.parameterExecuter",
            transformTemplate="pyHermes.executers.generalExecuter.transformTemplate",
            nogaExec = "pyHermes.executers.pythonExecuter.nogaExec",
            snappyHexMesh = "pyHermes.executers.pythonExecuter.snappyHexMesh",
            controlDict = "pyHermes.executers.pythonExecuter.controlDict",
            fvSchemes = "pyHermes.executers.pythonExecuter.fvSchemes",
            fvSolution = "pyHermes.executers.pythonExecuter.fvSolution",
            transportProperties = "pyHermes.executers.pythonExecuter.transportProperties",
            RASProperties = "pyHermes.executers.pythonExecuter.RASProperties"
        )
