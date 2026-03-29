# Boundary Conditions

Defines field boundary conditions for OpenFOAM simulation domains using the `changeDictionaryDict` approach.

**Type:** `BC.BoundaryCondition`

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `fields` | object | Per-field boundary condition definitions |

Each field contains patch definitions with:

| Property | Type | Description |
|----------|------|-------------|
| `type` | string | Boundary condition type |
| `value` | varies | Boundary value |

### Common Boundary Condition Types

| Type | Description | Value |
|------|-------------|-------|
| `fixedValue` | Fixed value at boundary | `uniform (Ux Uy Uz)` or `uniform value` |
| `zeroGradient` | Zero normal gradient | — |
| `noSlip` | No-slip wall condition | — |
| `inletOutlet` | Switches between fixed value and zero gradient | `inletValue`, `value` |
| `symmetryPlane` | Symmetry condition | — |
| `empty` | 2D simulation empty direction | — |
| `fixedFluxPressure` | Fixed flux pressure | `value uniform 0` |
| `kqRWallFunction` | Turbulent kinetic energy wall function | `value uniform value` |
| `epsilonWallFunction` | Epsilon wall function | `value uniform value` |
| `nutkWallFunction` | Turbulent viscosity wall function | `value uniform 0` |

## Output

| Field | Description |
|-------|-------------|
| `Result` | The rendered boundary condition dictionary content |

## Example

```json
{
    "BoundaryConditions": {
        "Execution": {
            "input_parameters": {
                "fields": {
                    "U": {
                        "inlet": {
                            "type": "fixedValue",
                            "value": "uniform (10 0 0)"
                        },
                        "outlet": {
                            "type": "zeroGradient"
                        },
                        "walls": {
                            "type": "noSlip"
                        }
                    },
                    "p": {
                        "inlet": {
                            "type": "zeroGradient"
                        },
                        "outlet": {
                            "type": "fixedValue",
                            "value": "uniform 0"
                        },
                        "walls": {
                            "type": "zeroGradient"
                        }
                    },
                    "k": {
                        "inlet": {
                            "type": "fixedValue",
                            "value": "uniform 0.1"
                        },
                        "outlet": {
                            "type": "zeroGradient"
                        },
                        "walls": {
                            "type": "kqRWallFunction",
                            "value": "uniform 0.1"
                        }
                    }
                }
            }
        },
        "type": "BC.BoundaryCondition"
    }
}
```
