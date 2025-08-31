import json
from pathlib import Path
import pytest
from hermes.workflow.reverseOpenFOAM import DictionaryReverser
from hermes.workflow.reverseOpenFOAM import FoamJSONEncoder


# Same mock template as in real usage


@pytest.mark.parametrize("input_path,expected_values", [

    # Case 1: pipe
    (
        "/Users/sapiriscfdc/Costumers/Hermes/pipe/caseConfiguration/system/controlDict",
        {
            "application": "simpleFoam",
            "startFrom": "startTime",
            "startTime": 0,
            "stopAt": "endTime",
            "endTime": 60,
            "deltaT": 1,
            "writeControl": "adjustableRunTime",
            "writeInterval": 0.1,
            "runTimeModifiable": True,
            "adjustTimeStep": True,
            "purgeWrite": 0,
            "writeFormat": "ascii",
            "writePrecision": 7,
            "writeCompression": False,
            "timeFormat": "general",
            "timePrecision": 6,
            "maxCo": 0.5,
            "functions": [],
            "libs": []
        }
    ),

    # Case 2: EWTModel
    (
        "/Users/sapiriscfdc/Costumers/Hermes/EWTModel/caseConfiguration/system/controlDict",
        {
            "application": "simpleFoam",   # "{workflow.solver}"
            "startFrom": "startTime",
            "startTime": 0,
            "stopAt": "endTime",
            "endTime": 600,
            "deltaT": 0.01,
            "writeControl": "adjustableRunTime",
            "writeInterval": 1,
            "runTimeModifiable": True,
            "adjustTimeStep": True,
            "purgeWrite": 0,
            "writeFormat": "ascii",
            "writePrecision": 7,
            "writeCompression": False,
            "timeFormat": "general",
            "timePrecision": 6,
            "maxCo": 0.5,
            "functions": [],
            "libs": []
        }
    ),

    # Case 3: LargeRoomSimpleFoam
    (
        "/Users/sapiriscfdc/Costumers/Hermes/LargeRoomSimpleFoam/caseConfiguration/system/controlDict",
        {
            "application": "simpleFoam",
            "startFrom": "startTime",
            "startTime": 0,
            "stopAt": "endTime",
            "endTime": 60,
            "deltaT": 1,
            "writeControl": "adjustableRunTime",
            "writeInterval": 0.1,
            "runTimeModifiable": True,
            "adjustTimeStep": True,
            "purgeWrite": 0,
            "writeFormat": "ascii",
            "writePrecision": 7,
            "writeCompression": False,
            "timeFormat": "general",
            "timePrecision": 6,
            "maxCo": 0.5,
            "functions": [],
            "libs": []
        }
    )
])
def test_reverse_controlDict_cases(tmp_path: Path, input_path, expected_values):
    """Parametrized test for multiple controlDict cases."""

    # Copy the uploaded file into the test case
    input_path = Path(input_path)
    system_dir = tmp_path / "system"
    system_dir.mkdir()
    control_dict_path = system_dir / "controlDict"
    control_dict_path.write_text(input_path.read_text())

    # Setup the reverser and parse the controlDict
    reverser = DictionaryReverser(str(control_dict_path))
    reverser.parse()
    node = reverser.build_node()

    assert node["type"] == "openFOAM.system.ControlDict"

    actual = node["Execution"]["input_parameters"]["values"]
    assert actual == expected_values, (
        f"ControlDict {input_path} did not match expected.\n"
        f"Actual:\n{json.dumps(actual, indent=2, cls=FoamJSONEncoder)}"
    )

    print(f"Node built successfully for {input_path}")
    print(json.dumps(node, indent=4, ensure_ascii=False, cls=FoamJSONEncoder))
