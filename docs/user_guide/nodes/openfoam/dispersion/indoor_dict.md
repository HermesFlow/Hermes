# IndoorDict

Generates dispersion model parameters for **indoor** environment simulations.

**Type:** `openFOAM.dispersion.IndoorDict`

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `C0` | number | `3` | Kolmogorov constant |
| `g` | number | `9.81` | Gravitational acceleration [m/s²] |
| `coriolisFactor` | number | `1e-4` | Coriolis parameter [1/s] |
| `zd` | number | `0.1` | Displacement height [m] |
| `Qh` | number | `100` | Sensible heat flux [W/m²] |
| `T0` | number | `100` | Reference temperature [K] |
| `stable` | boolean | `true` | Stability flag |

## Output

| Field | Description |
|-------|-------------|
| `Result` | The rendered indoor dispersion dictionary content |

## Example

```json
{
    "IndoorDict": {
        "Execution": {
            "input_parameters": {
                "C0": 3,
                "g": 9.81,
                "coriolisFactor": 1e-4,
                "zd": 0.1,
                "Qh": 100,
                "T0": 300,
                "stable": true
            }
        },
        "type": "openFOAM.dispersion.IndoorDict"
    }
}
```
