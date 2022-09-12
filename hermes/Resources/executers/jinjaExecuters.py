import os
import re
import pathlib

import numpy
from jinja2 import FileSystemLoader, Environment
from hermes.Resources.executers.abstractExecuter import abstractExecuter

# *************************************************************

    def run(self, **inputs):
        # get the  name of the template
        templateName = inputs['template']
        additionalTemplatePath = [os.path.abspath(x) for x in numpy.atleast_1d(inputs.get("path",[]))]

        # make sure the splits are with slash
        delimiters = ".", "/"
        regexPattern = '|'.join(map(re.escape, delimiters))
        spltList = re.split(regexPattern, templateName)
        templateName = '/'.join(spltList)

        # get the values to update in the template
        values = inputs['parameters']

        template = self._getTemplate(templateName,additionalTemplatePath=additionalTemplatePath)

        # render jinja for the choosen template
        output = template.render(**values)

        return dict(openFOAMfile=output)


class GeometryDefinerExecuter(abstractExecuter):

    def _defaultParameters(self):
        return dict(
            output=[],
            inputs=[],
            webGUI=dict(JSONSchema=None,
                        UISchema=None),
            parameters={}
        )

    def run(self, **inputs):
        return dict(GeometryDefinerExecuter="GeometryDefinerExecuter")