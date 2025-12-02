from ...executers.abstractExecuter import abstractExecuter
import pathlib
from jinja2 import Environment, FileSystemLoader, TemplateNotFound
import os
import logging
import copy
import numpy as np
import re

# --- Setup logger explicitly ---
logger = logging.getLogger("JinjaTransform")
logger.setLevel(logging.DEBUG)

if not logger.handlers:
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('[%(levelname)s] %(name)s: %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

# --- Main Class ---
class JinjaTransform(abstractExecuter):
    def __init__(self, JSON, full_workflow=None):
        super().__init__(JSON)
        self._JSON = JSON

        # Auto-infer full workflow
        if full_workflow is None:
            full_workflow = JSON.get("workflowJSON") or JSON.get("workflow") or {}

        self._workflow = full_workflow
        logger.debug(f"[Init] Full workflow version: {self._workflow.get('workflow', {}).get('version')}")

    def _defaultParameters(self):
        return dict(
            output=["status"],
            inputs=["classpath", "function"],
            webGUI=dict(
                JSONSchema="webGUI/jinjaExecuter_JSONchema.json",
                UISchema="webGUI/jinjaExecuter_UISchema.json"
            ),
            parameters={}
        )

    def _resources_root(self):
        here = pathlib.Path(__file__).resolve()
        for parent in here.parents:
            if (parent / "general").exists() and (parent / "openFOAM").exists():
                return str(parent)
        raise FileNotFoundError("Could not locate 'Resources' root directory.")

    def _getTemplate(self, template_name: str, additionalTemplatePath=None):
        search_paths = [self._resources_root()]
        if additionalTemplatePath:
            search_paths = additionalTemplatePath + search_paths

        env = Environment(
            loader=FileSystemLoader(search_paths),
            trim_blocks=True,
            lstrip_blocks=True
        )

        try:
            return env.get_template(template_name)
        except TemplateNotFound as e:
            raise TemplateNotFound(
                f"Template '{template_name}' not found in: {search_paths}"
            ) from e

    def _resolve_version_and_type(self) -> tuple[int, str | None]:
        version = self._workflow.get("workflow", {}).get("version")
        node_type = (self._JSON.get("Execution") or {}).get("type") or self._JSON.get("type")
        logger.debug(f"[resolve_version_and_type] Detected version={version}, type={node_type}")
        return version, node_type

    def run(self, **inputs):
        version, node_type = self._resolve_version_and_type()
        ctx = {}

        if version == 2:
            # Use general template for version 2
            execution_params = (
                (self._JSON.get("Execution") or {}).get("input_parameters")
                or self._JSON.get("input_parameters")
                or {}
            )

            if not isinstance(execution_params, dict):
                logger.warning("[JinjaTransform] input_parameters not a dict — coercing to empty.")
                execution_params = {}

            ctx = copy.deepcopy(execution_params)
            template_name = "general/JinjaTransform/generalTemplate.jinja"
            template = self._getTemplate(template_name)
            logger.debug(f"[run] Using general template for version=2: {template_name}")

        else:
            # Use classic node-specific template
            template_name = inputs.get("template")
            if not template_name:
                raise ValueError("[JinjaTransform] No template provided for classic workflow")

            path_list = [os.path.abspath(p) for p in np.atleast_1d(inputs.get("path", []))]
            path_list.append(os.getcwd())

            regexPattern = '|'.join(map(re.escape, [".", "/", "\\"]))
            parts = re.split(regexPattern, template_name)
            normalized_template_path = os.path.sep.join(parts)

            ctx = inputs.get("parameters", {})
            if not isinstance(ctx, dict):
                logger.warning("[JinjaTransform] parameters not a dict — coercing to empty.")
                ctx = {}

            template = self._getTemplate(normalized_template_path, additionalTemplatePath=path_list)
            logger.debug(f"[run] Using classic template: {normalized_template_path}")

        # Add aliases
        for alias in ["input_parameters", "parameters", "values"]:
            if alias not in ctx:
                ctx[alias] = copy.deepcopy(ctx)

        default_object = (node_type or "defaultDict").split(".")[-1]
        ctx.setdefault("FoamFile", {
            "format": "ascii",
            "class": "dictionary",
            "object": default_object
        })

        ctx.setdefault("type", node_type)
        ctx.setdefault("version", version)
        #ctx.setdefault("fields", {})
        #ctx.setdefault("solverProperties", {})

        try:
            output = template.render(**ctx)
        except Exception as e:
            logger.error(f"[JinjaTransform] Template render failed: {e}")
            raise

        logger.info(f"[JinjaTransform] Rendered for type={node_type}, version={version}")
        return dict(openFOAMfile=output)
