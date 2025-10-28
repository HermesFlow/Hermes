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

def preprocess_blockMeshDict(raw_text: str, parsed_dict: dict) -> dict:
    # 1. Extract variables like v 0.577; ma -0.707...
    variables = {
        match[0]: float(match[1])
        for match in re.findall(r'(\w+)\s+([-\d.eE]+);', raw_text)
    }

    # Expand expressions like $v into numeric values
    def expand(val):
        if isinstance(val, str) and val.startswith('$'):
            return variables.get(val[1:], val)
        return float(val)

    # 2. Expand variables in vertices
    if "vertices" in parsed_dict:
        parsed_dict["vertices"] = [
            [expand(x) for x in triplet]
            for triplet in parsed_dict["vertices"]
        ]

    # 3. Extract edges
    edges = []
    edge_block = re.search(r'edges\s*\((.*?)\);', raw_text, re.DOTALL)
    if edge_block:
        edge_lines = re.findall(r'(\w+)\s+(\d+)\s+(\d+)\s+\(([^()]+)\)', edge_block.group(1))
        for etype, start, end, coords in edge_lines:
            point = [expand(c) for c in coords.strip().split()]
            edges.append({
                "type": etype,
                "start": int(start),
                "end": int(end),
                "point": point
            })

    # 4. Extract faces
    faces = []
    face_block = re.search(r'faces\s*\((.*?)\);', raw_text, re.DOTALL)
    if face_block:
        face_lines = re.findall(r'project\s+\(([\d\s]+)\)\s+(\w+)', face_block.group(1))
        for verts_str, geometry in face_lines:
            verts = [int(v) for v in verts_str.strip().split()]
            faces.append({
                "type": "project",
                "vertices": verts,
                "geometry": geometry
            })

    # 5. Inject into parsed_dict
    parsed_dict["edges"] = edges
    parsed_dict["faces"] = faces

    return parsed_dict


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

def _normalize_parsed_dict(data):
    """
    Recursively normalize PyFoam parsed dict so downstream code sees consistent types.
    - Strings with whitespace -> split into list of tokens
    - "yes"/"no"/"true"/"false" -> boolean
    - Numeric strings -> int or float
    - Already a list -> normalize elements
    - Dicts -> recurse
    - Everything else -> unchanged
    """
    if isinstance(data, dict):
        return {k: _normalize_parsed_dict(v) for k, v in data.items()}

    elif isinstance(data, list):
        return [_normalize_parsed_dict(x) for x in data]

    elif isinstance(data, str):
        val = data.strip().lower()
        if val in ("yes", "true", "on", "1"):
            return True
        if val in ("no", "false", "off", "0"):
            return False

        # try numeric conversion
        try:
            if "." in val or "e" in val:
                return float(val)
            return int(val)
        except ValueError:
            pass

        parts = data.split()
        return parts if len(parts) > 1 else data.strip()

    else:
        return data




