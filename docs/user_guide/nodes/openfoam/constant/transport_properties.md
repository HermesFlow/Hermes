# TransportProperties

Generates the OpenFOAM `transportProperties` file defining fluid transport properties.

**Type:** `openFOAM.constant.TransportProperties`

!!! note "OpenFOAM Version"
    This node is for OpenFOAM versions 7-10. For newer versions, see [PhysicalProperties](physical_properties.md).

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `transportModel` | string | Transport model type (e.g., `Newtonian`) |
| `nu` | number | Kinematic viscosity [m²/s] |

## Output

| Field | Description |
|-------|-------------|
| `Result` | The rendered `transportProperties` file content |

## Example

```json
{
    "TransportProperties": {
        "Execution": {
            "input_parameters": {
                "transportModel": "Newtonian",
                "nu": 1e-06
            }
        },
        "type": "openFOAM.constant.TransportProperties"
    }
}
```
