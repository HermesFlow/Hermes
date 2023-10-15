from ...executers.abstractExecuter import abstractExecuter
import os
import re
import pathlib

import numpy
from jinja2 import FileSystemLoader, Environment

class JinjaTransform(abstractExecuter):

    def _defaultParameters(self):
        return dict(
            output=["status"],
            inputs=["classpath", "function"],
            webGUI=dict(JSONSchema="webGUI/jinjaExecuter_JSONchema.json",
                        UISchema="webGUI/jinjaExecuter_UISchema.json"),
            parameters={}
        )

    def _getTemplate(self,templateName,additionalTemplatePath=[]):

        templatePath = [pathlib.Path(__file__).parent.parent.parent.absolute()] + list(additionalTemplatePath)
        file_loader = FileSystemLoader(templatePath)
        env = Environment(loader=file_loader)
        return env.get_template(templateName)


    def run(self, **inputs):
        # get the  name of the template
        templateName = inputs['template']
        additionalTemplatePath = [os.path.abspath(x) for x in numpy.atleast_1d(inputs.get("path",[]))]
        additionalTemplatePath.append(os.getcwd())

        # make sure the splits are with slash
        delimiters = ".", "/", "\\"
        regexPattern = '|'.join(map(re.escape, delimiters))
        spltList = re.split(regexPattern, templateName)
        templateName = os.path.sep.join(spltList)

        # get the values to update in the template
        values = inputs['parameters']

        template = self._getTemplate(templateName,additionalTemplatePath=additionalTemplatePath)

        # render jinja for the choosen template
        output = template.render(**values)

        return dict(renderedText=output)
