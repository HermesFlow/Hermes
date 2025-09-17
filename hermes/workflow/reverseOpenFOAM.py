from __future__ import annotations

from PyFoam.RunDictionary.ParsedParameterFile import ParsedParameterFile
from PyFoam.Basics.DataStructures import Vector, BoolProxy
from ..Resources.reTemplateCenter import templateCenter
from ..utils.logging import get_classMethod_logger
from pathlib import Path
from typing import Any, Dict, Tuple, Optional
import json, copy, pydoc, re
from collections.abc import Mapping




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

"""
def unwrap_special_type(val):
    
    #Unwrap BoolProxy and Vector to native Python values.

    if isinstance(val, BoolProxy):
        return bool(val)
    if isinstance(val, Vector):
        return list(val.vals)
    return val


def unwrap_booleans_and_vectors(obj):

    #Recursively unwrap PyFoam BoolProxy/Vector and dict-shaped wrappers into native Python bools and lists.
    
    unwrap_special_type(obj)
    # Dict-shaped wrappers (often appear after to_native or PyFoam internals)
    if isinstance(obj, dict):
        # bool wrapper: {"val": True, "textual": "true"}
        if "val" in obj and isinstance(obj["val"], (bool, int, float, str)):
            # Prefer the real Python value; for booleans this yields True/False
            return unwrap_booleans_and_vectors(obj["val"])
        # vector wrapper: {"vals": [ ... ]}
        if "vals" in obj and isinstance(obj["vals"], list):
            return [unwrap_booleans_and_vectors(v) for v in obj["vals"]]
        # generic dict
        return {k: unwrap_booleans_and_vectors(v) for k, v in obj.items()}

    # Lists
    if isinstance(obj, list):
        return [unwrap_booleans_and_vectors(v) for v in obj]

    return obj
"""
def unwrap_special_type(val):
    """
    Unwrap PyFoam's special types and vector strings to native Python.
    """
    # PyFoam boolean
    if isinstance(val, BoolProxy):
        return bool(val)

    # PyFoam vector
    if isinstance(val, Vector):
        return list(val.vals)

    # Stringified vector: e.g. "(5 0 0)"
    if isinstance(val, str):
        match = re.match(r'^\(\s*([^\)]+)\s*\)$', val)
        if match:
            parts = match.group(1).split()
            try:
                return [float(p) for p in parts]
            except ValueError:
                pass  # Not a numeric vector — skip

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

