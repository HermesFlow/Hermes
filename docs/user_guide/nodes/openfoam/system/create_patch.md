# CreatePatch

Generates an OpenFOAM `createPatchDict` file for creating new boundary patches from existing mesh faces.

**Type:** `openFOAM.system.CreatePatch`

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `patches` | array | `[]` | List of patch definitions to create |

Each patch definition specifies:

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Name of the new patch |
| `patchInfo` | object | Patch type and properties |
| `constructFrom` | string | How to select faces (e.g., `"patches"`, `"set"`) |
| `set` | string | Face set name (when `constructFrom` is `"set"`) |

## Output

| Field | Description |
|-------|-------------|
| `Result` | The rendered `createPatchDict` file content |

## Example

```json
{
    "CreatePatch": {
        "Execution": {
            "input_parameters": {
                "patches": [
                    {
                        "name": "inlet",
                        "patchInfo": {
                            "type": "patch"
                        },
                        "constructFrom": "set",
                        "set": "inletFaces"
                    },
                    {
                        "name": "outlet",
                        "patchInfo": {
                            "type": "patch"
                        },
                        "constructFrom": "set",
                        "set": "outletFaces"
                    }
                ]
            }
        },
        "type": "openFOAM.system.CreatePatch"
    }
}
```
