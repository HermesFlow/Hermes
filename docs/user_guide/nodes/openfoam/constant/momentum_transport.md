# MomentumTransport

Generates the OpenFOAM `momentumTransport` file for turbulence modeling configuration.

**Type:** `openFOAM.constant.MomentumTransport`

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `simulationType` | string | Simulation type: `RAS`, `LES`, or `laminar` |
| `model` | string | Turbulence model name |

### Common Models

| Simulation Type | Models |
|----------------|--------|
| `RAS` | `kEpsilon`, `kOmega`, `kOmegaSST`, `realizableKE`, `SpalartAllmaras` |
| `LES` | `Smagorinsky`, `kEqn`, `dynamicKEqn`, `WALE` |
| `laminar` | (none) |

## Output

| Field | Description |
|-------|-------------|
| `Result` | The rendered `momentumTransport` file content |

## Example

```json
{
    "MomentumTransport": {
        "Execution": {
            "input_parameters": {
                "simulationType": "RAS",
                "model": "kEpsilon"
            }
        },
        "type": "openFOAM.constant.MomentumTransport"
    }
}
```
