from __future__ import annotations

from PyFoam.RunDictionary.ParsedParameterFile import ParsedParameterFile
from PyFoam.Basics.DataStructures import Vector, BoolProxy
from ..Resources.reTemplateCenter import templateCenter
from ..utils.logging import get_classMethod_logger
from pathlib import Path
from typing import Any, Dict, Tuple, Optional
import json, copy, pydoc


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
        # 1) modules {castellatedMesh,snap,layers,mergeTolerance}
        normalize_in_place(ip)

        modules = {}
        sentinel = object()
        for key in ("castellatedMesh", "snap", "addLayers", "mergeTolerance"):
            val = ip.pop(key, sentinel)
            if val is not sentinel:
                # coerce BoolProxy to bool if needed
                try:
                    from PyFoam.Basics.DataStructures import BoolProxy
                    if isinstance(val, BoolProxy):
                        val = bool(val)
                except Exception:
                    pass
                modules["layers" if key == "addLayers" else key] = val
        if modules:
            ip["modules"] = modules

        # 2) normalize castellatedMeshControls.locationInMesh
        cmc = ip.setdefault("castellatedMeshControls", {})
        normalize_in_place(cmc)
        try:
            loc = cmc.get("locationInMesh")
            if isinstance(loc, str):
                parts = loc.strip("()").split()
                cmc["locationInMesh"] = [float(p) for p in parts]
        except Exception as e:
            self.log.warning(f"Failed to normalize locationInMesh: {e}")

        # 3) prepare geometry + objects
        geometry = ip.setdefault("geometry", {})
        objects = geometry.setdefault("objects", {})
        normalize_in_place(objects)

        # 3a) SAFE hoist of *.obj entries into objects[name]
        #     Work from a native snapshot so we never call PyFoam __getitem__ on 'building.obj'
        try:
            normalize_in_place(geometry)
            for k, v in list(geometry.items()):
                if isinstance(k, str) and k.endswith(".obj"):
                    # Determine object name
                    name = None
                    if isinstance(v, dict):
                        name = v.get("name")
                    if not name:
                        from pathlib import Path as _P
                        name = _P(k).stem

                    tgt = objects.setdefault(name, {})
                    if isinstance(v, dict):
                        tgt.update(v)

                    # Expected headers on the object
                    tgt.setdefault("objectName", name)
                    tgt.setdefault("objectType", "obj")

                    # Try to remove the *.obj key from the PyFoam map (ignore failures)
                    try:
                        if hasattr(geometry, "pop"):
                            geometry.pop(k, None)
                    except Exception:
                        pass
        except Exception as e:
            self.log.warning(f"Failed hoisting triSurface objects: {e}")

        # 4) ensure typo-preserved key
        geometry.setdefault("gemeotricalEntities", {})

        # 5) Ensure a building object exists and has expected headers
        building = objects.setdefault("building", {})
        building.setdefault("objectName", "building")
        building.setdefault("objectType", "obj")

        # 6) Migrate features[*].file -> objects[*].levels (string "1" expected)
        features = None
        try:
            features = cmc.get("features", None)
        except Exception as e:
            self.log.warning(f"Could not safely access 'features': {e}")

        if features:
            for feature in to_native(features):
                file = str(feature.get("file", "")).strip('"')
                lvl = feature.get("level")
                name = (Path(file).stem if file else None) or "building"
                if name in objects and lvl is not None:
                    objects[name]["levels"] = str(lvl)
            try:
                cmc.pop("features", None)
            except Exception:
                pass
        ip["castellatedMeshControls"] = cmc

        # 7) Promote refinementSurfaces / refinementRegions from cmc into 'building' + Walls
        ref_surfs = cmc.pop("refinementSurfaces", {}) or {}
        ref_regs = cmc.pop("refinementRegions", {}) or {}

        # build/ensure regions
        regions = building.setdefault("regions", {})
        walls = regions.setdefault("Walls", {"name": "Walls"})
        regions.setdefault("inlet", {"name": "inlet", "type": "patch"})
        regions.setdefault("outlet", {"name": "outlet", "type": "patch"})

        # Ensure inlet/outlet always have type patch even if they already exist
        for rn in ("inlet", "outlet"):
            if rn in regions and isinstance(regions[rn], dict):
                regions[rn].setdefault("type", "patch")
            else:
                regions[rn] = {"name": rn, "type": "patch"}

        # refinementSurfaces -> building.refinementSurfaces + Walls.refinementSurfaceLevels
        try:
            bsurf = to_native(ref_surfs).get("building", {})
            if isinstance(bsurf, dict):
                levels = bsurf.get("level", [])
                ptype = bsurf.get("patchInfo", {}).get("type", "wall")
                if levels:
                    building["refinementSurfaces"] = {
                        "levels": levels,
                        "patchType": ptype
                    }
                    walls["refinementSurfaceLevels"] = levels
                    walls["type"] = ptype
        except Exception as e:
            self.log.warning(f"Failed to promote refinementSurfaces: {e}")

        # refinementRegions -> building.refinementRegions + Walls.refinementRegions
        try:
            regs = to_native(ref_regs)
            if "Walls" in regs:
                walls["refinementRegions"] = regs["Walls"]
            # Ensure building has an empty dict (as per expected)
            building["refinementRegions"] = building.get("refinementRegions", {}) or {}

        except Exception as e:
            self.log.warning(f"Failed to promote refinementRegions: {e}")

        # 8) Clean name/type duplication on building (keep on walls)
        for fld in ("name", "type"):
            building.pop(fld, None)

        # 9) addLayersControls defaults and move nSurfaceLayers
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
                try:
                    alc.pop("layers", None)
                except Exception:
                    pass
        ip["addLayersControls"] = alc

        if nsl is not None:
            building.setdefault("layers", {})["nSurfaceLayers"] = nsl

        # 10) Duplicate top-level geometry mirrors required by expected JSON
        #     (these "empty shells" live alongside geometry.objects)
        #     geometry.layers.nSurfaceLayers should mirror building.layers.nSurfaceLayers
        top_layers = {}
        if nsl is not None:
            top_layers["nSurfaceLayers"] = nsl
        geometry["layers"] = top_layers or {"nSurfaceLayers": building.get("layers", {}).get("nSurfaceLayers", 10)}
        geometry.setdefault("refinementSurfaces", {})
        geometry.setdefault("regions", {})

        # 11) Reassign geometry to contain ONLY wanted keys (drop any lingering '*.obj')
        ip["geometry"] = {
            "objects": objects,
            "gemeotricalEntities": geometry.get("gemeotricalEntities", {}),
            "refinementSurfaces": geometry.get("refinementSurfaces", {}),
            "regions": geometry.get("regions", {}),
            "layers": geometry.get("layers", {}),
        }

        # 12) If writeFlags is empty -> remove
        if not ip.get("writeFlags"):
            ip.pop("writeFlags", None)

        # Final unwrap: remove BoolProxy/Vector wrappers everywhere
        final_native = unwrap_booleans_and_vectors(ip)
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
