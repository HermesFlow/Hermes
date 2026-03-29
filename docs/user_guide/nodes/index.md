# Node Reference

Nodes are the fundamental building blocks of Hermes workflows. Each node performs a specific task and can receive inputs from and provide outputs to other nodes.

## Node JSON Structure

Every node in a workflow has this basic structure:

```json
{
    "NodeName": {
        "Execution": {
            "input_parameters": {
                "param1": "value1",
                "param2": "value2"
            }
        },
        "type": "category.NodeType",
        "requires": ["OtherNode"]
    }
}
```

| Field | Description |
|-------|-------------|
| `Execution.input_parameters` | Parameters that configure the node's behavior |
| `type` | Node type identifier (e.g., `general.CopyDirectory`) |
| `requires` | Optional explicit dependencies on other nodes |
| `GUI` | Optional FreeCAD GUI configuration |

## Dependencies

Dependencies between nodes are resolved in two ways:

1. **Implicit** — via parameter references like `{NodeName.output.Field}`
2. **Explicit** — via the `requires` field

## Node Categories

### [General Nodes](general/index.md)

Basic file operations, code execution, and template processing.

| Node | Type | Description |
|------|------|-------------|
| [CopyDirectory](general/copy_directory.md) | `general.CopyDirectory` | Copy entire directory trees |
| [CopyFile](general/copy_file.md) | `general.CopyFile` | Copy individual files |
| [RunOsCommand](general/run_os_command.md) | `general.RunOsCommand` | Execute shell commands |
| [RunPythonCode](general/run_python_code.md) | `general.RunPythonCode` | Execute Python code |
| [JinjaTransform](general/jinja_transform.md) | `general.JinjaTransform` | Process Jinja2 templates |
| [FilesWriter](general/files_writer.md) | `general.FilesWriter` | Write files with generated content |
| [Parameters](general/parameters.md) | `general.Parameters` | Define simulation parameters |

### [OpenFOAM Nodes](openfoam/index.md)

Specialized nodes for OpenFOAM CFD simulation setup.

| Category | Nodes | Description |
|----------|-------|-------------|
| [Mesh](openfoam/mesh/blockmesh.md) | BlockMesh, SnappyHexMesh | Mesh generation |
| [System](openfoam/system/controldict.md) | ControlDict, FvSchemes, FvSolution | Solver configuration |
| [Constant](openfoam/constant/transport_properties.md) | Transport, Turbulence, Physical properties | Physical properties |
| [Dispersion](openfoam/dispersion/kinematic_cloud.md) | KinematicCloudProperties | Particle dispersion |
| [BC](openfoam/boundary_conditions.md) | Boundary Conditions | Field boundary conditions |
