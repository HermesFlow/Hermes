import json
from pathlib import Path

from hermes.workflow.reverseOpenFOAM import DictionaryReverser

# --- test-only mock template center ---
class _TemplateCenterMock(dict):
    def __init__(self):
        super().__init__()
        self["openFOAM.system.ControlDict"] = {
            "Execution": {
                "input_parameters": {
                    "values": {
                        "application": "simpleFoam",
                        "startTime": 0,
                        "endTime": 0,
                        "deltaT": 1
                    }
                }
            }
        }

def test_reverse_controlDict(tmp_path: Path):
    # 1) Create a temp system/controlDict
    case_sys = tmp_path / "system"
    case_sys.mkdir(parents=True, exist_ok=True)
    controlDict = case_sys / "controlDict"
    controlDict.write_text(
        """/*--------------------------------*- C++ -*----------------------------------*\\
    | =========                 |                                                 |
    | \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox           |
    |  \\    /   O peration     | Version:  v2212                                 |
    |   \\  /    A nd           | Website:  www.openfoam.com                      |
    |    \\/     M anipulation  |                                                 |
    \\*---------------------------------------------------------------------------*/
    FoamFile
    {
        version     2.0;
        format      ascii;
        class       dictionary;
        location    "system";
        object      controlDict;
    }
    // * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //
    application     simpleFoam;
    startFrom       startTime;
    startTime       0;
    stopAt          endTime;
    endTime         60;
    deltaT          1;
    writeControl    timeStep;
    writeInterval   10;
    purgeWrite      0;
    writeFormat     ascii;
    writePrecision  6;
    writeCompression off;
    timeFormat      general;
    timePrecision   6;
    runTimeModifiable true;

    // ************************************************************************* //
    """
    )



    # 2) Instantiate reverser and inject the mock template center
    r = DictionaryReverser(str(controlDict))
    r._template_center = _TemplateCenterMock()

    # 3) Build the node
    node = r.build_node()

    # 4) Assert and print
    assert node["type"] == "openFOAM.system.ControlDict"
    values = node["Execution"]["input_parameters"]["values"]
    assert values["application"] == "simpleFoam"
    assert values["endTime"] == 60

    print(json.dumps(node, indent=2))
