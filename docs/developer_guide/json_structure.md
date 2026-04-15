# JSON Structure

This document describes the complete JSON schema used by Hermes workflows.

## Workflow JSON

The top-level structure of a Hermes workflow:

```json
{
    "workflow": {
        "root": "FinalNodeName",
        "nodeList": ["Node1", "Node2", "Node3"],
        "solver": "simpleFoam",
        "Templates": {},
        "nodes": {
            "Node1": { ... },
            "Node2": { ... },
            "Node3": { ... }
        }
    }
}
```

### Top-Level Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `workflow` | object | Yes | Container for the workflow definition |
| `workflow.root` | string/null | No | Name of the root (final) node. If `null`, auto-detected |
| `workflow.nodeList` | array | Yes | Ordered list of node names |
| `workflow.nodes` | object | Yes | Node definitions keyed by name |
| `workflow.solver` | string | No | Solver name (for OpenFOAM workflows) |
| `workflow.Templates` | object | No | Shared template definitions |

## Node JSON

Each node in the `nodes` object has this structure:

```json
{
    "NodeName": {
        "type": "category.NodeType",
        "Execution": {
            "input_parameters": {
                "param1": "value1",
                "param2": "value2"
            }
        },
        "GUI": {
            "Schema": { ... },
            "uiSchema": { ... },
            "formData": { ... }
        },
        "requires": ["OtherNode"]
    }
}
```

### Node Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `type` | string | Yes | Node type identifier |
| `Execution` | object | Yes | Execution configuration |
| `Execution.input_parameters` | object | Yes | Parameters for the node |
| `GUI` | object | No | FreeCAD GUI configuration |
| `requires` | array | No | Explicit dependencies |
| `Template` | string | No | Template reference (alternative to full definition) |

### Template References

Instead of a full definition, a node can reference a template:

```json
{
    "BlockMesh": {
        "Template": "openFOAM.mesh.BlockMesh.jsonForm"
    }
}
```

The template path maps to a file in `hermes/Resources/`:
`openFOAM.mesh.BlockMesh.jsonForm` → `hermes/Resources/openFOAM/mesh/BlockMesh/jsonForm.json`

## GUI Configuration (react-jsonschema-form)

The GUI section follows the [react-jsonschema-form](https://react-jsonschema-form.readthedocs.io/) specification:

### Schema

JSON Schema defining the form fields:

```json
{
    "Schema": {
        "type": "object",
        "properties": {
            "velocity": {
                "type": "number",
                "title": "Inlet Velocity",
                "default": 10.0
            },
            "viscosity": {
                "type": "number",
                "title": "Kinematic Viscosity",
                "default": 1e-06
            }
        }
    }
}
```

### uiSchema

Controls how form fields are rendered:

```json
{
    "uiSchema": {
        "velocity": {
            "ui:widget": "updown"
        },
        "viscosity": {
            "ui:widget": "text"
        }
    }
}
```

### formData

Default values for the form:

```json
{
    "formData": {
        "velocity": 10.0,
        "viscosity": 1e-06
    }
}
```

## Parameter References

Parameters can reference outputs from other nodes:

| Pattern | Description |
|---------|-------------|
| `{NodeName.output.Field}` | Reference a specific output field |
| `{NodeName.output}` | Reference the entire output object |
| `{workflow.field}` | Reference a workflow-level field |

### Special Syntax

| Syntax | Description |
|--------|-------------|
| `{}` | Empty parameter (interpreted as empty object) |
| `#{expression}` | OpenFOAM `#calc` expression (preserved in output) |

## Complete Example

```json
{
    "workflow": {
        "root": null,
        "nodeList": [
            "Parameters",
            "CopyDirectory",
            "BlockMesh",
            "ControlDict",
            "FilesWriter"
        ],
        "nodes": {
            "Parameters": {
                "type": "general.Parameters",
                "Execution": {
                    "input_parameters": {
                        "OFversion": "10",
                        "targetDirectory": "myCase"
                    }
                }
            },
            "CopyDirectory": {
                "type": "general.CopyDirectory",
                "Execution": {
                    "input_parameters": {
                        "Source": "templateCase",
                        "Target": "{Parameters.output.targetDirectory}"
                    }
                }
            },
            "BlockMesh": {
                "Template": "openFOAM.mesh.BlockMesh.jsonForm"
            },
            "ControlDict": {
                "Template": "openFOAM.system.ControlDict.jsonForm"
            },
            "FilesWriter": {
                "type": "general.FilesWriter",
                "Execution": {
                    "input_parameters": {
                        "Files": [
                            {
                                "Path": "{Parameters.output.targetDirectory}/system/blockMeshDict",
                                "Content": "{BlockMesh.output.Result}"
                            },
                            {
                                "Path": "{Parameters.output.targetDirectory}/system/controlDict",
                                "Content": "{ControlDict.output.Result}"
                            }
                        ]
                    }
                },
                "requires": ["CopyDirectory"]
            }
        }
    }
}
```
