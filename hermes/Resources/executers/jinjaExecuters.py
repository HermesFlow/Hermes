import os
import re
import pathlib
from jinja2 import FileSystemLoader, Environment
from hermes.Resources.executers.abstractExecuter import abstractExecuter

# *************************************************************
class jinjaExecuter(abstractExecuter):



    def _defaultParameters(self):
        return dict(
            output=["status"],
            inputs=["classpath", "function"],
            webGUI=dict(JSONSchema="webGUI/jinjaExecuter_JSONchema.json",
                        UISchema="webGUI/jinjaExecuter_UISchema.json"),
            parameters={}
        )

    def _getTemplate(self,templateName,additionalTemplatePath=[]):
        templatePath = [os.path.join(pathlib.Path(__file__).parent.absolute(), "jinjaTemplates")] + additionalTemplatePath
        file_loader = FileSystemLoader(templatePath)
        env = Environment(loader=file_loader)
        return env.get_template(templateName)

    def run(self, **inputs):
        # get the  name of the template
        templateName = inputs['jinjaTemplate']

        # make sure the splits are with slash
        delimiters = ".", "/"
        regexPattern = '|'.join(map(re.escape, delimiters))
        spltList = re.split(regexPattern, templateName)
        templateName = '/'.join(spltList)

        # get the values to update in the template
        values = inputs['jinjaParameters']

        template = self._getTemplate(templateName)

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