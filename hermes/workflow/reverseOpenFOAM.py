from __future__ import annotations

from PyFoam.RunDictionary.ParsedParameterFile import ParsedParameterFile
from PyFoam.Basics.DataStructures import Vector, BoolProxy
from ..Resources.reTemplateCenter import templateCenter
from ..utils.logging import get_classMethod_logger
from pathlib import Path
from typing import Any, Dict, Tuple, Optional
import json, copy, pydoc


class FoamJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, BoolProxy):
            return bool(o)
        elif isinstance(o, Vector):
            return list(o.vals)  # ✅ Important: use .vals to get the underlying list
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

    def parse(self) -> None:
        """
        Read the OpenFOAM dictionary with PyFoam, capture content, and infer
        node identifiers (domain/subdomain/node_type) directly from the input
        (header + path).
        """
        p = Path(self.dictionary_path)
        self.ppf = ParsedParameterFile(str(p))
        self.dict_data = copy.deepcopy(self.ppf.content)

        #Object name (dict_name)
        header_obj = str(self.ppf.header.get("object", "")).strip()
        stem = p.stem.strip()
        obj = header_obj or stem
        if not obj:
            raise ValueError(f"Cannot detect dictionary object name for {self.dictionary_path}")
        self.dict_name = obj

        # Subdomain: prefer header 'location' (/0 or '/system' or '/constant'), else parent dir name
        header_loc = str(self.ppf.header.get("location", "")).strip()  # e.g. "/system", "/constant", "/0"
        subdomain = header_loc.strip().strip("/").split("/")[-1] if header_loc else p.parent.name
        self.subdomain = subdomain or "system"

        self.domain = "openFOAM"
        pascal = self.dict_name[0].upper() + self.dict_name[1:] # Check if this is matches template file
        self.node_type = f"{self.domain}.{self.subdomain}.{pascal}"

        self.log.debug(
            f"Detected node_type={self.node_type} "
            f"(object='{self.dict_name}', location='{header_loc}', parent='{p.parent.name}')"
        )

    def load_template(self) -> Dict[str, Any]:
        """
        Look up and return a fresh copy of the JSON template corresponding to this dictionary type, based on its node_type.
        """
        if not self.node_type:
            raise RuntimeError("node_type not set; call parse() first")
        try:
            # ask templateCenter for the template directly
            return copy.deepcopy(self._template_center[self.node_type])
        except FileNotFoundError as e:
            raise KeyError(f"No template found for node_type '{self.node_type}'") from e



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
        """
        Build a node.
        - Always create: Execution -> input_parameters
        - Special case: for controlDict, put data under .../values
        - If a converter exists, let it update a minimal structure and normalize results
        """
        if self.ppf is None:
            self.parse()

        # Decide if this is a controlDict node (case-insensitive)
        is_control = (self.dict_name.lower() == "controldict") or \
                     (self.node_type and self.node_type.endswith(".ControlDict"))

        # Minimal base skeleton
        base = {"Execution": {"input_parameters": {}}}

        # For controlDict we want .../values to exist
        if is_control:
            ensure_path(base, ("Execution", "input_parameters", "values"))

        # Try a converter on a copy of the minimal base; otherwise, direct-merge dict_data
        converter, err, path = self.locate_converter_class()
        if converter is not None and hasattr(converter, "updateDictionaryToJson"):
            self.log.debug(f"Using converter: {path}")
            work = copy.deepcopy(base)
            converter.updateDictionaryToJson(work, self.dict_data)

            # Choose the leaf we will populate/normalize
            leaf = ensure_path(work, ("Execution", "input_parameters", "values")) if is_control \
                else work["Execution"]["input_parameters"]

            # If converter wrote flat keys at the root, move them under the leaf
            for k in list(work.keys()):
                if k not in {"Execution", "type"}:
                    leaf[k] = work.pop(k)

            # If the converter produced nothing, fallback to merging dict_data
            if not leaf:
                merge_into(leaf, self.dict_data or {}, list_strategy)

            node = {"Execution": work["Execution"], "type": self.node_type}
        else:
            self.log.debug(f"No converter at {path} (err: {err}). Falling back to direct insert.")
            leaf = ensure_path(base, ("Execution", "input_parameters", "values")) if is_control \
                else base["Execution"]["input_parameters"]
            merge_into(leaf, self.dict_data or {}, list_strategy)
            node = {"Execution": base["Execution"], "type": self.node_type}

        if is_control:
            values_leaf = ensure_path(node, ("Execution", "input_parameters", "values"))
        else:
            values_leaf = node["Execution"]["input_parameters"]

        if isinstance(values_leaf.get("functions"), dict):
            values_leaf["functions"] = []
        if isinstance(values_leaf.get("libs"), dict):
            values_leaf["libs"] = []

        if self.dict_name == "snappyHexMeshDict":

            ip = node["Execution"]["input_parameters"]

            # Normalize modules
            modules_keys = ["castellatedMesh", "snap", "addLayers", "mergeTolerance"]
            modules = {}
            for key in modules_keys:
                if key in ip:
                    val = ip.pop(key)
                    # Rename "addLayers" to "layers" for normalization
                    if key == "addLayers":
                        modules["layers"] = val
                    else:
                        modules[key] = val
            if modules:
                ip["modules"] = modules

            # Fix geometry
            geometry = ip.get("geometry", {})
            objects = {}
            to_remove = []

            for k, v in geometry.items():
                if k.endswith(".obj"):
                    name = k.replace(".obj", "")
                    obj = {
                        "objectName": name,
                        "objectType": "obj",
                    }
                    if isinstance(v, dict):
                        obj.update(v)
                    objects[name] = obj
                    to_remove.append(k)

            for k in to_remove:
                del geometry[k]
            if objects:
                geometry["objects"] = objects

            geometry.setdefault("gemeotricalEntities", {})

            # Map features[*].file to geometry.objects[*].levels
            features = ip.get("castellatedMeshControls", {}).get("features", [])
            for feature in features:
                file = feature.get("file", "").strip('"')
                name = Path(file).stem  # e.g. "building.eMesh" -> "building"
                if name in geometry["objects"]:
                    geometry["objects"][name]["levels"] = str(feature.get("level"))

            # Ensure addLayersControls exists
            alc = ip.setdefault("addLayersControls", {})

            # Add missing default fields
            alc.setdefault("nRelaxedIter", 20)
            alc.setdefault("nMedialAxisIter", 10)
            alc.setdefault("additionalReporting", False)

            # Migrate nSurfaceLayers from layers -> building.layers
            nsl = None
            if "layers" in alc:
                try:
                    layers = alc["layers"]
                    if isinstance(layers, dict):
                        nsl = layers.pop("nSurfaceLayers", None)
                        # Remove 'layers' if empty after popping
                        if not layers:
                            del alc["layers"]
                except KeyError:
                    pass
                if nsl is not None:
                    for obj in geometry["objects"].values():
                        obj.setdefault("layers", {})["nSurfaceLayers"] = nsl

            # Migrate refinementSurfaces and refinementRegions
            cmc = ip.get("castellatedMeshControls", {})
            rs = cmc.get("refinementSurfaces", {})
            rr = cmc.get("refinementRegions", {})

            for name, obj in geometry["objects"].items():
                if name in rs:
                    surf = rs[name]
                    obj["refinementSurfaces"] = {
                        "levels": surf.get("level", [0, 0]),
                        "patchType": surf.get("patchInfo", {}).get("type", "wall")
                    }

                    for rname, rinfo in surf.get("regions", {}).items():
                        region = obj.setdefault("regions", {}).get(rname, {})
                        region["refinementSurfaceLevels"] = rinfo.get("level", [0, 0])
                        region["type"] = rinfo.get("type", "wall")
                        obj["regions"][rname] = region

                for rname, rinfo in rr.items():
                    if "regions" in obj and rname in obj["regions"]:
                        obj["refinementRegions"] = {}
                        obj["regions"][rname]["refinementRegions"] = {
                            "mode": rinfo.get("mode"),
                            "levels": rinfo.get("levels")
                        }

        return node

    def to_json_str(self, node: dict) -> str:
        return json.dumps(node, indent=4, ensure_ascii=False, cls=FoamJSONEncoder)

    def save_node(self, node: dict, out_path: str):
        save_json(node, out_path)
