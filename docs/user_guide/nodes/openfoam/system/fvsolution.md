# FvSolution

Generates the OpenFOAM `fvSolution` file that defines linear equation solvers, solver algorithm (SIMPLE/PISO/PIMPLE), and relaxation factors.

**Type:** `openFOAM.system.FvSolution`

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `fields` | object | Per-field linear solver settings |
| `solverProperties` | object | Solution algorithm settings (SIMPLE, PISO, or PIMPLE) |
| `relaxationFactors` | object | Under-relaxation factors for fields and equations |

### Field Solver Settings

Each field defines its linear solver:

| Property | Type | Description |
|----------|------|-------------|
| `solver` | string | Linear solver type (`GAMG`, `PBiCGStab`, `smoothSolver`) |
| `preconditioner` | string | Preconditioner (e.g., `DILU`, `DIC`) |
| `tolerance` | number | Absolute tolerance |
| `relTol` | number | Relative tolerance |
| `smoother` | string | Smoother type (for `smoothSolver` and `GAMG`) |

### Solution Algorithm

| Property | Type | Description |
|----------|------|-------------|
| `type` | string | Algorithm type: `SIMPLE`, `PISO`, or `PIMPLE` |
| `nNonOrthogonalCorrectors` | integer | Non-orthogonal correction steps |
| `nCorrectors` | integer | Pressure correction steps (PISO/PIMPLE) |
| `residualControl` | object | Convergence criteria per field |

## Output

| Field | Description |
|-------|-------------|
| `Result` | The rendered `fvSolution` file content |

## Example

```json
{
    "FvSolution": {
        "Execution": {
            "input_parameters": {
                "fields": {
                    "p": {
                        "solver": "GAMG",
                        "tolerance": 1e-06,
                        "relTol": 0.1,
                        "smoother": "GaussSeidel"
                    },
                    "U": {
                        "solver": "smoothSolver",
                        "smoother": "symGaussSeidel",
                        "tolerance": 1e-05,
                        "relTol": 0.1
                    }
                },
                "solverProperties": {
                    "type": "SIMPLE",
                    "nNonOrthogonalCorrectors": 0,
                    "residualControl": {
                        "p": 1e-04,
                        "U": 1e-04
                    }
                },
                "relaxationFactors": {
                    "fields": {"p": 0.3},
                    "equations": {"U": 0.7, "k": 0.7, "epsilon": 0.7}
                }
            }
        },
        "type": "openFOAM.system.FvSolution"
    }
}
```
