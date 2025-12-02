from ...executers.abstractExecuter import abstractExecuter
import pathlib
from jinja2 import Environment, FileSystemLoader, TemplateNotFound
import os
import logging
import copy

class JinjaTransform(abstractExecuter):

    def _defaultParameters(self):
        return dict(
            output=["status"],
            inputs=["classpath", "function"],
            webGUI=dict(JSONSchema="webGUI/jinjaExecuter_JSONchema.json",
                        UISchema="webGUI/jinjaExecuter_UISchema.json"),
            parameters={}
        )

    def _resources_root(self):
        """
        Resolve the resources root directory (where templates live).
        Prefer package-relative Resources directory, else fallback to legacy hardcoded path.
        """
        # file path: .../hermes/Resources/general/JinjaTransform/executer.py
        here = pathlib.Path(__file__).resolve()
        # climb up to hermes/Resources (parents: executer.py -> JinjaTransform -> general -> Resources)
        candidate = here.parent.parent.parent.parent / "Resources"
        if candidate.exists():
            return str(candidate)

        return None

    def _getTemplate(self, templateName):
        """
        Create jinja environment and get template by name.
        templateName is relative to Resources/ (e.g. openFOAM/system/FvSchemes/jinjaTemplate.v2
        or openFOAM/system/FvSchemes/jinjaTemplate for v1).
        """
        resources_root = self._resources_root()
        env = Environment(
            loader=FileSystemLoader(resources_root),
            trim_blocks=True,
            lstrip_blocks=True
        )
        try:
            return env.get_template(templateName)
        except TemplateNotFound as e:
            # re-raise with helpful message
            raise TemplateNotFound(f"Template '{templateName}' not found in search path: '{resources_root}'") from e

    def run(self, **inputs):
        """
        Run the transform. Accepts:
         - template (optional) : explicit template name (v1 usage)
         - parameters (optional): parameters dict to render with (v1 usage)
        For v2 nodes, reads top-level 'type' and 'Execution.input_parameters' and renders using
        <type-with-dots-replaced>/jinjaTemplate.v2
        """
        logger = logging.getLogger("JinjaTransform")
        # inputs may be empty (we often call JinjaTransform(self._JSON).run(template=..., parameters=...))
        inputs = inputs or {}

        # Determine version and type
        logger.debug(f"[JinjaTransform] Detected version: {self.version}; top-level type: {self.executerType}")
        type_path = self.executerType.replace(".", os.path.sep)
        if self.version >= 2:
            # Version 2: use type -> path/jinjaTemplate.v2
            # convert dot path to folder path and build template file name
            template_name = f"{type_path}/jinjaTemplate.v2"
        else:
            template_name = f"{type_path}/jinjaTemplate"

        values = inputs
        # ctx = {}
        # if isinstance(parameters, dict):
        #     ctx.update(parameters)
        #
        #     # Promote known nested keys to top-level in context
        #     nested_keys_to_promote = [
        #         "fields",
        #         "default",
        #         "values",
        #         "solverProperties",
        #         "relaxationFactors",
        #         "parameters"
        #     ]
        #
        #     for key in nested_keys_to_promote:
        #         if key not in ctx:
        #             val = parameters.get(key)
        #             if isinstance(val, dict):
        #                 ctx[key] = val
        #
        # # Always fallback defaults for robustness
        # ctx.setdefault("solverProperties", {})
        # ctx.setdefault("fields", {})
        # ctx.setdefault("default", {})
        # ctx.setdefault("values", parameters if isinstance(parameters, dict) else {})
        # ctx.setdefault("parameters", parameters)
        # ctx.setdefault("input_parameters", parameters)
        #
        # # Add top-level metadata
        # ctx.setdefault("type", self.executerType)
        # ctx.setdefault("version", self.version)
        # logger.debug(f"[JinjaTransform] Final rendering context keys: {sorted(ctx.keys())}")

        # Get template and render
        template = self._getTemplate(template_name)
        try:
            # import pprint
            # logger.debug("[JinjaTransform] Context passed to template:\n" + pprint.pformat(ctx))
            output = template.render(**values)
        except Exception as e:
            # Log with context for easier debugging
            logger.error(f"[JinjaTransform] Template render failed: {e}")
            # optional: attach a snippet of the context keys
            logger.debug(f"[JinjaTransform] Context (shallow): { {k: type(v).__name__ for k,v in ctx.items()} }")
            raise

        logger.warning(f"[DEBUG-JT] Node type: {self.executerType}, Version: {self.version}")

        return dict(openFOAMfile=output)
