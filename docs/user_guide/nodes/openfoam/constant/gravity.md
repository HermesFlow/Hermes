# Gravity (g)

Generates the OpenFOAM `g` file that defines the gravitational acceleration vector.

**Type:** `openFOAM.constant.g`

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `x` | number | `0` | Gravitational acceleration in x direction [m/s²] |
| `y` | number | `0` | Gravitational acceleration in y direction [m/s²] |
| `z` | number | `-9.8` | Gravitational acceleration in z direction [m/s²] |

## Output

| Field | Description |
|-------|-------------|
| `Result` | The rendered `g` file content |

## Example

```json
{
    "Gravity": {
        "Execution": {
            "input_parameters": {
                "x": 0,
                "y": 0,
                "z": -9.81
            }
        },
        "type": "openFOAM.constant.g"
    }
}
```

!!! note
    Required for buoyancy-driven simulations (e.g., Boussinesq approximation) and Lagrangian particle tracking.
