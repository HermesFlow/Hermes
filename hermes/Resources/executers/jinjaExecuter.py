import os
import string
import re
from jinja2 import FileSystemLoader, Environment
from abstractExecuter import abstractExecuter


class jinjaExecuter(abstractExecuter):

    def __init__(self):
        # update 'pathFile' to full path- absolute
        self.templates = os.path.abspath("templates")

    def _defaultParameters(self):
        return dict(
            output=["status"],
            inputs=["classpath", "function"],
            webGUI=dict(JSONSchema="webGUI/jinjaExecuter_JSONchema.json",
                        UISchema="webGUI/jinjaExecuter_UISchema.json"),
            parameters={}
        )

    def run(self, inputs):

        # get the  name of the template
        templateName = inputs['template']
        # templateName = os.path.abspath(templateName)


        # make sure the splits are with slash
        delimiters = ".", "/"
        regexPattern = '|'.join(map(re.escape, delimiters))
        spltList = re.split(regexPattern, templateName)
        templateName = '/'.join(spltList)

        # get the values to update in the template
        values = inputs['values']

        # define the environment - in this case : templates directory
        file_loader = FileSystemLoader(self.templates)
        env = Environment(loader=file_loader)

        # Define the template to use
        template = env.get_template(templateName)

        # render jinja for the choosen template
        output = template.render(values=values)

        # save as dict item
        D_item = {inputs['name'] : output}

        return D_item