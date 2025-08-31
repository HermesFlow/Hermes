import json
from pathlib import Path
import pytest
from hermes.workflow.reverseOpenFOAM import DictionaryReverser
from hermes.workflow.reverseOpenFOAM import FoamJSONEncoder
import copy


def test_reverse_snappyHexMeshDict_against_input(tmp_path: Path):
    """
    Compare reversed snappyHexMeshDict against the expected node from pipe_1 input file.
    """

    # Load expected JSON input file
    input_file_path = Path("/Users/sapiriscfdc/Costumers/Hermes/pipe/pipe_1.json")
    with open(input_file_path, "r") as f:
        input_json = json.load(f)

    expected = input_json["workflow"]["nodes"]["snappyHexMesh"]

    # Locate source dictionary file
    src = Path("/Users/sapiriscfdc/Costumers/Hermes/pipe/caseConfiguration/system/snappyHexMeshDict")
    if not src.exists():
        alt = Path("/Users/sapiriscfdc/Costumers/Hermes/LargeRoomSimpleFoam/caseConfiguration/system/snappyHexMeshDict")
        if alt.exists():
            src = alt
        else:
            pytest.skip("snappyHexMeshDict not found on this machine; skipping test.")

    # Create a temporary isolated system directory
    system_dir = tmp_path / "system"
    system_dir.mkdir()
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

    assert actual == expected, (
        "snappyHexMeshDict reverse result does not match expected.\n"
        f"Actual:\n{json.dumps(actual, indent=2, cls=FoamJSONEncoder)}\n\n"
        f"Expected:\n{json.dumps(expected, indent=2, cls=FoamJSONEncoder)}"
    )

    print("snappyHexMeshDict matches expected structure from pipe_1 input.")
