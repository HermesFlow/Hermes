# RunOsCommand

Executes system (shell) commands or batch files.

**Type:** `general.RunOsCommand`

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `Method` | enum | `"Commands list"` | Execution method: `"Commands list"` or `"batchFile"` |
| `Command` | string | `""` | Shell command(s) to execute (used with `"Commands list"` method) |
| `batchFile` | string | — | Path to a batch file to execute (used with `"batchFile"` method) |
| `changeDirTo` | string | — | Directory to change to before execution |

## Methods

### Commands List

Executes one or more shell commands sequentially via `os.system()`:

```json
{
    "CreateCase": {
        "Execution": {
            "input_parameters": {
                "Method": "Commands list",
                "Command": "mkdir -p case/0 case/constant case/system"
            }
        },
        "type": "general.RunOsCommand"
    }
}
```

### Batch File

Reads a file, sets it as executable, and runs it:

```json
{
    "RunSetup": {
        "Execution": {
            "input_parameters": {
                "Method": "batchFile",
                "batchFile": "scripts/setup.sh",
                "changeDirTo": "{Parameters.output.targetDirectory}"
            }
        },
        "type": "general.RunOsCommand"
    }
}
```

## Output

| Field | Description |
|-------|-------------|
| `Command` | The command(s) that were executed |
| `returncode` | Exit status of the command(s) |

## Notes

- When `changeDirTo` is specified, the executer changes to that directory before running and restores the original directory after execution.
- Parameter references can be used within the command string: `"Command": "cp {Parameters.output.objectFile} {Parameters.output.targetDirectory}"`
