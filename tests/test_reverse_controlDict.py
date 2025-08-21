import json
from pathlib import Path
from hermes.workflow.reverseOpenFOAM import DictionaryReverser
from hermes.workflow.reverseOpenFOAM import FoamJSONEncoder


# Same mock template as in real usage
class _TemplateCenterMock(dict):
    def __init__(self):
        super().__init__()
        self["openFOAM.system.ControlDict"] = {
            "Execution": {
                "input_parameters": {
                    "values": {
                        # These defaults are overwritten by merge
                        "application": "",
                        "startTime": 0,
                        "endTime": 0,
                        "deltaT": 0,
                        "functions": [],
                        "libs": []
                    }
                }
            }
        }

def test_reverse_controlDict_from_file(tmp_path: Path):
    # Copy the uploaded file into the test case
    input_path = Path("/Users/sapiriscfdc/Costumers/Hermes/pipe/caseConfiguration/system/controlDict")
    system_dir = tmp_path / "system"
    system_dir.mkdir()
    control_dict_path = system_dir / "controlDict"
    control_dict_path.write_text(input_path.read_text())

    # 2) Setup and inject the mock template
    reverser = DictionaryReverser(str(control_dict_path))
    reverser._template_center = _TemplateCenterMock()

    # 🔎 DEBUG: inspect what parse() gives you
    reverser.parse()
    # now build the node
    node = reverser.build_node()

    # Check node type
    assert node["type"] == "openFOAM.system.ControlDict"

    # Check full output content
    expected = {
        "Execution": {
            "input_parameters": {
                "values": {
                    "application": "simpleFoam",
                    "startFrom": "startTime",
                    "startTime": 0,
                    "stopAt": "endTime",
                    "endTime": 60,
                    "deltaT": 1,
                    "writeControl": "adjustableRunTime",
                    "writeInterval": 0.1,
                    "runTimeModifiable": True,
                    "interpolate": True,
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
            }
        }
    }

    assert node["Execution"]["input_parameters"]["values"] == expected["Execution"]["input_parameters"]["values"]

    print("Node built successfully:")
    print(json.dumps(node, indent=4, ensure_ascii=False, cls=FoamJSONEncoder))
