from __future__ import annotations
from PyFoam.RunDictionary.ParsedParameterFile import ParsedParameterFile
from PyFoam.RunDictionary.ParsedParameterFile import Field
from PyFoam.Basics.DataStructures import Vector, BoolProxy, Dimension
from ..Resources.reTemplateCenter import templateCenter
from ..utils.logging import get_classMethod_logger
from pathlib import Path
from typing import Any, Dict, Tuple, Optional
import json, copy, pydoc, re
from collections.abc import Mapping
import re




# ------ Helpers Functions ------


def convert_bools_to_lowercase(obj):
    if isinstance(obj, dict):
        return {k: convert_bools_to_lowercase(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_bools_to_lowercase(v) for v in obj]
    elif obj is True:
        return "true"
    elif obj is False:
        return "false"
    else:
        return obj


def _normalize_parsed_dict(data, split_strings=False):
    """
    Recursively normalize parsed OpenFOAM dictionaries to produce consistent Python data structures.

    Args:
        data: The parsed dictionary/list/value.
        split_strings (bool): If True, splits whitespace-delimited strings into lists (default: False).

    Returns:
        Normalized Python data structure.
    """
    if isinstance(data, dict):
        return {k: _normalize_parsed_dict(v, split_strings=split_strings) for k, v in data.items()}

    elif isinstance(data, list):
        return [_normalize_parsed_dict(x, split_strings=split_strings) for x in data]

    elif isinstance(data, str):
        val = data.strip().lower()
        if val in ("yes", "true", "on", "1"):
            return True
        if val in ("no", "false", "off", "0"):
            return False

        # Try numeric conversion
        try:
            if "." in val or "e" in val:
                return float(val)
            return int(val)
        except ValueError:
            pass

        # Optionally split string tokens (disabled for edge safety)
        if split_strings:
            parts = data.strip().split()
            return parts if len(parts) > 1 else data.strip()

        return data.strip()

    else:
        return data


# Helper to convert PyFoam dict-like objects to native Python types
def to_native(obj):
    """
    Recursively convert PyFoam dict-like objects to native Python types.
    """
    if isinstance(obj, dict):
        try:
            return {k: to_native(v) for k, v in obj.items()}
        except Exception:
            try:
                return {k: to_native(obj[k]) for k in list(obj)}
            except Exception:
                return str(obj)
    elif isinstance(obj, list):
        return [to_native(i) for i in obj]
    elif hasattr(obj, "__dict__"):
        return to_native(vars(obj))
    else:
        return obj

def normalize_in_place(d: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convert a dictionary in place to native Python types
    """
    native = to_native(d)
    if native is not d:
        d.clear()
        d.update(native)
    return d


def unwrap_special_type(val):
    """
    Unwrap PyFoam's special types and vector/field strings to native Python.
    """
    # PyFoam boolean
    if isinstance(val, BoolProxy):
        return bool(val)

    # PyFoam vector
    if isinstance(val, Vector):
        return list(val.vals)

    # PyFoam Field (e.g. internalField uniform 0.01;)
    if isinstance(val, Field):
        try:
            # Fields stringify nicely in OpenFOAM syntax
            return str(val).strip()
        except Exception:
            # fallback: treat as list if something weird happens
            return list(val)

    # Stringified vector: e.g. "(5 0 0)"
    if isinstance(val, str):
        match = re.match(r'^\(\s*([^\)]+)\s*\)$', val)
        if match:
            parts = match.group(1).split()
            try:
                return [float(p) for p in parts]
            except ValueError:
                pass  # Not a numeric vector — keep as-is

    return val

def unwrap_booleans_and_vectors(obj):
    """
    Recursively unwrap special PyFoam types to native Python.
    """
    obj = unwrap_special_type(obj)

    if isinstance(obj, dict):
        # Handle wrapped bool or vector structures
        if "val" in obj and isinstance(obj["val"], (bool, int, float, str)):
            return unwrap_booleans_and_vectors(obj["val"])
        if "vals" in obj and isinstance(obj["vals"], list):
            return [unwrap_booleans_and_vectors(v) for v in obj["vals"]]

        return {k: unwrap_booleans_and_vectors(v) for k, v in obj.items()}

    elif isinstance(obj, list):
        return [unwrap_booleans_and_vectors(v) for v in obj]

    return obj








# ------- JSON Handling -------
class FoamJSONEncoder(json.JSONEncoder):
    """
    Custom JSON encoder to handle PyFoam types like BoolProxy and Vector.
    """
    def default(self, o):
        if isinstance(o, BoolProxy):
            return bool(o)
        elif isinstance(o, Vector):
            return list(o.vals)
        elif isinstance(o, Dimension):
            return str(o)
        return super().default(o)


def save_json(data, save_name):
    """
    Convert Python dictionary into a JSON
    """
    with open(save_name, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, sort_keys=True, ensure_ascii=False, cls=FoamJSONEncoder)


def locate_class(path: str):
    """
    Load a Python class given its full path and returns it.
    """
    try:
        return pydoc.locate(path), None
    except Exception as e:
        return None, e

def merge_into(dst: Any, src: Any, list_strategy: str = "replace") -> Any:
    """
    Extract Keys and Values from a dictionary and Replace or Add Keys in the JSON Structure.
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
    """
    Make sure a nested dictionary path exists inside a dict,
    creating empty dicts along the way, and return the innermost dict
    """
    cur = d
    for k in keys:
        cur = cur.setdefault(k, {})
    return cur



class DictionaryReverser:
    """
    DictionaryReverser class set up all the states the reverser will need when parsing and building JSON nodes from OpenFOAM dictionaries.
    """
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

    def _normalize_booleans(self, data):
        """
        Recursively converts string booleans ("true", "false") into actual Python bools (True, False).
        """
        if isinstance(data, dict):
            return {k: self._normalize_booleans(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self._normalize_booleans(v) for v in data]
        elif isinstance(data, str):
            if data.lower() == "true":
                return True
            elif data.lower() == "false":
                return False
            return data
        else:
            return data


    def parse(self) -> None:
        """
        Read the OpenFOAM dictionary with PyFoam, capture content, and infer
        node identifiers (domain/subdomain/node_type) directly from the input
        (header + path).
        """
        p = Path(self.dictionary_path)

        # Manually fix malformed "edges" block in blockMeshDict
        def _extract_edges_manually(path: Path):
            with open(path, "r") as f:
                txt = f.read()

            import re
            block = re.search(r"edges\s*\((.*?)\);", txt, re.S)
            if not block:
                return None

            lines = block.group(1).strip().splitlines()
            edges = []

            for line in lines:
                line = line.strip()
                m = re.match(r"arc\s+(\d+)\s+(\d+)\s*\(([^)]+)\)", line)
                if m:
                    start = int(m.group(1))
                    end = int(m.group(2))
                    pt = [float(x) for x in m.group(3).split()]
                    edges.extend(["arc", start, end, pt])
            return edges

        edge_override = None
        if p.name == "blockMeshDict":
            edge_override = _extract_edges_manually(p)

        # Parse OpenFOAM file using PyFoam
        self.ppf = ParsedParameterFile(str(p))
        print(f"ParsedParameterFile content: {self.ppf.content}")

        # Use manual edges if needed
        if edge_override is not None:
            print(" Patched malformed edge parsing via manual override")
            self.ppf.content["edges"] = edge_override

        # Detect dictionary name
        header_obj = str(self.ppf.header.get("object", "")).strip()
        stem = p.stem.strip()
        self.dict_name = header_obj or stem
        if not self.dict_name:
            raise ValueError(f"Cannot detect dictionary object name for {self.dictionary_path}")

        # Parse and copy
        raw_data = copy.deepcopy(self.ppf.content)
        raw_data.pop("FoamFile", None)
        print(f"raw_data: {raw_data}")

        # Convert booleans/vectors to native Python
        unwrapped = unwrap_booleans_and_vectors(raw_data)

        # Normalize safely (no string splitting unless needed)
        self.dict_data = (
            unwrapped if self.dict_name == "changeDictionaryDict"
            else _normalize_parsed_dict(unwrapped, split_strings=False)
        )

        # Fix boundary format if alternating [name, dict, name, dict, ...]
        if "boundary" in self.dict_data and isinstance(self.dict_data["boundary"], list):
            boundary_list = self.dict_data["boundary"]
            normalized = []
            i = 0
            while i < len(boundary_list) - 1:
                name, body = boundary_list[i], boundary_list[i + 1]
                if isinstance(name, str) and isinstance(body, dict):
                    entry = {"name": name}
                    entry.update(body)
                    normalized.append(entry)
                i += 2
            self.dict_data["boundary"] = normalized

        # Detect subdomain
        header_loc = str(self.ppf.header.get("location", "")).strip()
        subdomain = header_loc.strip("/").split("/")[-1] if header_loc else p.parent.name
        self.subdomain = subdomain.strip('"').strip("'") or "system"

        # Final domain and node type
        self.domain = "openFOAM"
        pascal = self.dict_name[0].upper() + self.dict_name[1:]
        self.node_type = f"{self.domain}.{self.subdomain}.{pascal}".replace('"', '').replace("'", "")


    # Locate the converter class for the dictionary
    def locate_converter_class(self):
        """
        Figure out if a special-purpose converter exists for this dictionary type, and if so, return it.
        Try to locate a converter class (copyData<DictName>) for the current dictionary type.
        Converter classes are responsible for custom logic when translating
        dictionary content to JSON .
        """
        cls_name = f"copyData{self.dict_name[0].upper()}{self.dict_name[1:]}"
        path = f"hermes.Resources.{self.domain}.{self.subdomain}.{self.dict_name[0].upper()}{self.dict_name[1:]}.convertData.{cls_name}"
        converter, err = locate_class(path)
        return converter, err, path


    def build_node(self, list_strategy: str = "replace") -> Dict[str, Any]:
        if self.ppf is None:
            self.parse()

        is_control = (self.dict_name.lower() == "controldict") or \
                     (self.node_type and self.node_type.endswith(".ControlDict"))

        base = {"Execution": {"input_parameters": {}}}
        if is_control:
            ensure_path(base, ("Execution", "input_parameters", "values"))

        converter, err, path = self.locate_converter_class()
        use_converter = converter is not None and hasattr(converter, "updateDictionaryToJson")

        target = copy.deepcopy(base)
        leaf = ensure_path(target, ("Execution", "input_parameters", "values")) if is_control \
            else target["Execution"]["input_parameters"]

        if use_converter:
            self.log.debug(f"Using converter: {path}")
            converter.updateDictionaryToJson(target, self.dict_data)
            work_leaf = ensure_path(target, ("Execution", "input_parameters", "values")) if is_control \
                else target["Execution"]["input_parameters"]

            # Promote fields
            for k in list(target.keys()):
                if k not in {"Execution", "type"}:
                    work_leaf[k] = target.pop(k)

            if not work_leaf:
                merge_into(work_leaf, self.dict_data or {}, list_strategy)
        else:
            self.log.debug(f"No converter at {path} (err: {err}). Falling back to direct insert.")
            merge_into(leaf, self.dict_data or {}, list_strategy)

        # Replace the type for known overrides
        override_types = {
            "blockMeshDict": "openFOAM.mesh.BlockMesh",
            "snappyHexMeshDict": "openFOAM.mesh.SnappyHexMesh",
            "fvSchemes": "openFOAM.system.FvSchemes",
            "fvSolution": "openFOAM.system.FvSolution",
            "decomposeParDict": "openFOAM.system.DecomposePar",
            "controlDict": "openFOAM.system.ControlDict",
            "surfaceFeaturesDict": "openFOAM.system.SurfaceFeatures",
            "transportProperties": "openFOAM.constant.transportProperties",
            "turbulenceProperties": "openFOAM.constant.momentumTransport",
            "RASProperties": "openFOAM.constant.momentumTransport",
            "changeDictionaryDict": "openFOAM.system.ChangeDictionary",
            "momentumTransport": "openFOAM.constant.momentumTransport",
            "physicalProperties": "openFOAM.constant.physicalProperties"
        }

        override_type = override_types.get(self.dict_name, self.node_type)

        node = {"Execution": target["Execution"], "type": override_type}

        # Normalize quirks
        final_leaf = ensure_path(node, ("Execution", "input_parameters", "values")) if is_control \
            else node["Execution"]["input_parameters"]

        for key in ["functions", "libs"]:
            if isinstance(final_leaf.get(key), dict):
                final_leaf[key] = []

        if is_control:
            convert_bools_to_lowercase(final_leaf)
            node["version"] = 2

        node["version"] = 2
        return {self.dict_name: node}

    def to_json_str(self, node: dict) -> str:
        return json.dumps(node, indent=4, ensure_ascii=False, cls=FoamJSONEncoder)

    def save_node(self, node: dict, out_path: str):
        save_json(node, out_path)
