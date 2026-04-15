# CopyFile

Copies a single file from a source path to a target path.

**Type:** `general.CopyFile`

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `Source` | string | Path to the source file |
| `Target` | string | Path to the target file |

## Output

| Field | Description |
|-------|-------------|
| `Source` | The source file path |
| `Target` | The target file path |

## Example

```json
{
    "CopyFile": {
        "Execution": {
            "input_parameters": {
                "Source": "input/mesh.stl",
                "Target": "case/constant/triSurface/mesh.stl"
            }
        },
        "type": "general.CopyFile"
    }
}
```
