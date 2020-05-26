import pydoc

class executerHome(object):
    """
        Creates an executer from a configuration.


    TODO:
        For now read a predefined configuration.
        convert it to JSON in future versions.
    """

    # _executers_mapping = None
    #
    def __getitem__(self, item):
        return self.findExecuter(item)

    def findExecuter(self, executer):

        exec = pydoc.locate("hermes.Resources.executers.%s" % executer)
        if exec is None:
            raise KeyError("Executer %s Not Found" % executer)
        return exec

