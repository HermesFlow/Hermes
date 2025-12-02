from ...general import JinjaTransform
import logging

# abstractSystemExecuter.py
class abstractSystemExecuter(JinjaTransform):
    def __init__(self, JSON, templateName=None, full_workflow=None):
        workflow = full_workflow or JSON.get("workflowJSON") or JSON.get("workflow")
        super().__init__(JSON, full_workflow=workflow)
        self._templateName = f"openFOAM/system/{templateName}/jinjaTemplate" if templateName else None

    def run(self, **inputs):
        return super().run(template=self._templateName, parameters=self._JSON.get("Execution", {}).get("input_parameters"))
