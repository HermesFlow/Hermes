# FvSchemes

Generates the OpenFOAM `fvSchemes` file that defines numerical discretization schemes for the finite volume method.

**Type:** `openFOAM.system.FvSchemes`

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `ddtSchemes` | object | Time derivative schemes |
| `gradSchemes` | object | Gradient schemes |
| `divSchemes` | object | Divergence schemes |
| `laplacianSchemes` | object | Laplacian schemes |
| `interpolationSchemes` | object | Interpolation schemes |
| `snGradSchemes` | object | Surface-normal gradient schemes |

### Common Scheme Values

| Scheme Type | Options |
|-------------|---------|
| `ddtSchemes` | `steadyState`, `Euler`, `backward`, `CrankNicolson` |
| `gradSchemes` | `Gauss linear`, `leastSquares`, `cellLimited Gauss linear` |
| `divSchemes` | `Gauss linear`, `Gauss upwind`, `Gauss linearUpwind grad(U)` |
| `laplacianSchemes` | `Gauss linear corrected`, `Gauss linear uncorrected` |
| `interpolationSchemes` | `linear`, `midPoint` |
| `snGradSchemes` | `corrected`, `uncorrected`, `limited corrected` |

## Output

| Field | Description |
|-------|-------------|
| `Result` | The rendered `fvSchemes` file content |

## Example

```json
{
    "FvSchemes": {
        "Execution": {
            "input_parameters": {
                "ddtSchemes": {
                    "default": "steadyState"
                },
                "gradSchemes": {
                    "default": "Gauss linear",
                    "grad(p)": "Gauss linear",
                    "grad(U)": "cellLimited Gauss linear 1"
                },
                "divSchemes": {
                    "default": "none",
                    "div(phi,U)": "bounded Gauss linearUpwind grad(U)",
                    "div(phi,k)": "bounded Gauss upwind",
                    "div(phi,epsilon)": "bounded Gauss upwind",
                    "div((nuEff*dev2(T(grad(U)))))": "Gauss linear"
                },
                "laplacianSchemes": {
                    "default": "Gauss linear corrected"
                },
                "interpolationSchemes": {
                    "default": "linear"
                },
                "snGradSchemes": {
                    "default": "corrected"
                }
            }
        },
        "type": "openFOAM.system.FvSchemes"
    }
}
```
