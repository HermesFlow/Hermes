"""
    Manages the template retrieval from repositories.
"""
import os
import json
import pathlib

class templateCenter:

    _paths = None

    def __init__(self, paths=None):
        """
            Initialize the template center.

            The default repository is the current directory.
            Allows the use to add more repositories.

            The name of the template is:

                [path].[filename]

            for example:
                general.CopyDirectory.

            The class will search in all the repositories and return the first match.


        """
        self._paths = paths

    def getTemplate(self, template):
        """
        Finds a template and returns it as a dict.
        """
        jsonPath = None
        template = template.replace(".", "/") + ".json"
        if self._paths is not None:
            for path in self._paths:
                if os.path.exists(path+template):
                    jsonPath = path+template
                    break

        jsonPath = os.path.join(pathlib.Path(__file__).parent.absolute(), template) if jsonPath is None else jsonPath
        # print(jsonPath)
        try:
            with open(jsonPath) as json_file:
                template = json.load(json_file)
        except FileNotFoundError:
            raise KeyError("Template %s Not Found" % template)
        return template
