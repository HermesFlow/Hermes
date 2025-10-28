from ...executers.abstractExecuter import abstractExecuter
import pathlib
from jinja2 import Environment, FileSystemLoader, TemplateNotFound
import os
import logging
import copy

class JinjaTransform(abstractExecuter):

    def __init__(self, JSON):
        super().__init__(JSON)
        # store original JSON (node JSON as passed) for version/type lookup
        self._JSON = JSON

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

        fallback = "/Users/sapiriscfdc/Costumers/Hermes/Hermes/hermes/Resources"
        return fallback

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

    def _resolve_version_and_type(self, inputs):
        """
        Return (version, node_type, template_name_source)
         - version: int
         - node_type: e.g. 'openFOAM.system.FvSchemes' (may come from top-level or Execution)
         - template_name_source: final resolved template name (may still be None for v1)
        """
        # priority: explicit inputs (parameters/template) -> Execution.* -> top-level JSON
        # Version: prefer top-level 'version' (your workflow uses that)
        version = None
        # If caller passed a parameters dict which includes version, respect it:
        parameters_from_inputs = inputs.get("parameters") if inputs else None

        # Top-level version
        if isinstance(self._JSON, dict) and "version" in self._JSON:
            try:
                version = int(self._JSON["version"])
            except Exception:
                version = 1

        # If Execution has a version (older layout)
        if version is None:
            exec_ver = (self._JSON.get("Execution") or {}).get("version")
            if exec_ver is not None:
                try:
                    version = int(exec_ver)
                except Exception:
                    version = 1

        # If still None, default to 1
        if version is None:
            version = 1

        # Resolve node type: check Execution.type then top-level type
        node_type = None
        if isinstance(self._JSON, dict):
            node_type = (self._JSON.get("Execution") or {}).get("type")
            if not node_type:
                node_type = self._JSON.get("type")

        return version, node_type

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
        version, node_type = self._resolve_version_and_type(inputs)
        logger.debug(f"[JinjaTransform] Detected version: {version}; top-level type: {node_type}")

        # Resolve template name
        template_name = None

        if version == 2:
            # Version 2: use type -> path/jinjaTemplate.v2
            if not node_type:
                raise ValueError("[JinjaTransform] Missing 'type' for version 2 node (looked in top-level and Execution)")
            # convert dot path to folder path and build template file name
            type_path = node_type.replace(".", "/")
            template_name = f"{type_path}/jinjaTemplate.v2"
            # parameters come from Execution.input_parameters if present, else fallback to top-level node JSON
            execution_params = (self._JSON.get("Execution") or {}).get("input_parameters")
            if execution_params is None:
                # fallback: some nodes may put input parameters at top-level (defensive)
                execution_params = self._JSON.get("input_parameters") or {}
            parameters = copy.deepcopy(execution_params) if isinstance(execution_params, dict) else {}
            logger.debug(f"[JinjaTransform] Version 2: template_name='{template_name}', parameters keys={list(parameters.keys())}")
        else:
            # Version 1: template should be passed in inputs
            template_name = inputs.get("template")
            parameters = inputs.get("parameters", self._JSON)
            if not template_name:
                raise ValueError("[JinjaTransform] No template provided for version 1")
            logger.debug(f"[JinjaTransform] Version 1: template_name='{template_name}'")

        # Build a rendering context that is tolerant to templates expecting different variable shapes.
        # Parameters is the dict with input parameters; some templates read 'default' & 'fields', some use
        # a 'values' wrapper, others expect keys at top-level. Provide all common shapes.
        if not isinstance(parameters, dict):
            logger.warning("[JinjaTransform] parameters is not a dict; coercing to empty dict")
            parameters = {}

        ctx = {}

        if isinstance(parameters, dict):
            ctx.update(parameters)

            # Promote known nested keys to top-level in context
            nested_keys_to_promote = [
                "fields",
                "default",
                "values",
                "solverProperties",
                "relaxationFactors",
                "parameters"
            ]

            for key in nested_keys_to_promote:
                if key not in ctx:
                    val = parameters.get(key)
                    if isinstance(val, dict):
                        ctx[key] = val

        # Always fallback defaults for robustness
        ctx.setdefault("solverProperties", {})
        ctx.setdefault("fields", {})
        ctx.setdefault("default", {})
        ctx.setdefault("values", parameters if isinstance(parameters, dict) else {})
        ctx.setdefault("parameters", parameters)
        ctx.setdefault("input_parameters", parameters)

        # Add top-level metadata
        if isinstance(self._JSON, dict):
            ctx.setdefault("type", self._JSON.get("type"))
            ctx.setdefault("version", self._JSON.get("version"))

        logger.debug(f"[JinjaTransform] Final rendering context keys: {sorted(ctx.keys())}")


        # Get template and render
        template = self._getTemplate(template_name)
        try:
            import pprint
            logger.debug("[JinjaTransform] Context passed to template:\n" + pprint.pformat(ctx))

            output = template.render(**ctx)
        except Exception as e:
            # Log with context for easier debugging
            logger.error(f"[JinjaTransform] Template render failed: {e}")
            # optional: attach a snippet of the context keys
            logger.debug(f"[JinjaTransform] Context (shallow): { {k: type(v).__name__ for k,v in ctx.items()} }")
            raise

        logger.warning(f"[DEBUG-JT] Node type: {node_type}, Version: {version}")

        return dict(openFOAMfile=output)
