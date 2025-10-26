from ...general.JinjaTransform.executer import JinjaTransform
import logging

class abstractSystemExecuter(JinjaTransform):
    def __init__(self, JSON, templateName):
        super().__init__(JSON)
        self.templateName = templateName
        self._JSON = JSON  # used by JinjaTransform

    def run(self, **executer_parameters):
        logger = logging.getLogger("abstractSystemExecuter")

        version = self._JSON.get("version", 1)
        logger.debug(f"[abstractSystemExecuter] Detected version: {version}")

        if version == 2:
            node_type = self._JSON.get("type", "")
            if not node_type:
                raise ValueError("Missing 'type' field in JSON for version 2 node")

            # Convert dot notation to folder path and add template file name
            templateName = node_type.replace(".", "/") + "/jinjaTemplate.v2"
            parameters = self._JSON.get("Execution", {}).get("input_parameters", {})
            logger.debug(f"Using version 2 template: {templateName}")

        else:
            # version 1 fallback
            templateName = f"openFOAM/system/{self.templateName}/jinjaTemplate"
            parameters = self._JSON
            logger.debug(f"Using version 1 template: {templateName}")

        # Pass to JinjaTransform
        from hermes.Resources.general.JinjaTransform.executer import JinjaTransform
        return JinjaTransform(self._JSON).run(template=templateName, parameters=parameters)
