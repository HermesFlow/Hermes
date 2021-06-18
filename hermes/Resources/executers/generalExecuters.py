from .abstractExecuter import abstractExecuter
import os
import errno
import json

class parameterExecuter(abstractExecuter):

    def _defaultParameters(self):
        return dict(
            output=[],
            inputs=[],
            webGUI=dict(JSONSchema=None,
                        UISchema  =None),
            parameters={}
        )

    def run(self, **inputs):
        return dict(parameterExecuter="parameterExecuter")


class transformTemplateExecuter(abstractExecuter):

    def _defaultParameters(self):
        return dict(
            output=["transformed"],
            inputs=["template","templatedir"],
            webGUI=dict(JSONSchema=None,
                        UISchema  =None),
            parameters={}
        )

    def run(self, **inputs):
        return dict(transformTemplate="transformTemplate")


class FilesWriterExecuter(abstractExecuter):

    def __init__(self, tskJSON):
        pass

    def _defaultParameters(self):
        return dict(
            output=["status"],
            inputs=["classpath", "function"],
            webGUI=dict(JSONSchema="webGUI/FilesWriter_JSONchema.json",
                        UISchema="webGUI/FilesWriter_UISchema.json"),
            parameters={}
        )

    def run(self, **inputs):

        path = inputs["casePath"]
        files = inputs["Files"]

        for filename, file in files.items():

            newPath = os.path.join(path, filename)

            if not os.path.exists(os.path.dirname(newPath)):
                try:
                    os.makedirs(os.path.dirname(newPath))
                except OSError as exc:  # Guard against race condition
                    if exc.errno != errno.EEXIST:
                        raise
            with open(newPath, "w") as newfile:
                newfile.write(file)

