# KinematicCloudProperties

Generates the OpenFOAM `kinematicCloudProperties` file for Lagrangian particle tracking simulations.

**Type:** `openFOAM.dispersion.KinematicCloudProperties`

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `solution` | object | Solver settings for the particle cloud |
| `constantProperties` | object | Fixed particle properties |
| `subModels` | object | Sub-model configurations (injection, dispersion, etc.) |
| `injectionModels` | object | Particle injection definitions |
| `dispersionModel` | string | Turbulent dispersion model |
| `patchInteractionModel` | string | Wall interaction model |

## Output

| Field | Description |
|-------|-------------|
| `Result` | The rendered `kinematicCloudProperties` file content |

## Example

```json
{
    "KinematicCloudProperties": {
        "Execution": {
            "input_parameters": {
                "solution": {
                    "active": true,
                    "coupled": true,
                    "transient": true
                },
                "constantProperties": {
                    "rho0": 1000,
                    "youngsModulus": 6e8,
                    "poissonsRatio": 0.35
                },
                "dispersionModel": "stochasticDispersionRAS",
                "patchInteractionModel": "standardWallInteraction"
            }
        },
        "type": "openFOAM.dispersion.KinematicCloudProperties"
    }
}
```
