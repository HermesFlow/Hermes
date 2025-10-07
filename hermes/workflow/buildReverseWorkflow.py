import argparse
from pathlib import Path
from hermes.workflow.reverseOpenFOAM import DictionaryReverser
import json

def wrap_as_hermes_workflow(base_nodes: dict, base_nodeList: list) -> dict:
    # Add Hermes-specific nodes like Parameters, buildAllRun, etc.
    hermes_nodes = {}
    hermes_nodeList = []

    # Add Parameters node
    hermes_nodes["Parameters"] = {
        "Execution": {
            "input_parameters": {
                "OFversion": "of10",
                "targetDirectory": "{#moduleName}",
                "objectFile": "Pipe.obj",  # You might want to extract this dynamically
                "decomposeProcessors": 8
            }
        },
        "type": "general.Parameters"
    }
    hermes_nodeList.append("Parameters")

    # Remap original nodes
    mapping = {
        "blockMeshDict": "blockMesh",
        "snappyHexMeshDict": "snappyHexMesh",
        "decomposeParDict": "decomposePar",
        "controlDict": "controlDict",
        "fvSchemes": "fvSchemes",
        "fvSolution": "fvSolution",
        "thermophysicalProperties": "defineNewBoundaryConditions"
    }

    for original, hermes_name in mapping.items():
        if original in base_nodes:
            node = base_nodes[original]
            # Optionally convert `type` field to Hermes type
            if "Execution" in node:
                node["Execution"]["input_parameters"].setdefault("geometry", {})
            hermes_nodes[hermes_name] = node
            hermes_nodeList.append(hermes_name)

    # Add extra Hermes stages
    hermes_nodes["buildAllRun"] = {
        "Execution": {
            "input_parameters": {
                "casePath": "{Parameters.output.targetDirectory}",
                "caseExecution": {
                    "parallelCase": True,
                    "slurm": False,
                    "getNumberOfSubdomains": 10,
                    "runFile": []
                },
                "parallelCase": True,
                "runFile": [
                    {
                        "name": "blockMesh",
                        "couldRunInParallel": False,
                        "parameters": None
                    },
                    {
                        "name": "surfaceFeatures",
                        "parameters": "-dict system/building",
                        "couldRunInParallel": False
                    },
                    {
                        "name": "decomposePar",
                        "parameters": "-force",
                        "couldRunInParallel": False
                    },
                    {
                        "name": "snappyHexMesh",
                        "parameters": "-overwrite",
                        "couldRunInParallel": True
                    },
                    {
                        "name": "ls -d processor* | xargs -i cp -r 0.parallel/* ./{}/0/ $1",
                        "parameters": None,
                        "couldRunInParallel": False,
                        "foamJob": False
                    },
                    {
                        "name": "changeDictionary",
                        "parameters": None,
                        "couldRunInParallel": True
                    }
                ]
            }
        },
        "type": "openFOAM.BuildAllrun"
    }

    hermes_nodeList.append("buildAllRun")

    hermes_nodes["fileWriter"] = {
        "Execution": {
            "input_parameters": {
                "directoryPath": ".",
                "Files": {
                    "blockMesh": {
                        "fileName": "system/blockMeshDict",
                        "fileContent": "{blockMesh.output.openFOAMfile}"
                    },
                    "decomposePar": {
                        "fileName": "system/decomposeParDict",
                        "fileContent": "{decomposePar.output.openFOAMfile}"
                    },
                    "snappyHexMeshDict": {
                        "fileName": "system/snappyHexMeshDict",
                        "fileContent": "{snappyHexMesh.output.openFOAMfile}"
                    },
                    "g": {
                        "fileName": "constant/g",
                        "fileContent": "{g.output.openFOAMfile}"
                    },
                    "controlDict": {
                        "fileName": "system/controlDict",
                        "fileContent": "{controlDict.output.openFOAMfile}"
                    },
                    "fvSchemes": {
                        "fileName": "system/fvSchemes",
                        "fileContent": "{fvSchemes.output.openFOAMfile}"
                    },
                    "fvSolution": {
                        "fileName": "system/fvSolution",
                        "fileContent": "{fvSolution.output.openFOAMfile}"
                    },
                    "physicalProperties": {
                        "fileName": "constant/physicalProperties",
                        "fileContent": "{physicalProperties.output.openFOAMfile}"
                    },
                    "momentumTransport": {
                        "fileName": "constant/momentumTransport",
                        "fileContent": "{momentumTransport.output.openFOAMfile}"
                    },
                    "changeDictionary": {
                        "fileName": "system/changeDictionaryDict",
                        "fileContent": "{defineNewBoundaryConditions.output.openFOAMfile}"
                    },
                    "surfaceFeatures": {
                        "fileName": "system",
                        "fileContent": "{surfaceFeatures.output.openFOAMfile}"
                    }
                },
                "casePath": "{Parameters.output.targetDirectory}"
            }
        },
        "type": "general.FilesWriter"
    }

    hermes_nodeList.append("fileWriter")

    return {
        "workflow": {
            "root": None,
            "solver": "simpleFoam",  # Extract from controlDict ideally
            "SolvedFields": "p U k epsilon nut",  # Optional automation
            "AuxFields": "",
            "Templates": [],
            "nodeList": hermes_nodeList,
            "nodes": hermes_nodes
        }
    }

def build_workflow(case_dir: str, out_json_path: str, files=None):
    print("Reversing workflow...")

    known_dicts = files or [
        "system/blockMeshDict",
        "system/snappyHexMeshDict",
        "system/decomposeParDict",
        "system/controlDict",
        "system/fvSchemes",
        "system/fvSolution",
        "system/changeDictionaryDict",
        "system/surfaceFeaturesDict"
    ]

    nodes = {}
    nodeList = []

    for dict_file in known_dicts:
        path = Path(case_dir) / dict_file
        if not path.exists():
            print(f"⚠️ Skipping missing: {path}")
            continue

        print(f"🔄 Reversing: {dict_file}")
        reverser = DictionaryReverser(str(path))
        reverser.parse()
        node = reverser.build_node()
        node_name = reverser.dict_name  # e.g. "controlDict", "fvSchemes"

        nodes[node_name] = node
        nodeList.append(node_name)

    # 🔁 Now wrap it into a Hermes workflow
    workflow = wrap_as_hermes_workflow(nodes, nodeList)

    # Save workflow JSON
    with open(out_json_path, "w") as f:
        json.dump(workflow, f, indent=4)

    print(f"\n Saved reversed workflow to: {out_json_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Reverse OpenFOAM dictionaries into Hermes workflow JSON")
    parser.add_argument("--case", required=True, help="Path to the OpenFOAM case folder")
    parser.add_argument("--output", required=True, help="Path to output JSON workflow")
    args = parser.parse_args()

    build_workflow(args.case, args.output)
