# FilesWriter

Creates files with content assembled from node outputs. Useful for writing generated configuration files to disk.

**Type:** `general.FilesWriter`

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `Files` | array | List of file definitions, each with `Path` and `Content` |

Each file definition:

| Field | Type | Description |
|-------|------|-------------|
| `Path` | string | Output file path |
| `Content` | string | File content (can reference other node outputs) |

## Output

| Field | Description |
|-------|-------------|
| `Files` | List of files that were written |

## Example

```json
{
    "FilesWriter": {
        "Execution": {
            "input_parameters": {
                "Files": [
                    {
                        "Path": "case/system/controlDict",
                        "Content": "{ControlDict.output.Result}"
                    },
                    {
                        "Path": "case/system/fvSchemes",
                        "Content": "{FvSchemes.output.Result}"
                    }
                ]
            }
        },
        "type": "general.FilesWriter"
    }
}
```
