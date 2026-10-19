import os
import shutil
from typing import Any

from ...executers.abstractExecuter import abstractExecuter


class CopyFile(abstractExecuter):

    def _defaultParameters(self):
        return dict(
            output=["Source", "Target"],
            inputs=["Source", "Target"],
            webGUI=dict(JSONSchema="webGUI/copyFile_JSONchema.json",
                        UISchema="webGUI/copyFile_UISchema.json"),
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
            shutil.copy(inputs['Source'], inputs['Target']) # this will change to a flag like the other version.
        else:
            print("=============== empty ===============")

        absSource = os.path.abspath(inputs["Source"])
        absTarget = os.path.abspath(inputs["Target"])

        return dict(Source =absSource,Target=absTarget)