# Helpers for blockMeshDict normalization



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

        # Parse and deep copy
        raw_data = copy.deepcopy(self.ppf.content)

        # Clean it from PyFoam wrappers like BoolProxy, Vector, etc.
        self.dict_data = unwrap_booleans_and_vectors(raw_data)

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


    def convert_snappy_dict_to_v2(self, raw_dict):
        """
        Convert OpenFOAM snappyHexMeshDict (parsed) into structured version 2 input JSON.
        """
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

    """
    def handle_snappy_dict(self, ip: Dict[str, Any]):
        
            #Normalize a snappyHexMeshDict-like dictionary into the JSON node shape used by the workflow.
        
        # 0) Basic normalization
        normalize_in_place(ip)

        # 1) Collect modules into a single block
        extract_modules(ip)

        # 2) castellatedMeshControls normalization
        cmc = ip.setdefault("castellatedMeshControls", {})
        normalize_in_place(cmc)
        # locationInMesh may arrive as "(x y z)"; normalize to list[float]
        normalize_location_in_mesh(cmc, self.log)

        # 3) Geometry/Object hoisting
        geometry = ip.setdefault("geometry", {})
        normalize_in_place(geometry)
        hoist_geometry_objects(geometry, self.log)
        objects = geometry.setdefault("objects", {})
        normalize_in_place(objects)
        geometry.setdefault("gemeotricalEntities", {}) # The pipeline sometimes keeps this optional container (typo kept for compatibility)

        # Work on 'building' object
        building = objects.setdefault("building", {})
        originally_flat = "refinementSurfaceLevels" in building
        building.setdefault("objectName", "building")
        building.setdefault("objectType", "obj")

        # 4) Promote feature files (optional)
        features = cmc.get("features")
        if features:
            for feature in to_native(features):
                file = str(feature.get("file", "")).strip('"')
                lvl = feature.get("level")
                name = (Path(file).stem if file else None) or "building"
                if name in objects and lvl is not None:
                    objects[name]["levels"] = str(lvl)
            cmc.pop("features", None)

        # Capture & remove refinement sections from cmc (we will place them in geometry/objects)
        ref_surfs = cmc.pop("refinementSurfaces", {}) or {}
        ref_regs = cmc.pop("refinementRegions", {}) or {}

        # 5) Regions: snapshot and setup
        regions = building.setdefault("regions", {})

        # Snapshot which regions originally had a 'name' key
        original_region_has_name = {
            r: (isinstance(d, dict) and "name" in d)
            for r, d in regions.items()
        }

        # Access Walls without creating it (avoid side effects in snapshot)
        walls = regions.get("Walls", {})

        # 6) Promote refinementSurfaces (global + region overrides)
        promote_refinement_surfaces(building, regions, walls, ref_surfs, originally_flat, self.log)

        # 7) Promote refinementRegions
        promote_refinement_regions(building, walls, ref_regs, self.log)

        # Remove helper keys if they accidentally appeared on 'building'
        for fld in ("name", "type"):
            building.pop(fld, None)

        # 8) addLayersControls: lift nSurfaceLayers
        handle_add_layers_controls(ip, building, geometry)

        # Remove empty writeFlags only if it exists
        if "writeFlags" in ip and not ip.get("writeFlags"):
            ip.pop("writeFlags", None)

        # 9) Final normalization & flattening rules
        normalize_in_place(ip)
        final_native = unwrap_booleans_and_vectors(ip)

        try:
            building = final_native["geometry"]["objects"]["building"]
            regions = building.get("regions", {})

            # Drop redundant 'name' only if it wasn't in the original input
            for rname, rdef in list(regions.items()):
                if isinstance(rdef, dict):
                    # drop 'name' only if it wasn't present in the original input
                    if not original_region_has_name.get(rname, False):
                        rdef.pop("name", None)

           # walls = regions.get("Walls", {})

            # Decide whether to flatten nested building.refinementSurfaces
            rs = building.get("refinementSurfaces")
            if isinstance(rs, dict):
                gl = rs.get("levels")
                pt = rs.get("patchType", "wall")
                rr = building.get("regions", {})

                def mirrors_global_or_placeholder(d):
                    if not isinstance(d, dict):
                        return True
                    lvl = d.get("refinementSurfaceLevels", None)
                    typ = d.get("type", None)
                    lvl_ok = (lvl is None) or (lvl == gl) or (lvl == [0, 0])
                    typ_ok = (typ is None) or (typ == pt) or (typ == "patch")
                    return lvl_ok and typ_ok

                # Flatten if originally flat, or if global is non-zero and
                # all regions don't contradict (only mirror/placeholder)
                will_flatten = False
                if originally_flat:
                    will_flatten = True
                elif isinstance(gl, list) and gl != [0, 0] and all(
                        mirrors_global_or_placeholder(d) for d in rr.values()):
                    will_flatten = True

                if will_flatten:
                    # Push global to regions where missing or placeholders
                    for rname, rdef in (rr.items() if isinstance(rr, dict) else []):
                        if not isinstance(rdef, dict):
                            continue
                        lvl = rdef.get("refinementSurfaceLevels", None)
                        typ = rdef.get("type", None)
                        if (lvl is None) or (lvl == [0, 0]):
                            if isinstance(gl, list):
                                rdef["refinementSurfaceLevels"] = gl
                        if (typ is None) or (typ == "patch"):
                            if isinstance(pt, str):
                                rdef["type"] = pt

                    # Replace nested with flat keys on building
                    building["refinementSurfaceLevels"] = gl or []
                    building["patchType"] = pt
                    building.pop("refinementSurfaces", None)

        except Exception as e:
            self.log.warning(f"Final cleanup failed: {e}")

        # 10) Replace incoming dict with normalized final
        ip.clear()
        ip.update(final_native)
    """


    def handle_block_mesh_dict(self, ip: Dict[str, Any]) -> None:
        """
        Normalize a blockMeshDict-like dictionary into the JSON node shape
        used by the workflow.
        """
        raw = unwrap_booleans_and_vectors(self.dict_data or {})

        convert_to_meters = str(raw.get("convertToMeters", "1"))
        vertices = raw.get("vertices", [])
        default_patch = raw.get("defaultPatch")  # ← Optional

        # --- Parse blocks ---
        blocks = []
        raw_blocks = raw.get("blocks", [])
        i = 0
        while i < len(raw_blocks):
            if raw_blocks[i] == "hex":
                try:
                    hex_points = raw_blocks[i + 1]
                    cell_count_raw = raw_blocks[i + 2]
                    grading_raw = raw_blocks[i + 4]

                    # Convert cell count string to list of ints
                    cell_count = (
                        list(map(int, cell_count_raw.strip("()").split()))
                        if isinstance(cell_count_raw, str)
                        else cell_count_raw
                    )

                    # Convert grading string to list of floats
                    grading = (
                        list(map(float, grading_raw.strip("()").split()))
                        if isinstance(grading_raw, str)
                        else grading_raw
                    )

                    blocks.append({
                        "hex": hex_points,
                        "cellCount": cell_count,
                        "grading": grading
                    })

                    i += 5  # Move to next block
                except Exception as e:
                    print(f"Failed parsing block at index {i}: {e}")
                    i += 1
            else:
                i += 1

        # --- Fallback: Use 'geometry' if no blocks parsed ---
        geometry = raw.get("geometry", {})
        if not blocks and isinstance(geometry, dict):
            cell_count = geometry.get("cellCount")
            grading = geometry.get("grading", [1, 1, 1])
            if isinstance(cell_count, list) and len(cell_count) == 3:
                blocks.append({
                    "hex": list(range(8)),  # Default 8-point cube
                    "cellCount": cell_count,
                    "grading": grading
                })
                # Keep geometry untouched — it may be expected in the output

        # --- Parse boundary ---
        boundary = []
        raw_boundary = raw.get("boundary", {})
        if isinstance(raw_boundary, dict):
            for name, bdef in raw_boundary.items():
                if not isinstance(bdef, dict):
                    continue
                boundary.append({
                    "name": name,
                    "type": bdef.get("type", "patch"),
                    "faces": bdef.get("faces", [])
                })
        elif isinstance(raw_boundary, list):
            i = 0
            while i < len(raw_boundary) - 1:
                name = raw_boundary[i]
                bdef = raw_boundary[i + 1]
                if not isinstance(name, str) or not isinstance(bdef, dict):
                    i += 1
                    continue
                boundary.append({
                    "name": name,
                    "type": bdef.get("type", "patch"),
                    "faces": bdef.get("faces", [])
                })
                i += 2

        # --- Final output ---
        final_dict = {
            "convertToMeters": convert_to_meters,
            "vertices": vertices,
            "blocks": blocks,
            "boundary": boundary,
            "geometry": geometry,
        }

        if isinstance(default_patch, dict) and default_patch.get("type") is not None:
            final_dict["defaultPatch"] = default_patch

        ip.clear()
        ip.update(final_dict)



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

        if is_control:
            convert_bools_to_lowercase(final_leaf)

        # SnappyHexMeshDict special handling
        if self.dict_name == "snappyHexMeshDict":
            v2_structured = self.convert_snappy_dict_to_v2(final_leaf)
            v2_structured = convert_bools_to_lowercase(v2_structured)  # normalize booleans
            final_leaf.clear()
            final_leaf.update(copy.deepcopy(v2_structured))
            node["version"] = 2

        """ 
        if self.dict_name == "snappyHexMeshDict":
            print("➡️ Handling snappyHexMeshDict with handle_snappy_dict()")
        if self.dict_name == "snappyHexMeshDict":
            self.handle_snappy_dict(final_leaf)
            # One more unwrap pass (in place) on the whole input_parameters
            normalize_in_place(final_leaf)  # to drop any PyFoam mapping shells
            final_native = unwrap_booleans_and_vectors(final_leaf)
            final_leaf.clear()
            final_leaf.update(final_native)
        """

        # blockMeshDict special handling
        if self.dict_name == "blockMeshDict":
            print("➡️ Handling blockMeshDict with handle_block_mesh_dict()")

        if self.dict_name == "blockMeshDict":
            self.handle_block_mesh_dict(final_leaf)
            normalize_in_place(final_leaf)
            final_native = unwrap_booleans_and_vectors(final_leaf)
            final_leaf.clear()
            final_leaf.update(final_native)

        return node

    def to_json_str(self, node: dict) -> str:
        return json.dumps(node, indent=4, ensure_ascii=False, cls=FoamJSONEncoder)

    def save_node(self, node: dict, out_path: str):
        save_json(node, out_path)
