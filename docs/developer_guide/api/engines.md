# Engines API

## Luigi Engine

### `LuigiBuilder` class

**Module:** `hermes.engines.luigi.builder`

Converts the TaskWrapper network into executable Luigi Python code.

#### Constructor

```python
LuigiBuilder(workflow)
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `workflow` | workflow | The workflow instance |

#### Methods

##### `build()`

Generates the complete Luigi Python file:

1. Writes import statements and utilities
2. Iterates through task representations
3. For each task wrapper, locates the appropriate transformer
4. Generates a Luigi Task class

The generated code includes:

- `hermesLuigiTask` base class
- Per-node Task classes with `requires()`, `output()`, and `run()` methods
- Parameter mapping and executer invocation
- JSON output writing

### `pythonClassBase` class

**Module:** `hermes.engines.luigi.pythonClassBase`

Base class for node-specific code transformers. Override this to customize how a node type is translated to Luigi code.

#### Methods

##### `transform(taskWrapper)`

Generate Luigi task class code for the given task wrapper.

```python
class MyTransformer(pythonClassBase):
    def transform(self, taskWrapper):
        code = self.generate_class_header(taskWrapper)
        code += self.generate_requires(taskWrapper)
        code += self.generate_output(taskWrapper)
        code += self.generate_run(taskWrapper)
        return code
```

### `taskUtils` module

**Module:** `hermes.engines.luigi.taskUtils`

Utility functions used in generated Luigi task code:

| Function | Description |
|----------|-------------|
| `map_parameters(inputs, parameter_map)` | Map dependency outputs to task parameters |
| `resolve_path(path, inputs)` | Resolve a `{Node.output.Field}` path expression |
| `write_output(target, data)` | Write task output as JSON |

## Generated Task Structure

Each generated Luigi task follows this pattern:

```python
import luigi
from hermes.engines.luigi.taskUtils import hermesLuigiTask

class MyNode(hermesLuigiTask):
    """Auto-generated from Hermes workflow."""

    def requires(self):
        return [DependencyNode()]

    def output(self):
        return luigi.LocalTarget("MyNode_output.json")

    def run(self):
        # Load dependency outputs
        dep_data = self.load_inputs()

        # Map parameters
        params = {
            "Source": dep_data["Dependency"]["Source"],
            "Target": "output_dir"
        }

        # Run the executer
        from hermes.Resources.general.CopyDirectory.executer import executer
        result = executer.run(params)

        # Write output
        with self.output().open('w') as f:
            json.dump(result, f)
```
