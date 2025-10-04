import json
from pathlib import Path
import pytest
from hermes.workflow.reverseOpenFOAM import DictionaryReverser, FoamJSONEncoder


@pytest.mark.parametrize(
    "case_name, input_json_path, dict_path",
    [
        (
            "pipe_2",
            "/Users/sapiriscfdc/Costumers/Hermes/pipe/pipe_2.json",
            "/Users/sapiriscfdc/Costumers/Hermes/pipe/caseConfiguration/system/building",
        ),
(
            "LargeRoom_2",
            "/Users/sapiriscfdc/Costumers/Hermes/LargeRoomSimpleFoam/LargeRoom_2.json",
            "/Users/sapiriscfdc/Costumers/Hermes/LargeRoomSimpleFoam/caseConfiguration/system/building",
        ),
(
            "Flow_2",
            "/Users/sapiriscfdc/Costumers/Hermes/EWTModel/Flow_2.json",
            "/Users/sapiriscfdc/Costumers/Hermes/EWTModel/caseConfiguration/system/building",
        ),

    ],
)
def test_reverse_surfaceFeatures_against_inputs(tmp_path: Path, case_name: str, input_json_path: str, dict_path: str):
    """
    Compare reversed surfaceFeaturesDict against the expected node from reference inputs.
    """
    input_file_path = Path(input_json_path)
    dict_file_path = Path(dict_path)

    if not input_file_path.exists():
        pytest.skip(f"[{case_name}] expected JSON not found at {input_file_path}")
    if not dict_file_path.exists():
        pytest.skip(f"[{case_name}] surfaceFeaturesDict not found at {dict_file_path}")

    with open(input_file_path, "r") as f:
        input_json = json.load(f)

    expected = input_json["workflow"]["nodes"]["surfaceFeatures"]

    # Temp directory for parsing
    system_dir = tmp_path / case_name / "system"
    system_dir.mkdir(parents=True, exist_ok=True)
    dst = system_dir / "surfaceFeaturesDict"
    dst.write_text(dict_file_path.read_text())

    # Reverse
    reverser = DictionaryReverser(str(dst))
    reverser.parse()
    node = reverser.build_node()

    # Debug print to inspect structure
    print(f"[DEBUG] Built node for {case_name}:\n{json.dumps(node, indent=2, cls=FoamJSONEncoder)}")

    actual = node

    assert actual == expected, (
        f"[{case_name}] surfaceFeaturesDict reverse mismatch.\n"
        f"Actual:\n{json.dumps(actual, indent=2, cls=FoamJSONEncoder)}\n\n"
        f"Expected:\n{json.dumps(expected, indent=2, cls=FoamJSONEncoder)}"
    )
