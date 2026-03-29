# BuildAllrun

Generates the `allRun` and `allClean` shell scripts used to execute and clean up OpenFOAM simulation cases.

**Type:** `openFOAM.constant.BuildAllrun`

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `commands` | array | List of OpenFOAM commands to include in the allRun script |
| `parallel` | boolean | Whether to set up parallel execution |
| `decomposeProcessors` | integer | Number of processors for parallel runs |

## Output

| Field | Description |
|-------|-------------|
| `allRun` | Content of the `allRun` script |
| `allClean` | Content of the `allClean` script |

## Example

```json
{
    "BuildAllrun": {
        "Execution": {
            "input_parameters": {
                "commands": [
                    "blockMesh",
                    "snappyHexMesh -overwrite",
                    "simpleFoam"
                ],
                "parallel": true,
                "decomposeProcessors": 4
            }
        },
        "type": "openFOAM.constant.BuildAllrun"
    }
}
```

The generated `allRun` script handles:

- Sequential command execution
- Parallel decomposition with `decomposePar`
- MPI execution with `mpirun`
- Reconstruction with `reconstructPar`
