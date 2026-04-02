# FvConstraints

Generates an OpenFOAM `fvConstraints` (or `fvOptions`) file for applying field constraints during the simulation.

**Type:** `openFOAM.system.FvConstraints`

## Parameters

Constraints are defined as objects following the OpenFOAM fvConstraints format. The specific parameters depend on the type of constraint applied.

## Output

| Field | Description |
|-------|-------------|
| `Result` | The rendered `fvConstraints` file content |

## Example

```json
{
    "FvConstraints": {
        "Execution": {
            "input_parameters": {
                "limitT": {
                    "type": "limitTemperature",
                    "active": true,
                    "selectionMode": "all",
                    "min": 273,
                    "max": 373
                }
            }
        },
        "type": "openFOAM.system.FvConstraints"
    }
}
```

!!! note
    The available constraint types and their parameters depend on the OpenFOAM version and installed modules.
