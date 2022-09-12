from ...general import jinjaTransform

class abstractSystemExecuter(jinjaTransform):
    def __init__(self,JSON,templateName):
        super().__init__(JSON)
        self.templateName =f"openFOAM/system/{templateName}/jinjaTemplate"
