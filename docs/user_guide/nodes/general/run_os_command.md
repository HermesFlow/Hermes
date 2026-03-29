# RunOsCommand

Executes a system (shell) command.

**Type:** `general.RunOsCommand`

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `Command` | string | The shell command to execute |

## Output

| Field | Description |
|-------|-------------|
| `Command` | The command that was executed |
| `returncode` | Exit code of the command |

## Example

```json
{
    "CreateEmptyCase": {
        "Execution": {
            "input_parameters": {
                "Command": "mkdir -p case/0 case/constant case/system"
            }
        },
        "type": "general.RunOsCommand"
    }
}
```

!!! note
    Parameter references can be used within the command string: `"Command": "cp {Parameters.output.objectFile} {Parameters.output.targetDirectory}"`
