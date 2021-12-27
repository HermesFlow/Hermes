from ..jinjaExecuters import jinjaExecuter
import os
import errno
import json
import re

class kinematicCloudPropertiesExecuter(jinjaExecuter):

    def run(self, **inputs):
        template = self._getTemplate("openFOAM/kinematicCloudProperties/kinematicCloudProperties")
        output = template.render(**inputs)
        return dict(openFOAMfile=output)
