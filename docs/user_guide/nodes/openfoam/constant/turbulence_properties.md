# TurbulenceProperties

Generates the OpenFOAM `turbulenceProperties` file for turbulence model configuration.

**Type:** `openFOAM.constant.TurbulenceProperties`

!!! note "OpenFOAM Version"
    This node is for OpenFOAM versions 7-10. For newer versions, see [MomentumTransport](momentum_transport.md).

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
| `Result` | The rendered `turbulenceProperties` file content |

## Example

```json
{
    "TurbulenceProperties": {
        "Execution": {
            "input_parameters": {
                "simulationType": "RAS",
                "model": "kEpsilon"
            }
        },
        "type": "openFOAM.constant.TurbulenceProperties"
    }
}
```
