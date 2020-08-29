import pydoc

class executerHome(object):
    """
        Creates an executer from a configuration.


    TODO:
        For now read a predefined configuration.
        convert it to JSON in future versions.
    """

    _thirdPartyExcuters = None

    def __init__(self):
        self._thirdPartyExcuters = {}

    def __getitem__(self, item):
        if item not in self._thirdPartyExcuters:
            return f"hermes.Resources.executers.{item}Executer"
        else:
            return self._thirdPartyExcuters[item]

    def loadExecuter(self, executer):
        fullpath = self[executer]
        exec = pydoc.locate(fullpath)
        if exec is None:
            raise KeyError("Executer %s Not Found" % executer)
        return exec

