import os
import re
import pathlib
from jinja2 import FileSystemLoader, Environment
#from abstractExecuter import abstractExecuter
from hermes.Resources.executers.abstractExecuter import abstractExecuter

# *************************************************************
class jinjaExecuter(abstractExecuter):

    # def __init__(self):
    #     pass
    #     # get the user working dir
    #     self.u_wd = os.getcwd()
    #
    #     # define executer as the current working directory
    #     HermesDirpath = os.getenv('HERMES_2_PATH')
    #     cwd=HermesDirpath+"/hermes/Resources/executers"
    #     os.chdir(cwd)
    #
    #     # update 'pathFile' to full path- absolute
    #     self.templates = os.path.abspath("templates")

    def _defaultParameters(self):
        return dict(
            output=["status"],
            inputs=["classpath", "function"],
            webGUI=dict(JSONSchema="webGUI/jinjaExecuter_JSONchema.json",
                        UISchema="webGUI/jinjaExecuter_UISchema.json"),
            parameters={}
        )

    def run(self, **inputs):
        # get the  name of the template
        templateName = inputs['template']
        # templateName = os.path.abspath(templateName)

        # make sure the splits are with slash
        delimiters = ".", "/"
        regexPattern = '|'.join(map(re.escape, delimiters))
        spltList = re.split(regexPattern, templateName)
        templateName = '/'.join(spltList)

        print(inputs)
        print("*************************")
        # get the values to update in the template
        values = inputs['values']

        # define the environment - in this case : templates directory
#        file_loader = FileSystemLoader(self.templates)
        file_loader = FileSystemLoader(os.path.join(pathlib.Path(__file__).parent.absolute(), "jinjaTemplates"))
        env = Environment(loader=file_loader)
        print(os.path.join(pathlib.Path(__file__).parent.absolute(), "jinjaTemplates"))

        # Define the template to use
        template = env.get_template(templateName)

        # render jinja for the choosen template
        output = template.render(values=values)

        return dict(openFOAMfile=output)

# *************************************************************
class BlockMeshExecuter(abstractExecuter):

    # def __init__(self):
    #     pass

    def _defaultParameters(self):
        return dict(
            output=["status"],
            inputs=["classpath", "function"],
            webGUI=dict(JSONSchema="webGUI/BlockMeshExecuter_JSONchema.json",
                        UISchema="webGUI/BlockMeshExecuter_UISchema.json"),
            parameters={}
        )

    def run(self, **inputs):

        # get the  name of the template
        templateName = inputs['template']
        # templateName = os.path.abspath(templateName)

        # make sure the splits are with slash
        delimiters = ".", "/"
        regexPattern = '|'.join(map(re.escape, delimiters))
        spltList = re.split(regexPattern, templateName)
        templateName = '/'.join(spltList)

        # get the values to update in the template
        Properties = inputs['Properties']
        boundary = inputs['boundary']
        vertices = inputs['vertices']

        # define the environment - in this case : templates directory
#        file_loader = FileSystemLoader(self.templates)
        file_loader = FileSystemLoader(os.path.join(pathlib.Path(__file__).parent.absolute(), "jinjaTemplates"))
        env = Environment(loader=file_loader)
        # print(os.path.join(pathlib.Path(__file__).parent.absolute(), "templates"))

        # Define the template to use
        template = env.get_template(templateName)

        # render jinja for the choosen template
        output = template.render(Properties = Properties, boundary = boundary, vertices = vertices)

        return dict(openFOAMfile=output)

# *************************************************************
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