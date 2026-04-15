# PhysicalProperties

Generates the OpenFOAM `physicalProperties` file defining transport properties including optional thermal parameters.

**Type:** `openFOAM.constant.PhysicalProperties`

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `transportModel` | string | Transport model type (e.g., `Newtonian`) |
| `nu` | number | Kinematic viscosity [m²/s] |
| `beta` | number | (Optional) Thermal expansion coefficient [1/K] |
| `TRef` | number | (Optional) Reference temperature [K] |
| `Pr` | number | (Optional) Prandtl number |
| `Prt` | number | (Optional) Turbulent Prandtl number |

## Output

| Field | Description |
|-------|-------------|
| `Result` | The rendered `physicalProperties` file content |

## Example

```json
{
    "PhysicalProperties": {
        "Execution": {
            "input_parameters": {
                "transportModel": "Newtonian",
                "nu": 1.5e-05,
                "beta": 3e-03,
                "TRef": 300,
                "Pr": 0.9,
                "Prt": 0.7
            }
        },
        "type": "openFOAM.constant.PhysicalProperties"
    }
}
```
