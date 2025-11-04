from ...executers.abstractExecuter import abstractExecuter
import errno
import json
import os, sys, stat

class FilesWriter(abstractExecuter):

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

        workdir = inputs["directoryPath"]
        if workdir is None:
            workdir = os.getcwd()

        path = os.path.join(workdir,inputs["casePath"])
        files = inputs["Files"]

        createdFiles = dict()
        for groupName, groupData in files.items():
            # make sure that the user input is regarded as a directory in case of input dict file.
            fileContent = groupData['fileContent']
            fileName    = groupData['fileName']

            # If fileContent is a dict, treat it as a directory of multiple files
            # But don't append '/' – just make sure fileName is a directory name
            is_multi_file = isinstance(fileContent, dict)

            newPath = os.path.join(path, fileName)

            # Create directories
            if is_multi_file:
                os.makedirs(newPath, exist_ok=True)
            else:
                os.makedirs(os.path.dirname(newPath), exist_ok=True)

            # Handle file writing
            if is_multi_file:
                outputFiles = []
                for filenameItr, fileContentValue in fileContent.items():
                    finalFileName = os.path.join(newPath, filenameItr)
                    with open(finalFileName, "w") as newfile:
                        newfile.write(fileContentValue)
                    outputFiles.append(finalFileName)
            else:
                with open(newPath, "w") as newfile:
                    newfile.write(fileContent)
                outputFiles = newPath

            createdFiles[groupName] = outputFiles


        return dict(fileWriterTemplate="fileWriterTemplate",
                    files=createdFiles)
