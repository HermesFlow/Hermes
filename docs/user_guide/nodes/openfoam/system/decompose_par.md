# DecomposePar

Generates an OpenFOAM `decomposeParDict` file for domain decomposition in parallel simulations.

**Type:** `openFOAM.system.DecomposePar`

## Parameters

The decomposition parameters are configured through the Jinja template with standard OpenFOAM decomposeParDict fields:

| Parameter | Type | Description |
|-----------|------|-------------|
| `numberOfSubdomains` | integer | Number of subdomains for parallel decomposition |
| `method` | string | Decomposition method (e.g., `"scotch"`, `"simple"`, `"hierarchical"`) |

## Output

| Field | Description |
|-------|-------------|
| `Result` | The rendered `decomposeParDict` file content |

## Example

```json
{
    "DecomposePar": {
        "Execution": {
            "input_parameters": {
                "numberOfSubdomains": 4,
                "method": "scotch"
            }
        },
        "type": "openFOAM.system.DecomposePar"
    }
}
```

!!! tip
    The number of subdomains should match the `getNumberOfSubdomains` value in the [BuildAllrun](../constant/build_allrun.md) node for consistent parallel execution.
