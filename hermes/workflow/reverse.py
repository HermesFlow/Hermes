import argparse
import json
from pathlib import Path
from .reverseOpenFOAM import DictionaryReverser

class HermesEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, '__dict__'):
            return obj.__dict__
        if hasattr(obj, '__str__'):
            return str(obj)
        return super().default(obj)

# Ordered nodes for Hermes workflow (preferred display order)
DEFAULT_NODE_ORDER = [
    "Parameters",
    "blockMeshDict",
    "snappyHexMeshDict",
    "surfaceFeatures",
    "decomposeParDict",
    "controlDict",
    "fvSchemes",
    "fvSolution",
    "physicalProperties",
    "momentumTransport",
    "defineNewBoundaryConditions",
    "buildAllRun",
    "fileWriter"
]

# Map from OpenFOAM dict filenames to Hermes node names
DICT_TO_NODE_NAME = {
    "blockMeshDict": "blockMesh",
    "snappyHexMeshDict": "snappyHexMesh",
    "surfaceFeaturesDict": "surfaceFeatures",
    "decomposeParDict": "decomposePar",
    "controlDict": "controlDict",
    "fvSchemes": "fvSchemes",
    "fvSolution": "fvSolution",
    "changeDictionaryDict": "defineNewBoundaryConditions",
    "thermophysicalProperties": "physicalProperties",
    "momentumTransport": "momentumTransport",
    "g": "g"
}


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


def build_workflow(case_path: Path, template_paths=None) -> dict:
    """
    Build Hermes-style workflow JSON by reversing all OpenFOAM dictionaries.
    """
    all_dicts = find_dicts(case_path)
    print(f"🔍 Found {len(all_dicts)} dictionary files.")
    nodes = {}

    for filename, filepath in all_dicts.items():
        dict_name = Path(filename).stem

        # 🚫 Skip most files from 0/ unless specifically needed
        if filepath.parts[-2] == "0" and dict_name not in ("changeDictionaryDict",):
            print(f"⚠️ Skipping field file from 0/: {filename}")
            continue

        try:
            print(f"🔄 Reversing: {filename}")
            reverser = DictionaryReverser(str(filepath), template_paths=template_paths)
            reverser.parse()
            node_dict = reverser.build_node()

            # Update with returned dict: {dict_name: node}
            nodes.update(node_dict)

            print(f"✅ Finished: {list(node_dict.keys())[0]}")

        except Exception as e:
            print(f"❌ Error reversing {filename}: {e}")

    # Finalize node list
    ordered_nodes = [n for n in DEFAULT_NODE_ORDER if n in nodes]
    remaining_nodes = [n for n in nodes if n not in ordered_nodes]
    node_list = ordered_nodes + remaining_nodes

    # Construct workflow
    workflow = {
        "workflow": {
            "root": None,
            "solver": "simpleFoam",
            "SolvedFields": "p U k epsilon nut",
            "AuxFields": "",
            "Templates": [],
            "nodeList": node_list,
            "nodes": nodes
        }
    }

    return workflow


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
        print(f"✅ Saved Hermes workflow to: {args.output}")
    else:
        print(json.dumps(workflow, indent=4, ensure_ascii=False, cls=HermesEncoder))


if __name__ == "__main__":
    main()
