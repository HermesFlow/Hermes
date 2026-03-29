# Workflow API

## `workflow` class

**Module:** `hermes.workflow.workflow`

The central class that loads JSON workflow definitions and builds executable task networks.

### Constructor

```python
workflow(workflowJSON, WD_path=None, Resources_path=None, name=None)
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `workflowJSON` | dict | The workflow JSON definition |
| `WD_path` | str | Working directory path |
| `Resources_path` | str | Path to the Resources directory |
| `name` | str | Optional workflow name |

### Properties

| Property | Type | Description |
|----------|------|-------------|
| `json` | dict | Full workflow JSON with GUI and final nodes |
| `workflowJSON` | dict | The `workflow` section only |
| `nodeList` | list | Ordered list of node names |
| `nodes` | dict | Node definitions dictionary |
| `parametersJSON` | dict | Extracted parameters only |
| `taskRepresentations` | dict | Map of node names to `TaskWrapper` lists |
| `solver` | str | Solver configuration |

### Methods

#### `build(buildername)`

Build execution code for the specified engine.

```python
wf.build("luigi")
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `buildername` | str | Engine name (e.g., `"luigi"`) |

#### `write(workflowName, directory, fullJSON=False)`

Persist the workflow to a JSON file.

```python
wf.write("my_workflow", "/output", fullJSON=True)
```

#### `updateNodes(parameters)`

Update node parameters from a dictionary.

```python
wf.updateNodes({"Parameters": {"OFversion": "10"}})
```

#### `getRootTaskName()`

Returns the name of the root (final) task in the workflow.

#### Dictionary Access

The workflow supports dictionary-like access to nodes:

```python
node = wf["NodeName"]          # Get node
wf["NewNode"] = node_def       # Set node
del wf["OldNode"]              # Delete node
for name in wf.keys():         # Iterate names
    ...
```

---

## `hermesNode` class

**Module:** `hermes.workflow.workflow`

Provides a convenient interface to individual node JSON definitions.

### Constructor

```python
hermesNode(name, nodeJSON)
```

### Properties

| Property | Type | Description |
|----------|------|-------------|
| `name` | str | Node name |
| `parameters` | dict | Node input parameters |
| `executionJSON` | dict | Execution configuration only |
| `parametersTable` | DataFrame | Pandas-formatted parameters table |

### Methods

#### Dictionary Access

```python
value = node["paramName"]      # Get parameter
node["paramName"] = value      # Set parameter
for key in node.keys():        # Iterate parameter names
    ...
```
