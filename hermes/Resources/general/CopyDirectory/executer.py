from ...executers.abstractExecuter import abstractExecuter
import shutil
import os, sys, stat

class CopyDirectoryExecuter(abstractExecuter):

    def _defaultParameters(self):
        return dict(
            output=["status"],
            inputs=["source","target"],
            webGUI=dict(JSONSchema="webGUI/copyDirectory_JSONchema.json",
                        UISchema  = "webGUI/copyDirectory_UISchema.json"),
            parameters={}
        )

    def run(self, **inputs):
        if (len(inputs["Source"]) > 0 and len(inputs["Target"]) > 0):
            shutil.copytree(inputs['Source'],inputs['Target'],dirs_exist_ok=inputs.get("dirs_exist_ok",True))
        else:
            print("=============== empty ===============")

        absSource = os.path.abspath(inputs["Source"])
        absTarget = os.path.abspath(inputs["Target"])

        return dict(copyDirectory="copyDirectory",
                    Source =absSource,Target=absTarget)