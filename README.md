# Hermes

[![Documentation](https://img.shields.io/badge/docs-GitHub%20Pages-blue)](https://hermesflow.github.io/Hermes/)

Hermes is a Python framework for building task-based workflow pipelines, with a focus on CFD (Computational Fluid Dynamics) and structural simulation applications.

Workflows are described in JSON format and executed via engines like [Luigi](https://luigi.readthedocs.io/) or [Airflow](https://airflow.apache.org/). The framework also provides a [FreeCAD](https://www.freecad.org/)-based GUI for visual workflow configuration.

**Documentation: [https://hermesflow.github.io/Hermes/](https://hermesflow.github.io/Hermes/)**

## Features

- **JSON-based workflows** — define pipelines as JSON, enabling version control, comparison, and querying
- **Node system** — 40+ built-in node types for general operations and OpenFOAM simulations
- **Template engine** — Jinja2-based file generation for OpenFOAM configuration files
- **FreeCAD integration** — GUI workbench for visual workflow and boundary condition setup
- **Extensible architecture** — create custom nodes and execution engine backends

## Quick Start

```bash
git clone https://github.com/HermesFlow/Hermes.git
cd Hermes
pip install -e .
```

Run a workflow:

```bash
hermes-workflow buildExecute examples/general/copyDir/copyDir.json
```

## Project Structure

```
Hermes/
├── hermes/                        # Main Python package
│   ├── bin/                       # CLI (hermes-workflow)
│   ├── workflow/                  # Core workflow engine
│   ├── taskwrapper/               # Task wrapper abstraction
│   ├── engines/                   # Execution engines (Luigi)
│   ├── Resources/                 # Node types & templates
│   │   ├── general/               # General-purpose nodes
│   │   ├── openFOAM/              # OpenFOAM simulation nodes
│   │   ├── BC/                    # Boundary condition nodes
│   │   └── workbench/             # FreeCAD workbench nodes
│   └── utils/                     # Utilities
├── examples/                      # Workflow examples
├── freecad_source_hermes/         # FreeCAD integration source
├── docs/                          # Documentation source (MkDocs)
└── doc/                           # Legacy Sphinx documentation
```

## Installation

### Standard (CLI only)

```bash
pip install -e .
```

### Docker-based (with FreeCAD GUI)

```bash
chmod +x install.sh
./install.sh -o /path/to/destination
```

See the [Installation Guide](https://hermesflow.github.io/Hermes/user_guide/installation/) for full details and options.

## CLI Usage

```bash
# Build and execute a workflow
hermes-workflow buildExecute workflow.json

# Expand a workflow with default values
hermes-workflow expand workflow.json myCase

# Build Luigi Python file
hermes-workflow build workflow.json myCase

# Execute a built workflow
hermes-workflow execute myCase
```

## Example Workflow

```json
{
    "workflow": {
        "root": null,
        "nodeList": ["CopyDirectory", "RunPythonCode"],
        "nodes": {
            "CopyDirectory": {
                "Execution": {
                    "input_parameters": {
                        "Source": "source",
                        "Target": "target",
                        "dirs_exist_ok": true
                    }
                },
                "type": "general.CopyDirectory"
            },
            "RunPythonCode": {
                "Execution": {
                    "input_parameters": {
                        "ModulePath": "my_module",
                        "ClassName": "MyClass",
                        "MethodName": "process",
                        "Parameters": {
                            "source": "{CopyDirectory.output.Source}",
                            "target": "{CopyDirectory.output.Target}"
                        }
                    }
                },
                "type": "general.RunPythonCode"
            }
        }
    }
}
```

## Documentation

Full documentation is available at **[https://hermesflow.github.io/Hermes/](https://hermesflow.github.io/Hermes/)**, including:

- [User Guide](https://hermesflow.github.io/Hermes/user_guide/) — installation, concepts, tutorials, node reference
- [Developer Guide](https://hermesflow.github.io/Hermes/developer_guide/) — architecture, JSON schema, creating custom nodes, API reference

To serve docs locally:

```bash
./serve_docs.sh
```

## License

See [LICENSE](LICENSE) for details.
