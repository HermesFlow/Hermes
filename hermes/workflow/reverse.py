import argparse
import json
from pathlib import Path
from .reverseOpenFOAM import DictionaryReverser
from hermes.Resources.openFOAM.BuildAllrun.executer import BuildAllrun
from hermes.Resources.general.FilesWriter.executer import FilesWriter



class HermesEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, '__dict__'):
            return obj.__dict__
        if hasattr(obj, '__str__'):
            return str(obj)
        return super().default(obj)

def find_dicts(case_path: Path) -> dict[str, Path]:
    """
    Find dictionary files in system/, constant/, and 0/
    """
    found = {}
    for subdir in ["system", "constant", "0"]:
        sub_path = case_path / subdir
        if not sub_path.exists():
            continue
        for file in sub_path.iterdir():
            if file.is_file():
                found[file.name] = file
    return found


def build_parameters_node(case_path: Path) -> dict:
    """
    Create a Parameters node based on the folder name and guessed values.
    """
    case_name = case_path.name

    return {
        "Parameters": {
            "Execution": {
                "input_parameters": {
                    "OFversion": "of10",
                    "targetDirectory": case_name,
                    "objectFile": f"{case_name}.obj",
                    "decomposeProcessors": 4
                }
            },
            "type": "general.Parameters"
        }
    }


def build_workflow(case_path: Path, template_paths=None) -> dict:
    all_dicts = find_dicts(case_path)
    print(f" Found {len(all_dicts)} dictionary files.")
    nodes = {}

    for filename, filepath in all_dicts.items():
        dict_name = Path(filename).stem

        if filepath.parts[-2] == "0" and dict_name not in ("changeDictionaryDict",):
            print(f"Skipping field file from 0/: {filename}")
            continue

        try:
            print(f" Reversing: {filename}")
            reverser = DictionaryReverser(str(filepath), template_paths=template_paths)
            reverser.parse()
            print(f" Checking {filename} as {dict_name}")

            node_dict = reverser.build_node()
            nodes[dict_name] = node_dict[dict_name]

            print(f"Finished: {list(node_dict.keys())[0]}")
        except Exception as e:
            print(f"Error reversing {filename}: {e}")

    # Inject Parameters node if missing
    if "Parameters" not in nodes:
        nodes.update(build_parameters_node(case_path))

    # Dynamically build run steps only for available nodes
    run_steps = []

    if "blockMeshDict" in nodes:
        run_steps.append({
            "name": "blockMesh",
            "parameters": None,
            "couldRunInParallel": False
        })

    if "surfaceFeaturesDict" in nodes:
        run_steps.append({
            "name": "surfaceFeatures",
            "parameters": "-dict system/building",
            "couldRunInParallel": False
        })

    if "decomposeParDict" in nodes:
        run_steps.append({
            "name": "decomposePar",
            "parameters": "-force",
            "couldRunInParallel": False
        })

    if "snappyHexMeshDict" in nodes:
        run_steps.append({
            "name": "snappyHexMesh",
            "parameters": "-overwrite",
            "couldRunInParallel": True
        })

    # Always include this step
    run_steps.append({
        "name": "ls -d processor* | xargs -i cp -r 0.parallel/* ./{}/0/ $1",
        "parameters": None,
        "couldRunInParallel": False,
        "foamJob": False
    })

    if "defineNewBoundaryConditionsDict" in nodes:
        run_steps.append({
            "name": "changeDictionary",
            "parameters": None,
            "couldRunInParallel": True
        })

    # Add buildAllRun node
    # Create input params
    build_inputs = {
        "casePath": "{Parameters.output.targetDirectory}",
        "parallelCase": True,
        "slurm": False,
        "getNumberOfSubdomains": 10,
        "runFile": run_steps
    }

    build_exec = BuildAllrun({})
    build_node = build_exec.json() or {}
    build_node.update({
        "Execution": {
            "input_parameters": build_inputs
        },
        "type": "openFOAM.BuildAllrun"
    })
    nodes["buildAllRun"] = build_node

    files = {}
    for node_name, node_data in nodes.items():
        if node_name in {"buildAllRun", "fileWriter", "Parameters"}:
            continue  # skip non-dictionary nodes

        # Try to infer original path from dictionary object or guess it
        default_dir = "system"
        if node_name in ["g", "physicalProperties", "momentumTransport"]:
            default_dir = "constant"
        elif node_name in ["epsilon", "U", "p", "k", "nut"]:
            default_dir = "0"

        file_path = f"{default_dir}/{node_name}"

        files[node_name] = {
            "fileName": file_path,
            "fileContent": f"{{{node_name}.output.openFOAMfile}}"
        }

    # Add fileWriter node
    files_writer_inputs = {
        "directoryPath": ".",
        "Files": files,
        "casePath": "{Parameters.output.targetDirectory}"
    }

    file_writer_exec = FilesWriter({})
    file_writer_node = file_writer_exec.json() or {}
    file_writer_node.update({
        "Execution": {
            "input_parameters": files_writer_inputs
        },
        "type": "general.FilesWriter"
    })
    nodes["fileWriter"] = file_writer_node

    node_list = list(nodes.keys())


    return {
        "workflow": {
            "version": 2,
            "root": None,
            "solver": "simpleFoam",
            "SolvedFields": "p U k epsilon nut",
            "AuxFields": "",
            "Templates": [],
            "nodeList": node_list,
            "nodes": nodes
        }
    }





def main():
    parser = argparse.ArgumentParser(description="Reverse OpenFOAM case folder to Hermes workflow JSON")
    parser.add_argument("case_path", type=str, help="Path to the OpenFOAM case folder")
    parser.add_argument("--output", "-o", type=str, help="Optional path to save JSON")
    parser.add_argument("--template-paths", "-t", nargs="*", help="Optional template paths")
    parser.add_argument("--save", action="store_true", help="Save the result to file instead of printing")

    args = parser.parse_args()
    case_path = Path(args.case_path)

    if not case_path.exists():
        print(f"Error: Path does not exist: {case_path}")
        return

    workflow = build_workflow(case_path, template_paths=args.template_paths)

    if args.save and args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(workflow, f, indent=4, ensure_ascii=False, cls=HermesEncoder)
        print(f"Saved Hermes workflow to: {args.output}")
    else:
        print(json.dumps(workflow, indent=4, ensure_ascii=False, cls=HermesEncoder))


if __name__ == "__main__":
    main()
