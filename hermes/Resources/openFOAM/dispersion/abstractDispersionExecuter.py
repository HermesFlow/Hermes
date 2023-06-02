from ...general import jinjaTransform

class abstractDispersionExecuter(jinjaTransform):
    _templateName = None

    def __init__(self,JSON,templateName):
        super().__init__(JSON)
        self.templateName =f"openFOAM/dispersion/{templateName}/jinjaTemplate"


    def run(self, **inputs):


        template = self._getTemplate(self.templateName)

        # render jinja for the choosen template
        output = template.render(**inputs)
        return dict(openFOAMfile=output)

