import json
from pathlib import Path
import pytest
from hermes.workflow.reverseOpenFOAM import DictionaryReverser, FoamJSONEncoder

# Normalize optional keys to avoid false mismatches
def _normalize_optional_keys(doc: dict) -> None:
    try:
        geo = doc["Execution"]["input_parameters"].get("geometry")
        if isinstance(geo, dict) and geo.get("gemeotricalEntities") == {}:
            geo.pop("gemeotricalEntities")
    except Exception:
        pass
"""
(
            "Flow_1",
            "RASProperties",
            "/Users/sapiriscfdc/Costumers/Hermes/EWTModel/Flow_2.json",
            "/Users/sapiriscfdc/Costumers/Hermes/EWTModel/caseConfiguration/constant/momentumTransport",
            "momentumTransport",
            "openFOAM.constant.momentumTransport"
        ),
        
        
"""

@pytest.mark.parametrize(
    "case_name, dict_name, input_json_path, dict_file_path, expected_node_key, expected_type",
    [
        (
            "Flow_1",
            "g",
            "/Users/sapiriscfdc/Costumers/Hermes/EWTModel/Flow_2.json",
            "/Users/sapiriscfdc/Costumers/Hermes/EWTModel/caseConfiguration/constant/g",
            "g",
            "openFOAM.constant.g"
        ),
        (
            "Flow_1",
            "transportProperties",
            "/Users/sapiriscfdc/Costumers/Hermes/EWTModel/Flow_2.json",
            "/Users/sapiriscfdc/Costumers/Hermes/EWTModel/caseConfiguration/constant/physicalProperties",
            "physicalProperties",
            "openFOAM.constant.physicalProperties"
        ),


    ]
)
def test_reverse_constant_dicts_v2(
    tmp_path: Path,
    case_name: str,
    dict_name: str,
    input_json_path: str,
    dict_file_path: str,
    expected_node_key: str,
    expected_type: str
):
    """
    Test constant/ dictionaries (g, RASProperties, transportProperties) and compare reversed node to reference JSON.
    """
    input_file = Path(input_json_path)
    dict_file = Path(dict_file_path)

    if not input_file.exists():
        pytest.skip(f"[{case_name}] JSON not found at {input_file}")
    if not dict_file.exists():
        pytest.skip(f"[{case_name}] {dict_name} not found at {dict_file}")

    with open(input_file, "r") as f:
        reference_workflow = json.load(f)

    expected = reference_workflow["workflow"]["nodes"][expected_node_key]

    # Create temporary file for reverse parsing
    const_dir = tmp_path / case_name / "constant"
    const_dir.mkdir(parents=True, exist_ok=True)
    dst = const_dir / dict_name
    dst.write_text(dict_file.read_text())

    reverser = DictionaryReverser(str(dst))
    reverser.parse()
    node = reverser.build_node()

    actual = {
        "Execution": node["Execution"],
        "type": expected_type,
        "version": 2
    }

    # Optional cleanup
    _normalize_optional_keys(actual)
    _normalize_optional_keys(expected)

    assert actual == expected, (
        f"[{case_name}] {dict_name} reverse does not match expected.\n"
        f"Actual:\n{json.dumps(actual, indent=2, cls=FoamJSONEncoder)}\n\n"
        f"Expected:\n{json.dumps(expected, indent=2, cls=FoamJSONEncoder)}"
    )
