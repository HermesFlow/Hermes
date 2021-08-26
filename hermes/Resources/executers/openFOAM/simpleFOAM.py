from ..jinjaExecuters import jinjaExecuter

class CopenFOAM():
    '''
        will transform openFOAM from JSON structure
        to openFOAM structure   '''

    _mapping = None  # holds the mapping of the [task type]->luigiTaskTransform.

    def __init__(self):
        self._mapping = {} # dict(spanParameters=pydoc.locate("Hermes.transform.spanParameters")())

    def _getTransformaer(self, OFnode):
        # define the path to the class
        str1= OFnode +".C_transform"

        # get the class
        C_trns=pydoc.locate(str1)

        # return the class
        return self._mapping.get(OFnode,C_trns())


    def buildOpenFOAM(self,openFOAMjson):

        # define new dict hold the transformed string data
        openFOAMString = {}

        # loop all the nodes need to be tranform
        for nodename, nodeList in openFOAMjson['files'].items():

            # get the class of the specific node
            transformer = self._getTransformaer(nodename)

            # send the json string to the specific transformer. save the data in the new transform dict.
            openFOAMString[nodeList['name']] = transformer.transform(nodeList['values'])

        return openFOAMString


class transportPropertiesExecuter(jinjaExecuter):

    def run(self, **inputs):
        templateName = "openFOAM/simpleFOAM/transportProperties"
        template = self._getTemplate(templateName)

        effectiveInputs = inputs.get('values',inputs)

        output = template.render(**effectiveInputs)
        return dict(openFOAMfile=output)


class turbulenceProperties(jinjaExecuter):

    def run(self, **inputs):
        templateName = "openFOAM/simpleFOAM/turbulenceProperties"
        template = self._getTemplate(templateName)
        effectiveInputs = inputs.get('values',inputs)
        output = template.render(**effectiveInputs)
        return dict(openFOAMfile=output)
