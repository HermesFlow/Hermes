from __future__ import annotations

from PyFoam.RunDictionary.ParsedParameterFile import ParsedParameterFile
from PyFoam.Basics.DataStructures import BoolProxy
from ..Resources.reTemplateCenter import templateCenter
from ..utils.logging import get_classMethod_logger
from pathlib import Path
from typing import Any, Dict, Tuple, Optional
import json, copy, pydoc

# Json encoder
class FoamJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, BoolProxy):
            return bool(o)
        return super().default(o)

# Convert Python dictionary into a JSON
def save_json(data, save_name):
    with open(save_name, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, sort_keys=True, ensure_ascii=False, cls=FoamJSONEncoder)

#  To retrieve the correct template
def locate_class(path: str):
    try:
        return pydoc.locate(path), None
    except Exception as e:
        return None, e

# Extract Keys and Values from a dictionary and Replace or Add Keys in the JSON Structure
def merge_into(dst: Any, src: Any, list_strategy: str = "replace") -> Any:
    """
    Merge src into dst recursively. Works in-place for dicts.
    - dict + dict: recurse and insert new keys
    - list + list: replace or extend based on strategy
    - scalar + scalar or mismatched types: overwrite
    """
    if isinstance(dst, dict) and isinstance(src, dict):
        for k, v in src.items():
            if k in dst:
                dst[k] = merge_into(dst[k], v, list_strategy)
            else:
                dst[k] = copy.deepcopy(v)
        return dst

    if isinstance(dst, list) and isinstance(src, list):
        if list_strategy == "extend":
            return dst + copy.deepcopy(src)
        else:  # "replace"
            return copy.deepcopy(src)

    # If types are different or scalar: replace
    return copy.deepcopy(src)


def ensure_path(d: Dict[str, Any], keys: Tuple[str, ...]) -> Dict[str, Any]:
    cur = d
    for k in keys:
        cur = cur.setdefault(k, {})
    return cur

class DictionaryReverser:
    def __init__(self, dictionary_path: str, template_paths=None):
        self.log = get_classMethod_logger(self, "__init__")
        self.dictionary_path = dictionary_path

        self.ppf: Optional[ParsedParameterFile] = None
        self.dict_data: Optional[Dict[str, Any]] = None
        self.dict_name: Optional[str] = None
        self.domain: Optional[str] = None
        self.subdomain: Optional[str] = None
        self.node_type: Optional[str] = None

        self._template_center = templateCenter(template_paths)
        self._converter_cache: Dict[str, Tuple[Optional[type], Optional[Exception]]] = {}

    # Read OpenFOAM dictionary with PyFoam
    def parse(self) -> None:
        """Read dict file, capture content and identify node_type."""
        p = Path(self.dictionary_path)
        self.ppf = ParsedParameterFile(str(p))
        self.dict_data = copy.deepcopy(self.ppf.content)

        # Prefer filename stem, fallback to header object
        stem = p.stem.strip()
        header_obj = str(self.ppf.header.get("object", "")).strip()

        if stem:
            obj = stem
        elif header_obj:
            obj = header_obj
        else:
            raise ValueError(f"Cannot detect dictionary object name for {self.dictionary_path}")

        self.dict_name = obj

        # infer subdomain by path or well-known names
        lower = p.as_posix().lower()
        obj_l = self.dict_name.lower()

        sys_names = {
            "controldict", "fvschemes", "fvsolution",
            "decomposepardict", "fvconstraints", "fvoptions",
            "blockmeshdict", "snappyhexmeshdict", "changedictionarydict"
        }
        const_names = {
            "transportproperties", "thermophysicalproperties",
            "turbulenceproperties", "rasproperties",
            "momentumtransport", "physicalproperties", "g"
        }

        if "/system/" in lower or obj_l in sys_names:
            self.subdomain = "system"
        elif "/constant/" in lower or obj_l in const_names:
            self.subdomain = "constant"
        else:
            self.subdomain = "system"  # best-effort default

        self.domain = "openFOAM"
        pascal = self.dict_name[0].upper() + self.dict_name[1:]
        self.node_type = f"{self.domain}.{self.subdomain}.{pascal}"
        self.log.debug(f"Detected node_type={self.node_type}")

    #Load JSON Template
    def load_template(self) -> Dict[str, Any]:
        if not self.node_type:
            raise RuntimeError("node_type not set; call parse() first")
        try:
            # ask templateCenter for the template directly
            return copy.deepcopy(self._template_center[self.node_type])
        except FileNotFoundError as e:
            raise KeyError(f"No template found for node_type '{self.node_type}'") from e



    # Locate the converter class for the dictionary
    def locate_converter_class(self):
        # Expected: hermes.Resources.openFOAM.system.ControlDict.convertData.copyDataControlDict
        cls_name = f"copyData{self.dict_name[0].upper()}{self.dict_name[1:]}"
        path = f"hermes.Resources.{self.domain}.{self.subdomain}.{self.dict_name[0].upper()}{self.dict_name[1:]}.convertData.{cls_name}"
        converter, err = locate_class(path)
        return converter, err, path

    def build_node(self, list_strategy: str = "replace") -> Dict[str, Any]:
        if self.ppf is None:
            self.parse()

        # 1) Load the full template once
        template_full = self.load_template()

        # 2) Keep only the Execution branch from the template
        template = {
            "Execution": copy.deepcopy(template_full.get("Execution", {}))
        }

        # 3) Run converter
        converter, err, path = self.locate_converter_class()
        if converter is not None and hasattr(converter, "updateDictionaryToJson"):
            self.log.debug(f"Using converter: {path}")
            # Converter may write flat keys at the root of 'template'
            converter.updateDictionaryToJson(template, self.dict_data)
        else:
            self.log.debug(f"No converter at {path} (err: {err}). Falling back to direct insert.")
            # Ensure values path exists and merge dict_data into it
            values_leaf = ensure_path(template, ("Execution", "input_parameters", "values"))
            merge_into(values_leaf, self.dict_data or {}, list_strategy)

        # 4) Ensure 'values' exists
        values_leaf = ensure_path(template, ("Execution", "input_parameters", "values"))

        # 5) If converter wrote flat keys at the root, move them into values
        for k in list(template.keys()):
            if k not in {"Execution", "type"}:
                values_leaf[k] = template.pop(k)

        # 6) Add defaults / normalizations
        values_leaf.setdefault("interpolate", True)
        if isinstance(values_leaf.get("functions"), dict):
            values_leaf["functions"] = []
        if isinstance(values_leaf.get("libs"), dict):
            values_leaf["libs"] = []

        # 7) Final node:
        node = {
            "Execution": template["Execution"],
            "type": self.node_type
        }
        return node

    def to_json_str(self, node: dict) -> str:
        return json.dumps(node, indent=4, ensure_ascii=False, cls=FoamJSONEncoder)

    def save_node(self, node: dict, out_path: str):
        save_json(node, out_path)
