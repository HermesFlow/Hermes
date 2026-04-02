# Neutral2018Dict

Generates dispersion model parameters for **neutral** atmospheric conditions using the 2018 model formulation.

**Type:** `openFOAM.dispersion.Neutral2018Dict`

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
| `Result` | The rendered dispersion dictionary content |

## Example

```json
{
    "Neutral2018Dict": {
        "Execution": {
            "input_parameters": {
                "C0": 3,
                "g": 9.81,
                "coriolisFactor": 1e-4,
                "zd": 0.1,
                "Qh": 100,
                "T0": 300,
                "stable": false
            }
        },
        "type": "openFOAM.dispersion.Neutral2018Dict"
    }
}
```

!!! note
    See also [Stable2018Dict](stable_2018.md) and [Convective2018Dict](convective_2018.md) for other atmospheric stability conditions.
