# TopoSetDict

Generates an OpenFOAM `topoSetDict` file for defining topology sets — cell zones, face zones, and point sets used for mesh manipulation and post-processing.

**Type:** `openFOAM.system.TopoSetDict`

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `actions` | array | `[]` | List of topoSet actions to perform |

Each action defines:

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Name of the set |
| `type` | string | Set type (`cellSet`, `faceSet`, `pointSet`, `cellZoneSet`, `faceZoneSet`) |
| `action` | string | Action to perform (`new`, `add`, `delete`, `subset`, `invert`) |
| `source` | string | Source type (e.g., `boxToCell`, `sphereToCell`, `surfaceToCell`) |
| `sourceInfo` | object | Parameters for the source |

## Output

| Field | Description |
|-------|-------------|
| `Result` | The rendered `topoSetDict` file content |

## Example

```json
{
    "TopoSetDict": {
        "Execution": {
            "input_parameters": {
                "actions": [
                    {
                        "name": "refinementRegion",
                        "type": "cellSet",
                        "action": "new",
                        "source": "boxToCell",
                        "sourceInfo": {
                            "box": "(0 0 0) (1 1 0.5)"
                        }
                    },
                    {
                        "name": "refinementZone",
                        "type": "cellZoneSet",
                        "action": "new",
                        "source": "setToCellZone",
                        "sourceInfo": {
                            "set": "refinementRegion"
                        }
                    }
                ]
            }
        },
        "type": "openFOAM.system.TopoSetDict"
    }
}
```
