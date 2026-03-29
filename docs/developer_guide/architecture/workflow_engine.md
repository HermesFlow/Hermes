# Workflow Engine

The workflow engine is the core of Hermes, responsible for loading JSON definitions, building dependency graphs, and orchestrating code generation.

## Loading a Workflow

The `workflow` class accepts a JSON definition and optional paths:

```python
from hermes.workflow.workflow import workflow

wf = workflow(
    workflowJSON=json_data,
    WD_path="/path/to/working/directory",
    Resources_path="/path/to/hermes/Resources",
    name="my_workflow"
)
```

## Network Building

The `_buildNetwork()` method processes each node in the `nodeList`:

1. **Template resolution** — if a node has a `Template` field, loads the template from `Resources/`
2. **Parameter extraction** — reads `Execution.input_parameters`
3. **Dependency detection** — scans parameters for `{NodeName.output.*}` references
4. **TaskWrapper creation** — creates a `hermesTaskWrapper` for each node
5. **Graph assembly** — connects wrappers based on dependencies

### Cross-Product Expansion

When a node has parameterized inputs that produce multiple combinations, the engine generates cross-product task representations. Each combination becomes a separate task in the execution graph.

## Parameter Path Resolution

Parameter paths follow the format `{NodeName.output.FieldName}`:

- `{CopyDirectory.output.Source}` — references the `Source` output of `CopyDirectory`
- `{Parameters.output.OFversion}` — references the `OFversion` output of `Parameters`
- `{workflow.field}` — references a workflow-level field

The `parsePath()` method in `hermesTaskWrapper` handles path parsing and dependency extraction.

## Building Execution Code

The `build()` method delegates to a named engine builder:

```python
wf.build("luigi")  # Generates Luigi Python code
```

The builder receives the complete task network and generates engine-specific executable code.

## Writing Workflows

The `write()` method persists the workflow back to JSON:

```python
wf.write(workflowName="my_workflow", directory="/output", fullJSON=True)
```

With `fullJSON=True`, the output includes GUI configuration and resolved templates.

## Updating Parameters

The `updateNodes()` method applies parameter overrides:

```python
wf.updateNodes({"Parameters": {"OFversion": "10", "targetDirectory": "newCase"}})
```

This is used by the `--parameters` CLI flag to override values at build time.

## Workflow Expansion

The `expandWorkflow` module (`hermes/workflow/expandWorkflow.py`) handles template expansion — replacing `Template` references with fully resolved node definitions including all default values.

## Reverse Engineering

The `reverse` module (`hermes/workflow/reverse.py`) provides tools to reconstruct a Hermes workflow JSON from existing OpenFOAM case files. This is useful for importing existing simulations into the Hermes framework.
