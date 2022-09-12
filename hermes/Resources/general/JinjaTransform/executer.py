from ...executers.abstractExecuter import abstractExecuter
import shutil
import os, sys, stat

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

        templatePath = [os.path.join(pathlib.Path(__file__).parent.absolute(), "jinjaTemplates")] + list(additionalTemplatePath)

        tmp_path = os.path.join(pathlib.Path(__file__).parent.absolute(), "jinjaTemplates")
        print("tmp_path = " + str (tmp_path) + "\n")
        print("additionalTemplatePath = " + str(additionalTemplatePath) + "\n")
        print("templatePath = " + str (templatePath) + "\n")
        print("templateName = " + templateName + "\n")

        file_loader = FileSystemLoader(templatePath)
        env = Environment(loader=file_loader)
        return env.get_template(templateName)
