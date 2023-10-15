"""
    Manages the template retrieval from repositories.
"""
import os
import json
import pathlib
from importlib import resources
from ..utils.logging import helpers as hermes_logging
from ..utils.jsonutils import loadJSON

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
                mesh.CopyDirectory.

            The class will search in all the repositories and return the first match.


        """
        self.logger = hermes_logging.get_logger(self)
        self._paths = paths

    def __getitem__(self, item):
        return self.getTemplate(item)

    def getTemplate(self, template):
        """
        Finds a template and return a copy of it  as a dict.
        """
        self.logger.execution("--------- Start ----------")
        self.logger.debug(f"Getting template {template}")

        try:
            default = resources.files("hermes.Resources").joinpath(*template.split("."),"jsonForm.json")
            basicTemplate = loadJSON(default.read_text())
        except FileNotFoundError:
            fl = [x for x in resources.files("hermes.Resources").glob(f"{template.replace('.',os.path.sep)}*")]
            if len(fl) == 0:
                raise FileNotFoundError(f"{template} node found in {resources.files('hermes.Resources')}")
            else:
                 basicTemplate = loadJSON(fl[0].read_text())

        self._subsituteTemplates(basicTemplate)

        return basicTemplate


    def _subsituteTemplates(self,basicTemplate):
        self.logger.execution(f"Process {basicTemplate}")
        if 'Template' in basicTemplate.keys():
            self.logger.debug(f"Replacing template in {basicTemplate} ")
            ret =  "Done" #self.getTemplate(basicTemplate['Template'])
        else:
            for key,value in basicTemplate.items():
                self.logger.debug(f"processing {key}->{value}")
                if isinstance(value,dict):
                    basicTemplate[key] = self._subsituteTemplates(value)
            ret = basicTemplate

        self.logger.debug(f"Finish -> {ret}")
        return ret

