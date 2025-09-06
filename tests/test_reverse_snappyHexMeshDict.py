import json
from pathlib import Path
import pytest
from hermes.workflow.reverseOpenFOAM import DictionaryReverser
from hermes.workflow.reverseOpenFOAM import FoamJSONEncoder

def _strip_redundant_region_names(doc: dict) -> None:
    """
    In-place: drop regions[*].name when it redundantly equals the region key.
    (snappyHexMesh uses the region dict key as the patch name.)
    """
    try:
        objs = doc["Execution"]["input_parameters"]["geometry"]["objects"]
    except Exception:
        return
    if not isinstance(objs, dict):
        return

    for _, obj in objs.items():
        if not isinstance(obj, dict):
            continue
        regions = obj.get("regions")
        if not isinstance(regions, dict):
            continue
        for rkey, rdef in regions.items():
            if isinstance(rdef, dict):
                if rdef.get("name") == rkey:
                    rdef.pop("name", None)


def _normalize_optional_empty_geometry_keys(doc: dict) -> None:
    """
    In-place: treat optional empty geometry keys as equivalent to missing.
    Currently handles 'gemeotricalEntities'.
    """
    try:
        geo = doc["Execution"]["input_parameters"]["geometry"]
    except Exception:
        return
    if isinstance(geo.get("gemeotricalEntities", None), dict) and not geo["gemeotricalEntities"]:
        # empty dict -> remove
        geo.pop("gemeotricalEntities", None)


@pytest.mark.parametrize(
    "case_name, input_json_path, dict_path",
    [
        (
            "pipe_2",
            "/Users/sapiriscfdc/Costumers/Hermes/pipe/pipe_2.json",
            "/Users/sapiriscfdc/Costumers/Hermes/pipe/caseConfiguration/system/snappyHexMeshDict",
        ),
        (
            "LargeRoom_2",
            "/Users/sapiriscfdc/Costumers/Hermes/LargeRoomSimpleFoam/LargeRoom_2.json",
            "/Users/sapiriscfdc/Costumers/Hermes/LargeRoomSimpleFoam/caseConfiguration/system/snappyHexMeshDict",
        ),
        (
            "Flow_1",
            "/Users/sapiriscfdc/Costumers/Hermes/EWTModel/Flow_2.json",
            "/Users/sapiriscfdc/Costumers/Hermes/EWTModel/caseConfiguration/system/snappyHexMeshDict",
        ),
    ],
)
def test_reverse_snappyHexMeshDict_against_inputs(tmp_path: Path, case_name: str, input_json_path: str, dict_path: str):
    """
    Compare reversed snappyHexMeshDict against the expected node from reference inputs.
    """
    input_file_path = Path(input_json_path)
    dict_file_path = Path(dict_path)

    # Skip cleanly if this case isn't available locally
    if not input_file_path.exists():
        pytest.skip(f"[{case_name}] expected JSON not found at {input_file_path}")
    if not dict_file_path.exists():
        pytest.skip(f"[{case_name}] snappyHexMeshDict not found at {dict_file_path}")

    # Load expected JSON input file
    with open(input_file_path, "r") as f:
        input_json = json.load(f)

    expected = input_json["workflow"]["nodes"]["snappyHexMesh"]

    # Create a unique temporary isolated system directory for this param case
    system_dir = tmp_path / case_name / "system"
    system_dir.mkdir(parents=True, exist_ok=True)
    dst = system_dir / "snappyHexMeshDict"
    dst.write_text(dict_file_path.read_text())

    # Reverse the dictionary
    reverser = DictionaryReverser(str(dst))
    reverser.parse()
    node = reverser.build_node()

    # Wrap it to match structure of input JSON
    actual = {
        "Execution": node["Execution"],
        "type": "openFOAM.mesh.SnappyHexMesh"
    }

    # normalize optional keys on both sides
    _normalize_optional_empty_geometry_keys(actual)
    _normalize_optional_empty_geometry_keys(expected)

    # ignore redundant "name" in regions (e.g., inlet/outlet/Walls)
    _strip_redundant_region_names(actual)
    _strip_redundant_region_names(expected)

    assert actual == expected, (
        f"[{case_name}] snappyHexMeshDict reverse result does not match expected.\n"
        f"Actual:\n{json.dumps(actual, indent=2, cls=FoamJSONEncoder)}\n\n"
        f"Expected:\n{json.dumps(expected, indent=2, cls=FoamJSONEncoder)}"
    )
