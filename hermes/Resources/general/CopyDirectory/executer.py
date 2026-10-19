import os
import shutil
from typing import Any

from ...executers.abstractExecuter import abstractExecuter


class CopyDirectory(abstractExecuter):

    def _defaultParameters(self):
        return dict(
            output=["Source,Target"],
            inputs=["Source","Target"],
            webGUI=dict(JSONSchema="webGUI/copyDirectory_JSONchema.json",
                        UISchema  = "webGUI/copyDirectory_UISchema.json"),
            parameters={}
        )
    
    @staticmethod
    def testParamValues(params: dict[str, Any]):
        for param in ["Source", "Target"]:
            passed, status_message = abstractExecuter.checkParamType(params, param, str, required=True)
            if not passed:
                return passed, status_message

        return True, ""

    def run(self, **inputs):
        if (len(inputs["Source"]) > 0 and len(inputs["Target"]) > 0):
            shutil.copytree(inputs['Source'],inputs['Target'],dirs_exist_ok=inputs.get("dirs_exist_ok",True))
        else:
            print("=============== empty ===============")

        absSource = os.path.abspath(inputs["Source"])
        absTarget = os.path.abspath(inputs["Target"])

        return dict(Source =absSource,Target=absTarget)