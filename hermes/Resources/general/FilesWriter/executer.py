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

            if isinstance(fileContent,dict) and fileName[-1] != '/':
                fileName = f"{fileName}/"

            newPath = os.path.join(path, fileName)
            if not os.path.exists(os.path.dirname(newPath)):
                try:
                    os.makedirs(os.path.dirname(newPath),exist_ok=True)
                except OSError as exc:  # Guard against race condition
                    if exc.errno != errno.EEXIST:
                        raise
            try:
                # Check if it is a dict - e.g a list of files.
                fileContentParsed = json.loads(fileContent[1:-1].replace('"','\\"').replace("'",'"'))
            except json.decoder.JSONDecodeError as e:
                fileContentParsed = fileContent


            if isinstance(fileContentParsed,dict):
                outputFiles =[]
                for filenameItr,fileContent in fileContentParsed.items():
                    finalFileName = os.path.join(newPath,filenameItr)
                    with open(finalFileName, "w") as newfile:
                        newfile.write(fileContent)

                    outputFiles.append(finalFileName)
            else:
                outputFiles = newPath
                with open(newPath, "w") as newfile:
                    newfile.write(fileContentParsed)

            createdFiles[groupName] = outputFiles


        return dict(fileWriterTemplate="fileWriterTemplate",
                    files=createdFiles)
