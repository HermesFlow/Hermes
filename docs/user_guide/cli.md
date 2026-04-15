# CLI Reference

The `hermes-workflow` command-line tool provides commands for expanding, building, and executing Hermes workflows.

## Commands

### `expand`

Expand a workflow JSON file with default values from node templates.

```bash
hermes-workflow expand <workflow_file> <case_name>
```

| Argument | Description |
|----------|-------------|
| `workflow_file` | Path to the workflow JSON file |
| `case_name` | Name for the expanded case |

This reads the workflow JSON, resolves all template references, and writes an expanded version with all default values filled in.

### `build`

Generate a Python execution file (Luigi tasks) from a workflow.

```bash
hermes-workflow build <workflow_file> <case_name> [--parameters <params_file>]
```

| Argument | Description |
|----------|-------------|
| `workflow_file` | Path to the workflow JSON file |
| `case_name` | Name for the build output |
| `--parameters` | Optional parameters override file |

### `execute`

Run a previously built workflow.

```bash
hermes-workflow execute <case_name> [--force] [--overwrite]
```

| Argument | Description |
|----------|-------------|
| `case_name` | Name of the case to execute |
| `--force` | Force re-execution of all tasks |
| `--overwrite` | Overwrite existing outputs |

### `buildExecute`

Combined command: expand, build, and execute in one step.

```bash
hermes-workflow buildExecute <workflow_file> [--force] [--overwrite]
```

| Argument | Description |
|----------|-------------|
| `workflow_file` | Path to the workflow JSON file |
| `--force` | Force re-execution |
| `--overwrite` | Overwrite existing outputs |

This is the most common command for running workflows end-to-end.

## Logging

Hermes uses a configurable logging system with handlers for different verbosity levels:

- `console` — standard output
- Levels from `DEBUG` to `CRITICAL`

Specialized loggers are available for:

- `hermes.bin` — CLI operations
- `hermes.workflow` — workflow processing
- `hermes.engines` — engine-specific operations

The logging configuration is stored in `hermes/hermesLogging/hermesLogging.config`.

## Examples

```bash
# Build and run a simple workflow
hermes-workflow buildExecute examples/general/copyDir/copyDir.json

# Expand a workflow to see all resolved parameters
hermes-workflow expand examples/openFOAM/simpleFoam/simpleFoam.json myCase

# Build with parameter overrides
hermes-workflow build workflow.json myCase --parameters params.json

# Force re-execution
hermes-workflow execute myCase --force
```
