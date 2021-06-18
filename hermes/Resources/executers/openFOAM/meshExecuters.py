from ..jinjaExecuters import jinjaExecuter
import os
import errno
import json
import re

class BlockMeshExecuter(jinjaExecuter):
    """
        Transforms JSON->blockMeshDict using the jinja template in jinjaTemplates.openFOAM.mesh.BlockMesh

        The JSON format is:

        {
            "geometry": {
                    "convertToMeters" : "...",
                    "cellCount" : (50,50,30)
                    "grading" : {
                        "x"
                        "y"
                        "z"
                    }
            },
            "boundary" : [
                {
                    "Name" : "...",
                    "Type" : (wall|patch|cyclic|symmetry)
                    "faces" : [
                        (1,2,3),
                        (4,5,6),
                        ...
                    ],
                    "neighbourPatch" : ".."  # only if Type is cyclic.
                },....
            ],
            vertices : [
                (0,0,0),
                (0,1,2),
                (1,1,2),
                   .
                   .
                   .
            ]
        }


Noga:
    We should talk about when (and how) the FreeCAD webGUI is translated to this JSON.

    I think that the 'run' method should be sufficiently smart to identify
    an alternative JSON that arrives from the webGUI and then just translate it.
    I suggest that you would send me the JSON format of the webGUI and then we can discuss about how to convert it.

"""

    def _defaultParameters(self):
        return dict(
            output=["status"],
            inputs=["classpath", "function"],
            webGUI=dict(JSONSchema="webGUI/BlockMeshExecuter_JSONchema.json",
                        UISchema="webGUI/BlockMeshExecuter_UISchema.json"),
            parameters={}
        )

    def run(self, **inputs):

        # get the  name of the template
        templateName = "openFOAM/mesh/BlockMesh"
        # templateName = os.path.abspath(templateName)

        ## Noga:
        # 1. Check here if inputs['geometry'] is from webGUI. if it is: convert to the right form
        # 2. Check here if inputs['boundary'] is from webGUI. if it is: convert to the right form
        # 3. Check here if inputs['vertices'] is from webGUI. if it is: convert to the right form


        # get the values to update in the template
        geometry = inputs['geometry']
        boundary = inputs['boundary']
        vertices = inputs['vertices']

        template = self._getTemplate(templateName)

        # render jinja for the choosen template
        output = template.render(geometry = geometry, boundary = boundary, vertices = vertices)

        return dict(openFOAMfile=output)
