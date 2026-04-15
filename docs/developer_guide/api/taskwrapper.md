# TaskWrapper API

## `hermesTaskWrapper` class

**Module:** `hermes.taskwrapper.wrapper`

The frontend for engine transformation. Holds task metadata, input parameters, and connectivity information.

### Constructor

```python
hermesTaskWrapper(name, taskJSON, Resources_path=None)
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `name` | str | Task/node name |
| `taskJSON` | dict | The node's JSON definition |
| `Resources_path` | str | Path to the Resources directory |

### Properties

| Property | Type | Description |
|----------|------|-------------|
| `name` | str | Task name |
| `typeExecution` | str | Node type identifier |
| `input_parameters` | dict | Resolved input parameters |
| `Properties` | dict | Constant property values |
| `requires` | list | Explicit dependency names |

### Methods

#### `getRequiredTasks(taskJSON)`

Extract the list of required (dependency) task names from the task JSON.

```python
required = wrapper.getRequiredTasks(task_json)
# Returns: ["Node1", "Node2"]
```

Dependencies are extracted from:

- The `requires` field (explicit)
- Parameter references `{NodeName.output.*}` (implicit)

#### `parsePath(parameter)`

Parse a path expression and extract the referenced node name and field.

```python
node_name, field = wrapper.parsePath("{CopyDirectory.output.Source}")
# Returns: ("CopyDirectory", "Source")
```

## Specialized Wrappers

### OpenFOAM Wrappers

Located in `hermes/taskwrapper/specializedwrapper/openFOAMwrapper/`, these provide domain-specific handling for:

- OpenFOAM mesh generation tasks
- Solver execution tasks
- Post-processing tasks

### WrapperHome

**Module:** `hermes.taskwrapper.wrapperHome`

Factory that maps node types to appropriate wrapper classes:

```python
from hermes.taskwrapper.wrapperHome import wrapperHome

wrapper_class = wrapperHome.getWrapper("openFOAM.mesh.BlockMesh")
```
