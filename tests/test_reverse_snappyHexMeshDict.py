import json
from pathlib import Path
import pytest
from hermes.workflow.reverseOpenFOAM import DictionaryReverser
from hermes.workflow.reverseOpenFOAM import FoamJSONEncoder

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
    ],
)
def test_reverse_snappyHexMeshDict_against_inputs(tmp_path: Path, case_name: str, input_json_path: str, dict_path: str):
    """
    Compare reversed snappyHexMeshDict against the expected node from two reference inputs.
    """
    # Load expected JSON input file
    input_file_path = Path(input_json_path)
    with open(input_file_path, "r") as f:
        input_json = json.load(f)

    expected = input_json["workflow"]["nodes"]["snappyHexMesh"]

    # Locate source dictionary file
    src = Path(dict_path)

    # Create a unique temporary isolated system directory for this param case
    system_dir = tmp_path / case_name / "system"
    system_dir.mkdir(parents=True, exist_ok=True)
    dst = system_dir / "snappyHexMeshDict"
    dst.write_text(src.read_text())

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

    assert actual == expected, (
        f"[{case_name}] snappyHexMeshDict reverse result does not match expected.\n"
        f"Actual:\n{json.dumps(actual, indent=2, cls=FoamJSONEncoder)}\n\n"
        f"Expected:\n{json.dumps(expected, indent=2, cls=FoamJSONEncoder)}"
    )
