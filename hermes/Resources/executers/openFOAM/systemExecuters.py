from ..jinjaExecuters import jinjaExecuter


class systemFileExecuter(jinjaExecuter):
    def __init__(self,JSON,templateName):
        super().__init__(JSON)
        self.templateName =f"openFOAM/system/{templateName}"

    def run(self, **inputs):
        template = self._getTemplate(self.templateName)
        output = template.render(**inputs)
        return dict(openFOAMfile=output)

class decomposeParExecuter(systemFileExecuter):
    def __init__(self,JSON):
        super().__init__(JSON,"decomposePar")

class controlDictExecuter(systemFileExecuter):

    def __init__(self,JSON):
        super().__init__(JSON,"controlDict")

class fvSchemesExecuter(systemFileExecuter):

    def __init__(self,JSON):
        super().__init__(JSON,"fvSchemes")

class fvSolutionExecuter(systemFileExecuter):


    def __init__(self,JSON):
        super().__init__(JSON,"fvSolution")

class changeDictionaryExecuter(systemFileExecuter):

    def __init__(self,JSON):
        super().__init__(JSON,"changeDictionary")


class surfaceFeaturesDictExecuter(systemFileExecuter):

    def __init__(self,JSON):
        super().__init__(JSON,"surfaceFeaturesDict")

    def run(self, **inputs):
        template = self._getTemplate(self.templateName)

        retFiles ={}

        for objectName,objectData in inputs['geometryData'].items():
            retFiles[objectName] = template.render(nonManifoldEdges=inputs['nonManifoldEdges'],openEdges=inputs['openEdges'],geometryData=objectData)
        return dict(openFOAMfile=retFiles)



