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

        createdFiles = dict()
        for groupName, groupData in files.items():
            # make sure that the user input is regarded as a directory in case of input dict file.

            fileContent = groupData['fileContent']
            fileName    = groupData['fileName']

            if isinstance(fileContent,dict) and fileName[-1] != '/':
                fileName = f"{fileName}/"

            newPath = os.path.join(path, fileName)

            if not os.path.exists(os.path.dirname(newPath)):
                try:
                    os.makedirs(os.path.dirname(newPath),exist_ok=True)
                except OSError as exc:  # Guard against race condition
                    if exc.errno != errno.EEXIST:
                        raise

            if isinstance(fileContent,dict):
                outputFiles =[]
                for filenameItr,fileContent in fileContent.items():
                    finalFileName = os.path.join(newPath,filenameItr)
                    with open(finalFileName, "w") as newfile:
                        newfile.write(fileContent)

                    outputFiles.append(finalFileName)
            else:
                outputFiles = newPath
                with open(newPath, "w") as newfile:
                    newfile.write(fileContent)

            createdFiles[groupName] = outputFiles


        return dict(fileWriterTemplate="fileWriterTemplate",
                    files=createdFiles)