def as_dict(obj):
    if isinstance(obj, Mapping):
        return {k: as_dict(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [as_dict(i) for i in obj]
    else:
        return obj
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



# Helpers for snappyHexMeshDict normalization
def extract_modules(ip: Dict[str, Any]) -> None:
    """
    Collect castellatedMesh, snap, addLayers, and mergeTolerance into `modules` for snappyHexMeshDict.
    """
    modules = {}
    sentinel = object()
    for key in ("castellatedMesh", "snap", "addLayers", "mergeTolerance"):
        val = ip.pop(key, sentinel)
        if val is not sentinel:
            val = unwrap_special_type(val)
            modules["layers" if key == "addLayers" else key] = val
    if modules:
        ip["modules"] = modules

def normalize_location_in_mesh(cmc: Dict[str, Any], logger=None) -> None:
    loc = cmc.get("locationInMesh")
    if isinstance(loc, str):
        try:
            cmc["locationInMesh"] = [float(p) for p in loc.strip("()").split()]
        except ValueError as e:
            if logger:
                logger.warning(f"Failed to normalize locationInMesh: {e}")


def hoist_geometry_objects(geometry: Dict[str, Any], logger=None):
    objects = geometry.setdefault("objects", {})
    normalize_in_place(objects)

    try:
        for k, v in list(geometry.items()):
            if isinstance(k, str) and k.endswith(".obj"):
                name = v.get("name") if isinstance(v, dict) else None
                if not name:
                    name = Path(k).stem
                tgt = objects.setdefault(name, {})
                if isinstance(v, dict):
                    tgt.update(v)
                tgt.setdefault("objectName", name)
                tgt.setdefault("objectType", "obj")
                geometry.pop(k, None)
    except Exception as e:
        if logger:
            logger.warning(f"Failed hoisting triSurface objects: {e}")


def promote_refinement_surfaces(building, regions, walls, ref_surfs, originally_flat, logger=None):
    try:
        bsurf = to_native(ref_surfs).get("building", {})
        global_levels = []
        global_ptype = "wall"

        if isinstance(bsurf, dict):
            global_levels = bsurf.get("level", []) or []
            global_ptype = bsurf.get("patchInfo", {}).get("type", "wall")

            if global_levels:
                building["refinementSurfaces"] = {
                    "levels": global_levels,
                    "patchType": global_ptype
                }

            if isinstance(walls, dict) and global_levels:
                walls.setdefault("refinementSurfaceLevels", global_levels)
                if "type" not in walls:
                    walls["type"] = global_ptype

            rregions = bsurf.get("regions", {})
            if isinstance(rregions, dict):
                for rname, rdef in rregions.items():
                    if not isinstance(rdef, dict):
                        continue
                    region_entry = regions.get(rname, {})
                    if not isinstance(region_entry, dict):
                        region_entry = {}
                        regions[rname] = region_entry

                    r_levels = rdef.get("level")
                    r_type = rdef.get("type")

                    if originally_flat:
                        if isinstance(r_levels, list) and r_levels == [0, 0] and global_levels:
                            r_levels = global_levels
                        if r_type == "patch" and global_ptype:
                            r_type = global_ptype
                    else:
                        if isinstance(r_levels, list) and r_levels == [0, 0]:
                            r_levels = None

                    if isinstance(r_levels, list):
                        region_entry["refinementSurfaceLevels"] = r_levels
                    if isinstance(r_type, str):
                        region_entry["type"] = r_type

    except Exception as e:
        if logger:
            logger.warning(f"Failed to promote refinementSurfaces/regions: {e}")

def promote_refinement_regions(
    building: Dict[str, Any],
    walls: Dict[str, Any],
    ref_regs: Dict[str, Any],
    logger=None,
):
    try:
        regs = to_native(ref_regs) if ref_regs else {}
        bld_rr = regs.get("building")
        if isinstance(bld_rr, dict):
            building["refinementRegions"] = bld_rr
        else:
            building.setdefault("refinementRegions", {})

        w_rr = regs.get("Walls")
        if isinstance(w_rr, dict):
            walls["refinementRegions"] = w_rr
        else:
            walls.pop("refinementRegions", None)
    except Exception as e:
        if logger:
            logger.warning(f"Failed to promote refinementRegions: {e}")

def handle_add_layers_controls(
    ip: Dict[str, Any],
    building: Dict[str, Any],
    geometry: Dict[str, Any]
):
    alc = ip.setdefault("addLayersControls", {})
    normalize_in_place(alc)

    alc.setdefault("nRelaxedIter", 20)
    alc.setdefault("nMedialAxisIter", 10)
    alc.setdefault("additionalReporting", False)

    layers_block = alc.get("layers")
    nsl = None
    if isinstance(layers_block, dict):
        nsl = layers_block.pop("nSurfaceLayers", None)
        if not layers_block:
            alc.pop("layers", None)

    ip["addLayersControls"] = alc

    if nsl is not None:
        building.setdefault("layers", {})["nSurfaceLayers"] = nsl
        geometry.setdefault("layers", {})["nSurfaceLayers"] = nsl
    else:
        geometry.setdefault("layers", {}).setdefault(
            "nSurfaceLayers", building.get("layers", {}).get("nSurfaceLayers", 10)
        )

    geometry.setdefault("objects", geometry.get("objects", {}))
    geometry.setdefault("refinementSurfaces", {})
    geometry.setdefault("regions", {})
    ip["geometry"] = geometry





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
        self.ppf = ParsedParameterFile(str(p))

        # Parse and deep copy
        raw_data = copy.deepcopy(self.ppf.content)

        # Drop FoamFile block to avoid legacy headers
        raw_data.pop("FoamFile", None)

       # self.dict_data = _normalize_parsed_dict(self.dict_data)
        unwrapped = unwrap_booleans_and_vectors(raw_data)

        # ⬇️ Only normalize for dicts that benefit from tokenization
        if self.dict_name == "changeDictionaryDict":
            self.dict_data = unwrapped
        else:
            self.dict_data = _normalize_parsed_dict(unwrapped)

            # Normalize boundary from alternating [name, dict, name, dict, ...]
            if "boundary" in self.dict_data and isinstance(self.dict_data["boundary"], list):
                boundary_list = self.dict_data["boundary"]
                normalized = []
                i = 0
                while i < len(boundary_list) - 1:
                    name = boundary_list[i]
                    body = boundary_list[i + 1]
                    if isinstance(name, str) and isinstance(body, dict):
                        entry = {"name": name}
                        entry.update(body)
                        normalized.append(entry)
                    i += 2
                self.dict_data["boundary"] = normalized

            # Object name (dict_name)
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
            # Sanitize any quoted subdomain (like "constant")
            self.subdomain = self.subdomain.strip('"').strip("'")

            self.domain = "openFOAM"
            pascal = self.dict_name[0].upper() + self.dict_name[1:]  # Check if this is matches template file
            self.node_type = f"{self.domain}.{self.subdomain}.{pascal}".replace('"', '').replace("'", "")

        self.log.debug(
            f"Detected node_type={self.node_type} "
            f"(object='{self.dict_name}', location='{header_loc}', parent='{p.parent.name}')"
        )

        print("\n--- DEBUG PARSE ---")
        print("raw_data['boundary'] =", raw_data.get("boundary"))
        print("dict_data['boundary'] =", self.dict_data.get("boundary"))
        print("-------------------\n")



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


    def convert_snappy_dict_to_v2(self, raw_dict):
        """
        Convert OpenFOAM snappyHexMeshDict (parsed) into structured version 2 input JSON.
        """
        raw_dict = self._normalize_booleans(raw_dict)
        input_parameters = copy.deepcopy(raw_dict)

        # ----------------------------
        # 1. Extract modules
        # ----------------------------
        modules = {}
        for key in ("castellatedMesh", "snap", "addLayers", "mergeTolerance"):
            if key in input_parameters:
                modules["layers" if key == "addLayers" else key] = input_parameters.pop(key)
        input_parameters["modules"] = modules

        # ----------------------------
        # 2. Preserve and extend addLayersControls
        # ----------------------------
        alc = copy.deepcopy(input_parameters.get("addLayersControls", {}))
        nsl = alc.pop("nSurfaceLayers", 10)
        alc.pop("layers", None)
        alc["additionalReporting"] = alc.get("additionalReporting", False)
        alc["nMedialAxisIter"] = alc.get("nMedialAxisIter", 10)
        alc["nRelaxedIter"] = alc.get("nRelaxedIter", 20)
        input_parameters["addLayersControls"] = alc

        # ----------------------------
        # 3. Convert geometry section
        # ----------------------------
        original_geometry = input_parameters.get("geometry", {})
        geometry_objects = original_geometry.get("objects", original_geometry)

        new_geometry = {
            "objects": {},
            "refinementSurfaces": {},
            "regions": {},
            "layers": {"nSurfaceLayers": nsl},
        }

        cmc = input_parameters.get("castellatedMeshControls", {})
        refinement_regions = cmc.get("refinementRegions", {})
        refinement_surfaces = cmc.get("refinementSurfaces", {})

        for name, obj in geometry_objects.items():
            if not isinstance(obj, dict):
                continue

            object_name = name[:-4] if name.endswith(".obj") else name
            object_type = obj.get("objectType", "obj")

            building = {
                "objectName": object_name,
                "objectType": object_type,
                "levels": obj.get("levels", "1"),
                "layers": {"nSurfaceLayers": nsl},
                "regions": {},
                "refinementRegions": obj.get("refinementRegions", {}),
            }

            # Move inline refinementSurfaceLevels + patchType directly onto the object
            if "refinementSurfaceLevels" in obj:
                building["refinementSurfaceLevels"] = obj["refinementSurfaceLevels"]
            if "patchType" in obj:
                building["patchType"] = obj["patchType"]

            # Add refinementSurfaces block inside object
            ref_surf_key = object_name
            if "refinementSurfaceLevels" in obj or ref_surf_key in refinement_surfaces:
                levels = obj.get("refinementSurfaceLevels")
                if not levels:
                    levels = refinement_surfaces.get(ref_surf_key, {}).get("levels") or \
                             refinement_surfaces.get(ref_surf_key, {}).get("level", [0, 0])
                patch_type = obj.get("patchType") or \
                             refinement_surfaces.get(ref_surf_key, {}).get("patchType") or \
                             refinement_surfaces.get(ref_surf_key, {}).get("patchInfo", {}).get("type", "wall")

                if levels is not None and patch_type is not None:
                    building["refinementSurfaces"] = {
                        "levels": levels,
                        "patchType": patch_type
                    }

            # fallback refinementRegions from castellatedMeshControls
            if not building["refinementRegions"]:
                # Try object name first
                if object_name in refinement_regions:
                    building["refinementRegions"] = refinement_regions[object_name]
                # Then try full filename (e.g. building.obj) as fallback
                elif name in refinement_regions:
                    building["refinementRegions"] = refinement_regions[name]

            # ----------------------------
            # Regions
            # ----------------------------
            input_regions = obj.get("regions", {})

            # Pull from castellatedMeshControls if available
            ref_surf_regions = (
                refinement_surfaces.get(ref_surf_key, {}).get("regions", {})
            )

            for region_name, region_data in input_regions.items():
                region_entry = {}

                # Explicitly preserve known keys
                for k in ("type", "refinementRegions", "refinementSurfaceLevels", "name"):
                    if k in region_data:
                        region_entry[k] = region_data[k]

                # Fill in from refinementSurfaces -> regions if needed
                fallback_region_data = ref_surf_regions.get(region_name, {})
                if "type" not in region_entry and "type" in fallback_region_data:
                    region_entry["type"] = fallback_region_data["type"]
                if "refinementSurfaceLevels" not in region_entry and "level" in fallback_region_data:
                    region_entry["refinementSurfaceLevels"] = fallback_region_data["level"]

                # Fill in from refinementRegions if needed
                if "refinementRegions" not in region_entry and region_name in refinement_regions:
                    region_entry["refinementRegions"] = refinement_regions[region_name]

                # Final fallback
                if "type" not in region_entry or not region_entry["type"]:
                    region_entry["type"] = "patch"

                building["regions"][region_name] = region_entry

            new_geometry["objects"][object_name] = building

        # Add empty top-level refinementSurfaces for completeness
        new_geometry["refinementSurfaces"] = {}
        input_parameters["geometry"] = new_geometry

        # ----------------------------
        # 4. Clean up castellatedMeshControls
        # ----------------------------
        for key in ("features", "refinementSurfaces", "refinementRegions"):
            input_parameters.get("castellatedMeshControls", {}).pop(key, None)

        return input_parameters


    def convert_block_mesh_dict_to_v2(self, parsed_dict: dict) -> dict:

        result = {
            "Execution": {
                "input_parameters": {}
            },
            "type": "openFOAM.mesh.BlockMesh",
            "version": 2
        }

        params = result["Execution"]["input_parameters"]

        # 1. convertToMeters
        if "convertToMeters" in parsed_dict:
            params["convertToMeters"] = str(parsed_dict["convertToMeters"])

        # 2. vertices
        if "vertices" in parsed_dict:
            params["vertices"] = parsed_dict["vertices"]

        # 3. blocks
        blocks_out = []
        if "blocks" in parsed_dict and isinstance(parsed_dict["blocks"], list):
            blocks_raw = parsed_dict["blocks"]

            # Case A: already structured list of dicts
            if all(isinstance(b, dict) for b in blocks_raw):
                blocks_out.extend(blocks_raw)
            # Case B: flat token list
            else:
                i = 0
                while i + 4 < len(blocks_raw):
                    if blocks_raw[i] == "hex" and isinstance(blocks_raw[i + 1], list):
                        try:
                            hex_indices = blocks_raw[i + 1]
                            cell_count = blocks_raw[i + 2]
                            grading = blocks_raw[i + 4]  # Skip over "simpleGrading"

                            block_entry = {
                                "hex": hex_indices,
                                "cellCount": cell_count,
                                "grading": grading
                            }
                            blocks_out.append(block_entry)
                        except Exception as e:
                            print(f"Failed parsing block at index {i}: {e}")
                    i += 5

        params["blocks"] = blocks_out

        # 4. boundary
        if "boundary" in parsed_dict:
            boundary_out = []
            for bnd in parsed_dict["boundary"]:
                if not isinstance(bnd, dict):
                    print("Skipping invalid boundary entry:", bnd)
                    continue

                name = bnd.get("name")

                if name is None and len(bnd) == 1:
                    name, inner = next(iter(bnd.items()))
                    bnd = inner

                entry = {
                    "name": name,
                    "type": bnd.get("type"),
                    "faces": bnd.get("faces", []),
                }
                boundary_out.append(entry)

            params["boundary"] = boundary_out

        # 5. geometry
        if "geometry" in parsed_dict:
            params["geometry"] = parsed_dict["geometry"]
        else:
            params["geometry"] = {}

        # 6. edges
        edges_out = []

        if "edges" in parsed_dict:
            raw_edges = parsed_dict["edges"]

            # If flat list of "arc" tokens
            if isinstance(raw_edges, list):
                i = 0
                while i + 3 < len(raw_edges):
                    if raw_edges[i] == "arc":
                        try:
                            point1 = raw_edges[i + 1]
                            point2 = raw_edges[i + 2]
                            pointM = raw_edges[i + 3]

                            edge_entry = {
                                "type": "arc",
                                "point1": point1,
                                "point2": point2,
                                "pointM": pointM
                            }
                            edges_out.append(edge_entry)
                            i += 4
                        except Exception as e:
                            print(f"Failed parsing edge at index {i}: {e}")
                            i += 1
                    else:
                        i += 1  # Skip any unexpected tokens
            else:
                print("Unexpected edges format:", raw_edges)

        params["edges"] = edges_out

        # 7. faces
        if "faces" in parsed_dict:
            faces_out = []
            for entry in parsed_dict["faces"]:
                if isinstance(entry, dict):
                    faces_out.append(entry)
            params["faces"] = faces_out

        return result

    def convert_fv_schemes_dict_to_v2(self, parsed_dict: dict) -> dict:
        """
        Convert fvSchemes dictionary (parsed by PyFoam) into Hermes v2 JSON format.
        """

        parsed_dict.pop("FoamFile", None)

        result = {
            "Execution": {"input_parameters": {}},
            "type": "openFOAM.system.FvSchemes",
            "version": 2,
        }

        params = result["Execution"]["input_parameters"]

        # -------------------------
        # Defaults
        # -------------------------
        defaults = {}
        if "ddtSchemes" in parsed_dict and "default" in parsed_dict["ddtSchemes"]:
            defaults["ddtScheme"] = parsed_dict["ddtSchemes"]["default"]

        if "gradSchemes" in parsed_dict and "default" in parsed_dict["gradSchemes"]:
            grad_tokens = parsed_dict["gradSchemes"]["default"]
            if isinstance(grad_tokens, str):
                grad_tokens = grad_tokens.split()
            defaults["gradSchemes"] = {
                "type": grad_tokens[0],
                "name": grad_tokens[1] if len(grad_tokens) > 1 else "",
            }

        if "divSchemes" in parsed_dict and "default" in parsed_dict["divSchemes"]:
            div_tokens = parsed_dict["divSchemes"]["default"]
            if isinstance(div_tokens, str):
                div_tokens = div_tokens.split()
            defaults["divSchemes"] = {
                "type": div_tokens[0],
                "name": div_tokens[1] if len(div_tokens) > 1 else "",
                "parameters": " ".join(div_tokens[2:]),
            }

        if "laplacianSchemes" in parsed_dict and "default" in parsed_dict["laplacianSchemes"]:
            lap_tokens = parsed_dict["laplacianSchemes"]["default"]
            if isinstance(lap_tokens, str):
                lap_tokens = lap_tokens.split()
            defaults["laplacianSchemes"] = {
                "type": lap_tokens[0],
                "name": lap_tokens[1] if len(lap_tokens) > 1 else "",
                "parameters": " ".join(lap_tokens[2:]),
            }

        if "interpolationSchemes" in parsed_dict and "default" in parsed_dict["interpolationSchemes"]:
            defaults["interpolationSchemes"] = parsed_dict["interpolationSchemes"]["default"]

        if "snGradSchemes" in parsed_dict and "default" in parsed_dict["snGradSchemes"]:
            defaults["snGradSchemes"] = parsed_dict["snGradSchemes"]["default"]

        if "wallDist" in parsed_dict and "method" in parsed_dict["wallDist"]:
            defaults["wallDist"] = parsed_dict["wallDist"]["method"]

        params["default"] = defaults

        # -------------------------
        # Field-specific schemes
        # -------------------------
        fields_out = {}

        # divSchemes
        if "divSchemes" in parsed_dict:
            for key, val in parsed_dict["divSchemes"].items():
                if key == "default":
                    continue
                tokens = val if isinstance(val, list) else val.split()
                entry = {
                    "noOfOperators": key.count(",") + (1 if key.startswith("div(") else 0),
                    "type": tokens[0],
                    "name": tokens[1] if len(tokens) > 1 else "",
                    "parameters": " ".join(tokens[2:]),
                }
                if key.startswith("div(") and "," in key:
                    entry["phi"] = key.split("(")[1].split(",")[0]
                    field_name = key.split(",")[1].rstrip(")")
                elif key.startswith("div("):
                    field_name = key[4:-1]
                else:
                    field_name = key
                fields_out.setdefault(field_name, {}).setdefault("divSchemes", []).append(entry)

        # laplacianSchemes
        if "laplacianSchemes" in parsed_dict:
            for key, val in parsed_dict["laplacianSchemes"].items():
                if key == "default":
                    continue
                tokens = val if isinstance(val, list) else val.split()
                entry = {
                    "noOfOperators": key.count(",") + 1,
                    "type": tokens[0],
                    "name": tokens[1] if len(tokens) > 1 else "",
                    "parameters": " ".join(tokens[2:]),
                }
                if key.startswith("laplacian(") and "," in key:
                    inner = key[10:-1]
                    coeff, fld = inner.split(",", 1)
                    entry["coefficient"] = coeff.strip()
                    field_name = fld.strip()
                else:
                    field_name = key
                fields_out.setdefault(field_name, {}).setdefault("laplacianSchemes", []).append(entry)

        # -------------------------
        # fluxRequired
        # -------------------------
        default_flux = False
        if "fluxRequired" in parsed_dict and "default" in parsed_dict["fluxRequired"]:
            raw_default = parsed_dict["fluxRequired"]["default"]
            if isinstance(raw_default, str):
                default_flux = raw_default.strip().lower() == "yes"
            elif isinstance(raw_default, bool):
                default_flux = raw_default

        # Step 1: apply default to all fields we’ve seen
        for fld in fields_out.keys():
            fields_out[fld]["fluxRequired"] = default_flux

        # Step 2: override for explicitly listed fields
        if "fluxRequired" in parsed_dict:
            for fld in parsed_dict["fluxRequired"]:
                if fld == "default":
                    continue
                fields_out.setdefault(fld, {})["fluxRequired"] = True

        params["fields"] = fields_out

        return result

    def convert_fvSolution_dict_to_v2(self, parsed_dict: dict) -> dict:
        def _yn(v):
            if isinstance(v, bool):
                return "yes" if v else "no"
            if isinstance(v, str):
                s = v.strip().lower()
                if s in ("yes", "true", "on", "1"):
                    return "yes"
                if s in ("no", "false", "off", "0"):
                    return "no"
            return v

        result = {
            "Execution": {"input_parameters": {}},
            "type": "openFOAM.system.FvSolution",
            "version": 2,
        }
        params = result["Execution"]["input_parameters"]

        # -------------------------
        # 1. solvers (keep all)
        # -------------------------
        solvers_dict = parsed_dict.get("solvers", {})
        if solvers_dict:
            fields_out = {}
            for name, solver in solvers_dict.items():
                cleaned = {k: _yn(v) for k, v in solver.items()}
                fields_out[name] = cleaned
            params["fields"] = fields_out

        # -------------------------
        # 2. SIMPLE / PISO / PIMPLE block
        # -------------------------
        for algo in ("SIMPLE", "PISO", "PIMPLE"):
            if algo in parsed_dict:
                algo_block = parsed_dict[algo]
                converted = {k: _yn(v) for k, v in algo_block.items()}
                params["solverProperties"] = {
                    "algorithm": algo,
                    **converted
                }
                break

        # -------------------------
        # 3. relaxationFactors
        # -------------------------
        rf = parsed_dict.get("relaxationFactors")
        if isinstance(rf, dict):
            rf_cleaned = {}
            for section, val in rf.items():
                if isinstance(val, dict):
                    rf_cleaned[section] = {k: v for k, v in val.items()}
            if rf_cleaned:
                params["relaxationFactors"] = rf_cleaned

        return result

    def convert_changeDictionary_to_v2(self, parsed_dict: dict) -> dict:
        """
        Convert parsed changeDictionary file (boundary condition definitions) into v2 JSON.
        Returns a full structured node wrapped in "defineNewBoundaryConditions".
        """

        fields_out = {}

        def clean_value(val):
            val = unwrap_booleans_and_vectors(val)

            # Keep numbers & bools native
            if isinstance(val, (int, float, bool)):
                return val

            # If it's a list that looks like ["uniform", "0.1"], join it back
            if isinstance(val, list) and all(isinstance(v, str) for v in val):
                return " ".join(val)

            # Preserve "uniform ..." and "nonuniform ..." as single strings
            if isinstance(val, str):
                s = val.strip()
                if s.startswith("uniform") or s.startswith("nonuniform"):
                    return s
                return s

            return val

        for field_name, field_data in parsed_dict.items():
            if field_name in ("FoamFile",):
                continue

            field_entry = {}

            if "internalField" in field_data:
                field_entry["internalField"] = clean_value(field_data["internalField"])

            if "boundaryField" in field_data:
                bfields = {}
                for patch_name, patch_data in field_data["boundaryField"].items():
                    patch_entry = {}
                    for key, val in patch_data.items():
                        patch_entry[key] = clean_value(val)
                    bfields[patch_name] = patch_entry
                field_entry["boundaryField"] = bfields

            fields_out[field_name] = field_entry

        # 🔎 DEBUG PRINT
        import pprint
        print("\n[DEBUG] fields_out:")
        pprint.pprint(fields_out, width=120)

        return {
            "Execution": {"input_parameters": {"fields": fields_out}},
            "type": "openFOAM.system.ChangeDictionary",
            "version": 2,
        }

    def convert_decomposeParDict_to_v2(self, parsed_dict: dict) -> dict:
        """
        Convert parsed decomposeParDict into v2 JSON format.
        """
        return {
            "Execution": {
                "input_parameters": {
                    # Always return the placeholder reference
                    "numberOfSubdomains": "{Parameters.output.decomposeProcessors}"
                    # Do NOT include "method" since reference workflow JSON omits it
                }
            },
            "type": "openFOAM.system.DecomposePar",
            "version": 2,
        }

    def convert_surfaceFeatures_to_v2(self, leaf: dict) -> dict:
        subset = leaf.get("subsetFeatures", {})

        def to_bool(val: str) -> bool:
            val = str(val).strip().lower()
            return val in ("no", "false")  # treat "no" as True, "yes" as False

        return {
            "Execution": {
                "input_parameters": {
                    "OFversion": "{Parameters.output.OFversion}",
                    "geometryData": "{snappyHexMesh.input_parameters.geometry.objects}",
                    "includeAngle": int(leaf.get("includedAngle", 150)),
                    "nonManifoldEdges": to_bool(subset.get("nonManifoldEdges", "no")),
                    "openEdges": to_bool(subset.get("openEdges", "no")),
                },
                "type": "openFOAM.systemExecuters.surfaceFeaturesDict",
            },
            "type": "openFOAM.system.SurfaceFeatures",
            "version": 2,
        }

    def convert_g_dict_to_v2(self, parsed_dict: dict) -> dict:
        """
        Convert 'g' file to Hermes v2 format.

        Example OpenFOAM:
        dimensions      [0 1 -2 0 0 0 0];
        value           (0 0 -9.81);

        Hermes v2 input_parameters:
        {
            "x": 0,
            "y": 0,
            "z": -9.81
        }
        """
        val = parsed_dict.get("value", [0, 0, -9.81])
        if isinstance(val, str):
            # Convert string "(0 0 -9.81)" to list
            val = val.strip("()").split()
            val = [float(v) for v in val]

        return {
            "x": val[0] if len(val) > 0 else 0,
            "y": val[1] if len(val) > 1 else 0,
            "z": val[2] if len(val) > 2 else -9.81
        }

    def convert_momentum_transport_to_v2(self, parsed_dict: dict, as_node: bool = False) -> dict:
        """
        Convert a parsed OpenFOAM momentumTransport dictionary to Hermes v2 format.
        Relies only on the parsed input, doesn't use hardcoded defaults.
        """
        # Extract simulation type (e.g., RAS, LES, laminar)
        sim_type = parsed_dict.get("simulationType", "").strip()

        # Get the corresponding block (e.g., parsed_dict["RAS"])
        sim_block = parsed_dict.get(sim_type, {})

        # Build the input_parameters purely from parsed_dict
        input_parameters = {
            "simulationType": sim_type,
            "Model": sim_block.get("model") or sim_block.get(f"{sim_type}Model") or "",
            "turbulence": self._as_bool(sim_block.get("turbulence")),
            "printCoeffs": self._as_bool(sim_block.get("printCoeffs")),
        }

        if as_node:
            return {
                "Execution": {"input_parameters": input_parameters},
                "type": "openFOAM.constant.momentumTransport",
                "version": 2,
            }

        return input_parameters

    def _as_bool(self, value):
        """Convert typical OpenFOAM 'on'/'off' or booleans to True/False."""
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value.strip().lower() in ("on", "true", "yes", "1")
        return False

    def convert_physical_properties_to_v2(self, parsed_dict: dict) -> dict:
        """
        Convert physicalProperties (or transportProperties) dictionary into Hermes v2 format.
        Supports both modern and legacy styles (with dimensions, printName, etc.).
        Produces clean JSON ready for Jinja rendering.
        """
        result = {
            "transportModel": parsed_dict.get("transportModel", "Newtonian"),
        }

        # Handle nu as top-level scalar
        if "nu" in parsed_dict:
            val = parsed_dict["nu"]
            if isinstance(val, list):
                result["nu"] = val[-1]  # always last element is the numeric value
            elif isinstance(val, dict):
                result["nu"] = val.get("value", val)
            else:
                result["nu"] = val

        # Optional rhoInf
        if "rhoInf" in parsed_dict:
            val = parsed_dict["rhoInf"]
            if isinstance(val, list):
                result["rhoInf"] = val[-1]
            elif isinstance(val, dict):
                result["rhoInf"] = val.get("value", val)
            else:
                result["rhoInf"] = val

        parameters = {}
        reserved = {"FoamFile", "transportModel", "nu", "rhoInf"}

        for key, value in parsed_dict.items():
            if key in reserved:
                continue

            clean_val = None
            dims = "[0 0 0 0 0 0 0]"

            # Handle old-style list
            if isinstance(value, list):
                clean_val = value[-1] if len(value) > 0 else None

            # Handle dict-style
            elif isinstance(value, dict):
                clean_val = value.get("value", None)
                dims = str(value.get("dimensions", dims))

            # Handle plain scalar
            else:
                clean_val = value

            # If clean_val is still a list (like ['viscosityModel', '[0 ...]', 'constant'])
            if isinstance(clean_val, list) and len(clean_val) == 3:
                clean_val = clean_val[-1]

            parameters[key] = {
                "dimensions": dims,
                "value": clean_val
            }

        if parameters:
            result["parameters"] = parameters

        return result

    def convert_transport_properties_to_v2(self, parsed_dict: dict) -> dict:
        """
        Convert OpenFOAM transportProperties dictionary into Hermes v2 JSON format.
        Handles: transportModel, nu, optional rhoInf, and optional extra parameters.
        """
        input_parameters = {}

        # Required fields
        input_parameters["transportModel"] = parsed_dict.get("transportModel", "Newtonian")
        input_parameters["nu"] = parsed_dict.get("nu")

        # Optional rhoInf
        if "rhoInf" in parsed_dict:
            input_parameters["rhoInf"] = parsed_dict["rhoInf"]

        # Reserved keys not treated as additional parameters
        reserved = {"transportModel", "nu", "rhoInf", "FoamFile"}
        extras = {}

        for key, value in parsed_dict.items():
            if key in reserved:
                continue

            if isinstance(value, dict):
                extras[key] = {
                    "dimensions": value.get("dimensions", "[0 0 0 0 0 0 0]"),
                    "value": value.get("value")
                }
            else:
                extras[key] = {
                    "dimensions": "[0 0 0 0 0 0 0]",
                    "value": value
                }

        if extras:
            input_parameters["parameters"] = extras

        return {
            "Execution": {
                "input_parameters": input_parameters
            },
            "type": "openFOAM.constant.transportProperties",
            "version": 2
        }

    def convert_turbulence_properties_to_v2(self, parsed_dict: dict) -> dict:
        """
        Alias: turbulenceProperties is the same as momentumTransport (RASProperties).
        """
        return self.convert_momentum_transport_to_v2(parsed_dict, as_node=True)

    def convert_mesh_quality_dict_to_v2(self, parsed_dict: dict) -> dict:
        """
        Convert a meshQualityDict parsed dictionary to Hermes v2 node format.
        Supports both full dictionaries and include-only templates.
        """
        result = {
            "Execution": {
                "input_parameters": {}
            },
            "type": "openFOAM.system.MeshQualityDict",
            "version": 2
        }

        input_params = result["Execution"]["input_parameters"]

        # Case: include-only format
        if "0" in parsed_dict and isinstance(parsed_dict["0"], list):
            input_params["0"] = parsed_dict["0"]
            return result

        # Handle main keys
        for key, value in parsed_dict.items():
            if key == "relaxed" and isinstance(value, dict):
                # Preserve nested relaxed block
                input_params["relaxed"] = {}
                for rk, rv in value.items():
                    input_params["relaxed"][rk] = rv
            elif isinstance(value, (str, int, float, bool, list, dict)):
                input_params[key] = value
            else:
                print(f"Skipping unknown meshQualityDict key: {key} -> {value}")

        return result

    def apply_v2_conversion(self, dict_name: str, final_leaf: dict) -> Optional[dict]:
        """
        Apply v2 conversion for supported OpenFOAM dictionaries.
        Returns a v2-structured node or None if no conversion is defined.
        """
        print(f"apply_v2_conversion: dict_name = {dict_name}")

        if dict_name == "snappyHexMeshDict":
            return self.convert_snappy_dict_to_v2(final_leaf)

        if dict_name == "blockMeshDict":
            return self.convert_block_mesh_dict_to_v2(final_leaf)

        if dict_name == "fvSchemes":
            v2_structured = self.convert_fv_schemes_dict_to_v2(final_leaf)
            return v2_structured

        if dict_name == "fvSolution":
            v2_structured = self.convert_fvSolution_dict_to_v2(final_leaf)
            return v2_structured

        if dict_name == "changeDictionaryDict":
            # Treat both like boundary-condition dictionaries
            v2_structured = self.convert_changeDictionary_to_v2(final_leaf)
            return v2_structured

        if dict_name == "transportProperties":
            v2_structured = self.convert_transport_properties_to_v2(final_leaf)
            return v2_structured

        if dict_name == "decomposeParDict":
            v2_structured = self.convert_decomposeParDict_to_v2(final_leaf)
            return v2_structured

        if dict_name == "surfaceFeaturesDict":
            node = self.convert_surfaceFeatures_to_v2(final_leaf)
            return {"surfaceFeatures": node}

        if dict_name == "g":
            return self.convert_g_dict_to_v2(final_leaf)

        if dict_name == "meshQualityDict":
            return self.convert_mesh_quality_dict_to_v2(final_leaf)

        if dict_name in ("RASProperties", "turbulenceProperties", "momentumTransport"):
            print(f"Converting momentumTransport via convert_momentum_transport_to_v2()")
            return self.convert_momentum_transport_to_v2(final_leaf)

        if dict_name == "physicalProperties":
            return self.convert_physical_properties_to_v2(final_leaf)

        return None

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

        # Apply v2 conversion if available
        v2_structured = self.apply_v2_conversion(self.dict_name, final_leaf)

        print(f"\n apply_v2_conversion() returned for {self.dict_name}:")
        print(json.dumps(v2_structured, indent=4, default=str))

        if isinstance(v2_structured, dict) and "Execution" in v2_structured and "input_parameters" in v2_structured[
            "Execution"]:
            final_leaf.clear()
            final_leaf.update(copy.deepcopy(v2_structured["Execution"]["input_parameters"]))
            node["type"] = v2_structured.get("type", node["type"])
            node["version"] = v2_structured.get("version", 2)

        elif isinstance(v2_structured, dict):  # Flat format (e.g., blockMeshDict, fvSchemes)
            final_leaf.clear()
            final_leaf.update(copy.deepcopy(v2_structured))
            node["version"] = 2

        else:
            print(f"No structured v2 data returned for {self.dict_name}")

        """
        if v2_structured is not None:
            if self.dict_name == "surfaceFeaturesDict":
                # For surfaceFeaturesDict, use the full node (not just input_parameters)
                node = v2_structured
            else:
                # For other dictionaries, keep the existing Execution structure
                final_leaf.clear()
                final_leaf.update(copy.deepcopy(v2_structured))
                node["version"] = 2
            """

        return {self.dict_name: node}

    def to_json_str(self, node: dict) -> str:
        return json.dumps(node, indent=4, ensure_ascii=False, cls=FoamJSONEncoder)

    def save_node(self, node: dict, out_path: str):
        save_json(node, out_path)
