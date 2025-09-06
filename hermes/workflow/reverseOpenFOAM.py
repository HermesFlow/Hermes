from __future__ import annotations

from PyFoam.RunDictionary.ParsedParameterFile import ParsedParameterFile
from PyFoam.Basics.DataStructures import Vector, BoolProxy
from ..Resources.reTemplateCenter import templateCenter
from ..utils.logging import get_classMethod_logger
from pathlib import Path
from typing import Any, Dict, Tuple, Optional
import json, copy, pydoc

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
    native = to_native(d)
    if native is not d:
        d.clear()
        d.update(native)
    return d


def unwrap_booleans_and_vectors(obj):
    """
    Recursively unwrap PyFoam BoolProxy/Vector AND dict-shaped wrappers
    like {"val": true, "textual": "true"} and {"vals": [...]} into native
    Python bools and lists.
    """
    # Direct PyFoam types
    if isinstance(obj, BoolProxy):
        return bool(obj)
    if isinstance(obj, Vector):
        return list(obj.vals)

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


class FoamJSONEncoder(json.JSONEncoder):
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
        print(p)
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

    def handle_snappy_dict(self, ip: Dict[str, Any]):
        normalize_in_place(ip)

        modules = {}
        sentinel = object()
        for key in ("castellatedMesh", "snap", "addLayers", "mergeTolerance"):
            val = ip.pop(key, sentinel)
            if val is not sentinel:
                try:
                    from PyFoam.Basics.DataStructures import BoolProxy
                    if isinstance(val, BoolProxy):
                        val = bool(val)
                except Exception:
                    pass
                modules["layers" if key == "addLayers" else key] = val
        if modules:
            ip["modules"] = modules

        cmc = ip.setdefault("castellatedMeshControls", {})
        normalize_in_place(cmc)
        try:
            loc = cmc.get("locationInMesh")
            if isinstance(loc, str):
                parts = loc.strip("()").split()
                cmc["locationInMesh"] = [float(p) for p in parts]
        except Exception as e:
            self.log.warning(f"Failed to normalize locationInMesh: {e}")

        geometry = ip.setdefault("geometry", {})
        normalize_in_place(geometry)

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
            self.log.warning(f"Failed hoisting triSurface objects: {e}")

        geometry.setdefault("gemeotricalEntities", {})

        building = objects.setdefault("building", {})
        # Check for original flat structure before any transformation
        originally_flat = "refinementSurfaceLevels" in building

        building.setdefault("objectName", "building")
        building.setdefault("objectType", "obj")

        # Promote feature levels to object
        features = cmc.get("features", None)
        if features:
            for feature in to_native(features):
                file = str(feature.get("file", "")).strip('"')
                lvl = feature.get("level")
                name = (Path(file).stem if file else None) or "building"
                if name in objects and lvl is not None:
                    objects[name]["levels"] = str(lvl)
            cmc.pop("features", None)

        ip["castellatedMeshControls"] = cmc

        ref_surfs = cmc.pop("refinementSurfaces", {}) or {}
        ref_regs = cmc.pop("refinementRegions", {}) or {}

        # Setup region defaults
        regions = building.setdefault("regions", {})

        # Track which regions originally had a "name" key — snapshot BEFORE mutating regions
        original_region_has_name = {
            r: (isinstance(d, dict) and "name" in d)
            for r, d in regions.items()
        }

        # Access Walls without creating it (avoid side effects in snapshot)
        walls = regions.get("Walls", {})

        # --- Promote building-level refinementSurfaces and region-specific overrides
        try:
            bsurf = to_native(ref_surfs).get("building", {})
            global_levels = []
            global_ptype = "wall"

            if isinstance(bsurf, dict):
                # building-level (expected in your diff)
                global_levels = bsurf.get("level", []) or []
                global_ptype = bsurf.get("patchInfo", {}).get("type", "wall")

                # Always keep building.refinementSurfaces when global levels exist
                if global_levels:
                    building["refinementSurfaces"] = {
                        "levels": global_levels,
                        "patchType": global_ptype
                    }

                # Always echo global levels/type to 'Walls' if present (to match expected JSON)
                if isinstance(walls, dict) and isinstance(global_levels, list) and global_levels:
                    walls.setdefault("refinementSurfaceLevels", global_levels)
                    # don't inject name; only set type if missing
                    if "type" not in walls and isinstance(global_ptype, str):
                        walls["type"] = global_ptype

                # region-specific (mirror refSurfs; optionally inherit-if-zero)
                rregions = bsurf.get("regions", {})
                if isinstance(rregions, dict):
                    for rname, rdef in rregions.items():
                        if not isinstance(rdef, dict):
                            continue
                        region_entry = regions.get(rname)
                        if not isinstance(region_entry, dict):
                            region_entry = {}
                            regions[rname] = region_entry

                        r_levels = rdef.get("level")
                        r_type = rdef.get("type")

                        # --- apply inheritance only if originally_flat ---
                        if originally_flat:
                            # (0 0) -> inherit building levels
                            if isinstance(r_levels, list) and r_levels == [0, 0] and global_levels:
                                r_levels = global_levels
                            # patch -> inherit building type
                            if r_type == "patch" and global_ptype:
                                r_type = global_ptype
                        else:
                            # when not flat originally:
                            #  - never write region refinementSurfaceLevels for [0,0]
                            #  - keep 'patch' if that’s what the region had
                            if isinstance(r_levels, list) and r_levels == [0, 0]:
                                r_levels = None  # don't emit key

                        # write-back only when we have concrete values
                        if isinstance(r_levels, list):
                            region_entry["refinementSurfaceLevels"] = r_levels
                        if isinstance(r_type, str):
                            region_entry["type"] = r_type


        except Exception as e:
            self.log.warning(f"Failed to promote refinementSurfaces/regions: {e}")



        # Promote refinementRegions (match expected: keep empty {} on building)
        try:
            regs = to_native(ref_regs) if ref_regs else {}
            bld_rr = regs.get("building")
            if isinstance(bld_rr, dict):
                building["refinementRegions"] = bld_rr
            else:
                # expected shows empty {} even when none were defined
                building.setdefault("refinementRegions", {})

            w_rr = regs.get("Walls")
            if isinstance(w_rr, dict):
                walls["refinementRegions"] = w_rr
            else:
                # if it wasn't present, don't force it on Walls
                walls.pop("refinementRegions", None)
        except Exception as e:
            self.log.warning(f"Failed to promote refinementRegions: {e}")

        # Remove only helper keys we might have injected earlier
        for fld in ("name", "type"):  # <<< include "type" again to drop building.type
            building.pop(fld, None)

        # Add layers handling (only if explicitly provided)
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
            # only write geometry.layers if we actually have a value
            geometry.setdefault("layers", {})["nSurfaceLayers"] = nsl

        # Do NOT force-create empty geometry keys; only ensure 'objects' exists
        geometry.setdefault("objects", objects)

        # Ensure empty blocks exist to match expected structure
        geometry.setdefault("refinementSurfaces", {})
        geometry.setdefault("regions", {})

        # If these keys weren’t present originally, leave them absent
        # (no setdefault to {} here)
        ip["geometry"] = geometry

        # Clean optional flags without creating diffs
        if "writeFlags" in ip and not ip.get("writeFlags"):
            ip.pop("writeFlags", None)

        # 🔄 FINAL unwrap + cleanup
        normalize_in_place(ip)

        final_native = unwrap_booleans_and_vectors(ip)

        try:
            building = final_native["geometry"]["objects"]["building"]
            regions = building.get("regions", {})

            for rname, rdef in list(regions.items()):
                if isinstance(rdef, dict):
                    # drop 'name' only if it wasn't present in the original input
                    if not original_region_has_name.get(rname, False):
                        rdef.pop("name", None)

            walls = regions.get("Walls", {})

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

                # Decide whether to flatten
                will_flatten = False
                if originally_flat:
                    will_flatten = True
                elif isinstance(gl, list) and gl != [0, 0] and all(
                        mirrors_global_or_placeholder(d) for d in rr.values()):
                    will_flatten = True

                if will_flatten:
                    # Push global values down to regions where missing/placeholder
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

                    # Flatten building
                    building["refinementSurfaceLevels"] = gl or []
                    building["patchType"] = pt
                    building.pop("refinementSurfaces", None)


        except Exception as e:
            self.log.warning(f"Final cleanup failed: {e}")


        ip.clear()
        ip.update(final_native)

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
            self.handle_snappy_dict(final_leaf)
            # One more unwrap pass (in place) on the whole input_parameters
            normalize_in_place(final_leaf)  # to drop any PyFoam mapping shells
            final_native = unwrap_booleans_and_vectors(final_leaf)
            final_leaf.clear()
            final_leaf.update(final_native)

        return node

    def to_json_str(self, node: dict) -> str:
        return json.dumps(node, indent=4, ensure_ascii=False, cls=FoamJSONEncoder)

    def save_node(self, node: dict, out_path: str):
        save_json(node, out_path)
