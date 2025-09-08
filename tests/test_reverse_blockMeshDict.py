import json
from pathlib import Path
import pytest
from hermes.workflow.reverseOpenFOAM import DictionaryReverser, FoamJSONEncoder

def _normalize_optional_empty_geometry_keys(doc: dict) -> None:
    try:
        geo = doc["Execution"]["input_parameters"]["geometry"]
    except Exception:
        return
    if isinstance(geo.get("gemeotricalEntities", None), dict) and not geo["gemeotricalEntities"]:
        geo.pop("gemeotricalEntities", None)


@pytest.mark.parametrize(
    "case_name, input_json_path, dict_path",
    [
        (
            "pipe_2",
            "/Users/sapiriscfdc/Costumers/Hermes/pipe/pipe_2.json",
            "/Users/sapiriscfdc/Costumers/Hermes/pipe/caseConfiguration/system/blockMeshDict",
        ),
        (
            "LargeRoom_2",
            "/Users/sapiriscfdc/Costumers/Hermes/LargeRoomSimpleFoam/LargeRoom_2.json",
            "/Users/sapiriscfdc/Costumers/Hermes/LargeRoomSimpleFoam/caseConfiguration/system/blockMeshDict",
        ),
        (
            "Flow_2",
            "/Users/sapiriscfdc/Costumers/Hermes/EWTModel/Flow_2.json",
            "/Users/sapiriscfdc/Costumers/Hermes/EWTModel/caseConfiguration/system/blockMeshDict",
        ),

    ],
)
def test_reverse_blockMeshDict_against_inputs(tmp_path: Path, case_name: str, input_json_path: str, dict_path: str):
    """
    Compare reversed blockMeshDict against the expected node from reference inputs.
    """
    input_file_path = Path(input_json_path)
    dict_file_path = Path(dict_path)

    if not input_file_path.exists():
        pytest.skip(f"[{case_name}] expected JSON not found at {input_file_path}")
    if not dict_file_path.exists():
        pytest.skip(f"[{case_name}] blockMeshDict not found at {dict_file_path}")

    with open(input_file_path, "r") as f:
        input_json = json.load(f)

    expected = input_json["workflow"]["nodes"]["blockMesh"]

    # Temporary test directory
    system_dir = tmp_path / case_name / "system"
    system_dir.mkdir(parents=True, exist_ok=True)
    dst = system_dir / "blockMeshDict"
    dst.write_text(dict_file_path.read_text())

    # Reverse the dictionary
    reverser = DictionaryReverser(str(dst))
    reverser.parse()
    print("Loaded file:", dst)
    print("File contents:\n", dst.read_text())

    node = reverser.build_node()

    actual = {
        "Execution": node["Execution"],
        "type": "openFOAM.mesh.BlockMesh"
    }
    """
    # Normalize optional empty geometry
    _normalize_optional_empty_geometry_keys(actual)
    _normalize_optional_empty_geometry_keys(expected)
    """
    assert actual == expected, (
        f"[{case_name}] blockMeshDict reverse result does not match expected.\n"
        f"Actual:\n{json.dumps(actual, indent=2, cls=FoamJSONEncoder)}\n\n"
        f"Expected:\n{json.dumps(expected, indent=2, cls=FoamJSONEncoder)}"
    )
