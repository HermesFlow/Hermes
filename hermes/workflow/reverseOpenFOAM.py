from __future__ import annotations

from PyFoam.RunDictionary.ParsedParameterFile import ParsedParameterFile
from PyFoam.Basics.DataStructures import Vector, BoolProxy
from ..Resources.reTemplateCenter import templateCenter
from ..utils.logging import get_classMethod_logger
from pathlib import Path
from typing import Any, Dict, Tuple, Optional
import json, copy, pydoc


def unwrap_booleans_and_vectors(obj):
    """
    Recursively unwrap PyFoam-style 'val' booleans and 'vals' vectors
    into native Python bools and lists.
    """
    if isinstance(obj, dict):
        if "val" in obj and isinstance(obj["val"], bool):
            return obj["val"]
        if "vals" in obj and isinstance(obj["vals"], list):
            return [unwrap_booleans_and_vectors(v) for v in obj["vals"]]
        return {k: unwrap_booleans_and_vectors(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [unwrap_booleans_and_vectors(v) for v in obj]
    return obj


def unwrap_and_clean_snappy_node(node):
    """
    Normalize the reversed snappyHexMeshDict node structure so it matches
    the expected schema from the Hermes pipeline.
    """
    execution = node.get("Execution", {})
    params = execution.get("input_parameters", {})

    # ✅ Deep convert PyFoam objects to native first
    params_native = to_native(params)

    # ✅ Then unwrap BoolProxy and Vector types
    cleaned = unwrap_booleans_and_vectors(params_native)

    # 2. Fix 'geometry' field nesting and cleanup
    geometry = cleaned.get("geometry", {})
    objects = geometry.get("objects", {})
    if not isinstance(objects, dict):
        objects = {}
        geometry["objects"] = objects

    if "building" in objects:
        building = objects["building"]

        # Promote refinementSurfaceLevels
        regions = building.get("regions", {})
        walls = regions.get("Walls", {})

        level = walls.get("refinementSurfaceLevels")
        patch_type = walls.get("type", "wall")

        if level:
            building["refinementSurfaces"] = {
                "levels": level,
                "patchType": patch_type
            }

        refinement_regions = walls.get("refinementRegions")
        if refinement_regions:
            building["refinementRegions"] = refinement_regions

        for k in ["name", "type"]:
            walls.pop(k, None)
            building.pop(k, None)

    return {
        "Execution": {"input_parameters": cleaned},
        "type": node.get("type", "openFOAM.mesh.SnappyHexMesh")
    }



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

    def _handle_snappy_dict(self, ip: Dict[str, Any]):
        # Normalize modules
        modules = {}
        for key in ["castellatedMesh", "snap", "addLayers", "mergeTolerance"]:
            if key in ip:
                val = ip.pop(key)
                modules["layers" if key == "addLayers" else key] = val
        if modules:
            ip["modules"] = modules

        cmc = ip.get("castellatedMeshControls", {})

        # Fix locationInMesh format
        try:
            loc = cmc["locationInMesh"]
            if isinstance(loc, str):
                parts = loc.strip("()").split()
                cmc["locationInMesh"] = [float(p) for p in parts]
        except Exception as e:
            self.log.warning(f"Failed to normalize locationInMesh: {e}")

        # Migrate features[*].file -> geometry.objects[*].levels
        geometry = ip.setdefault("geometry", {})
        objects = geometry.setdefault("objects", {})

        # Ensure we have a 'building' object
        building = objects.setdefault("building", {})  # <-- this line fixes the NameError

        building.setdefault("objectName", "building")
        building.setdefault("objectType", "obj")

        # Safely migrate features[*].file -> geometry.objects[*].levels
        try:
            features = cmc["features"]
        except KeyError:
            features = None
        except Exception as e:
            self.log.warning(f"Unexpected error when accessing 'features': {e}")
            features = None

        if features:
            for feature in features:
                file = feature.get("file", "").strip('"')
                name = Path(file).stem
                if name in objects:
                    objects[name]["levels"] = str(feature.get("level"))
            # Remove the original features block
            try:
                del cmc["features"]
            except Exception:
                pass

        # Ensure nested structure
        geometry.setdefault("gemeotricalEntities", {})  # Probably typo — should be "geometricalEntities"?
        building = objects.setdefault("building", {})
        building.setdefault("objectName", "building")
        building.setdefault("objectType", "obj")
        building.setdefault("refinementRegions", {})

        # Promote refinementSurfaces and refinementRegions from castellatedMeshControls to geometry
        for key in ["refinementSurfaces", "refinementRegions"]:
            val = cmc.get(key)
            if val is not None:
                # Do NOT pop, just clone if needed
                try:
                    if key == "refinementRegions":
                        walls = building.setdefault("regions", {}).setdefault("Walls", {})
                        walls[key] = val
                    elif key == "refinementSurfaces":
                        building[key] = {
                            "levels": val.get("building", {}).get("level", []),
                            "patchType": val.get("building", {}).get("patchInfo", {}).get("type", "wall")
                        }
                except Exception as e:
                    self.log.warning(f"Failed to promote {key}: {e}")

        # Promote nested fields for compatibility
        regions = building.get("regions", {})
        walls = regions.get("Walls", {})

        if "refinementSurfaceLevels" in walls:
            building["refinementSurfaces"] = {
                "levels": walls["refinementSurfaceLevels"],
                "patchType": walls.get("type", "wall")
            }

        if "refinementRegions" in walls:
            building["refinementRegions"] = walls["refinementRegions"]

        for region_name in ["inlet", "outlet"]:
            if region_name in regions:
                regions[region_name].setdefault("type", "patch")

        for field in ["name", "type"]:
            building.pop(field, None)

        # addLayersControls defaults
        alc = ip.setdefault("addLayersControls", {})
        alc.setdefault("nRelaxedIter", 20)
        alc.setdefault("nMedialAxisIter", 10)
        alc.setdefault("additionalReporting", False)

        # Move nSurfaceLayers from addLayersControls to geometry.objects.building
        try:
            layers = alc["layers"]
        except KeyError:
            layers = None
        except Exception as e:
            self.log.warning(f"Failed to access addLayersControls.layers: {e}")
            layers = None

        if layers and isinstance(layers, dict):
            nsl = layers.pop("nSurfaceLayers", None)

            if nsl is not None:
                building.setdefault("layers", {})["nSurfaceLayers"] = nsl

            # Clean up: remove 'layers' only if now empty
            if not layers:
                try:
                    del alc["layers"]
                except Exception:
                    alc["layers"] = {}  # If deletion fails, ensure it's at least clean

        # Final cleanup
        if not ip.get("writeFlags"):
            ip.pop("writeFlags", None)


        # Fix geometry naming: convert "building.obj" → objects["building"]
        raw_geom = ip.get("geometry", {})
        geom_objs = raw_geom.setdefault("objects", {})

        for k in list(raw_geom.keys()):
            if k.endswith(".obj"):
                obj_data = raw_geom.pop(k)
                name = obj_data.get("name", Path(k).stem)
                geom_objs[name] = obj_data

        # Reassign with typo preserved
        ip["geometry"] = {
            "objects": geom_objs,
            "gemeotricalEntities": geometry.get("gemeotricalEntities", {}),
        }

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

        node = {"Execution": target["Execution"], "type": self.node_type}

        # Normalize quirks
        final_leaf = ensure_path(node, ("Execution", "input_parameters", "values")) if is_control \
            else node["Execution"]["input_parameters"]

        for key in ["functions", "libs"]:
            if isinstance(final_leaf.get(key), dict):
                final_leaf[key] = []

        # SnappyHexMeshDict special handling
        if self.dict_name == "snappyHexMeshDict":
            self._handle_snappy_dict(final_leaf)

        if self.dict_name == "snappyHexMeshDict":
            self._handle_snappy_dict(final_leaf)
            node = unwrap_and_clean_snappy_node(node)  # <== clean structure

        return to_native(node)

    def to_json_str(self, node: dict) -> str:
        return json.dumps(node, indent=4, ensure_ascii=False, cls=FoamJSONEncoder)

    def save_node(self, node: dict, out_path: str):
        save_json(node, out_path)
