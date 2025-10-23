import json
from pathlib import Path
import pytest
from hermes.workflow.reverseOpenFOAM import DictionaryReverser, FoamJSONEncoder

"""
(
            "Flow_1",
            "g",
            "/Users/sapiriscfdc/Costumers/Hermes/EWTModel/caseConfiguration/constant/g",
            "openFOAM.constant.g"
        ),
        (
            "Flow_1",
            "transportProperties",
            "/Users/sapiriscfdc/Costumers/Hermes/EWTModel/caseConfiguration/constant/physicalProperties",
            "openFOAM.constant.physicalProperties"
        ),
"""
@pytest.mark.parametrize(
    "case_name, dict_name, dict_file_path, expected_type",
    [
(
            "T3A",
            "momentumTransport",
            "/Users/sapiriscfdc/Costumers/Hermes/ReverseCases/simpleFoam/T3A/constant/momentumTransport",
            "openFOAM.constant.momentumTransport"
        ),

    ]
)
def test_reverse_and_print_only(
    tmp_path: Path,
    case_name: str,
    dict_name: str,
    dict_file_path: str,
    expected_type: str
):
    """
    Reverse OpenFOAM dictionary and print the resulting Hermes node (no assertions or comparisons).
    """
    dict_file = Path(dict_file_path)

    if not dict_file.exists():
        pytest.skip(f"[{case_name}] {dict_name} not found at {dict_file}")

    # Create temporary copy
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

    print(f"\n🔄 Reversed node for [{case_name}] ({dict_name}):")
    print(json.dumps(actual, indent=2, cls=FoamJSONEncoder))
