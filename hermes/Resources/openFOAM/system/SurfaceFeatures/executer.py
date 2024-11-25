from ..abstractSystemExecuter import abstractSystemExecuter

class SurfaceFeatures(abstractSystemExecuter):

    def __init__(self,JSON):
        super().__init__(JSON,"SurfaceFeatures")

    def run(self, **inputs):
        template = self._getTemplate(self.templateName)

        retFiles ={}
        if isinstance(inputs['geometryData'],str):
            import json
            geometryData = json.loads(inputs['geometryData'].replace('"',"").replace("'",'"'))
        else:
            geometryData = inputs['geometryData']

        OFversion = inputs.get("OFversion","of10")

        for objectName,objectData in geometryData.items():
            retFiles[objectName] = template.render(nonManifoldEdges=inputs['nonManifoldEdges'],
                                                   openEdges=inputs['openEdges'],
                                                   geometryData=objectData,
                                                   includeAngle=inputs['includeAngle'],
                                                   OFversion=OFversion)

        return dict(openFOAMfile=retFiles)

