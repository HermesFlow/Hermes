# CopyDirectory

Copies an entire directory tree from a source location to a target location.

**Type:** `general.CopyDirectory`

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `Source` | string | Path to the source directory |
| `Target` | string | Path to the target directory |
| `dirs_exist_ok` | boolean | If `true`, allow copying into an existing directory |

## Output

| Field | Description |
|-------|-------------|
| `Source` | The source directory path |
| `Target` | The target directory path |

## Example

```json
{
    "CopyDirectory": {
        "Execution": {
            "input_parameters": {
                "Source": "source",
                "Target": "target",
                "dirs_exist_ok": true
            }
        },
        "type": "general.CopyDirectory"
    }
}
```
