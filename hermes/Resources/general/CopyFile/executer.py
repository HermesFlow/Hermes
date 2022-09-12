from ...executers.abstractExecuter import abstractExecuter
import shutil
import os, sys, stat

class CopyFileExecuter(abstractExecuter):

    def _defaultParameters(self):
        return dict(
            output=["status"],
            inputs=["source", "target"],
            webGUI=dict(JSONSchema="webGUI/copyFile_JSONchema.json",
                        UISchema="webGUI/copyFile_UISchema.json"),
            parameters={}
        )

    def run(self, **inputs):
            if (len(inputs["Source"]) > 0 and len(inputs["Target"]) > 0):
                shutil.copy(inputs['Source'], inputs['Target']) # this will change to a flag like the other version.
            else:
                print("=============== empty ===============")

            absSource = os.path.abspath(inputs["Source"])
            absTarget = os.path.abspath(inputs["Target"])

            return dict(copyField="copyFile",Source =absSource,Target=absTarget)
