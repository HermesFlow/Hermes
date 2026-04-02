# BuildAllrun

Generates the `Allrun` and `Allclean` shell scripts used to execute and clean up OpenFOAM simulation cases.

**Type:** `openFOAM.BuildAllrun`

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `casePath` | string | `"pathToCase"` | Path to the OpenFOAM case directory |
| `caseExecution` | object | — | Execution configuration (see below) |

### caseExecution

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `parallelCase` | boolean | `true` | Enable parallel execution |
| `slurm` | boolean | `false` | Use SLURM job scheduler |
| `getNumberOfSubdomains` | integer | `10` | Number of subdomains for parallel decomposition |
| `runFile` | array | `[]` | Ordered list of execution steps |

### runFile Entry

Each entry in the `runFile` array defines one execution step:

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Command or application name (e.g., `"blockMesh"`, `"simpleFoam"`) |
| `couldRunInParallel` | boolean | Whether this step supports parallel execution |
| `parameters` | string | Additional command-line parameters |
| `foamJob` | boolean | Run via OpenFOAM's `foamJob` wrapper |
| `screen` | boolean | Display output on screen |
| `wait` | boolean | Wait for completion before next step |
| `slurm` | boolean | Submit as a SLURM job |

## Output

| Field | Description |
|-------|-------------|
| `casePath` | Path to the case directory |
| `Allrun` | Content of the generated Allrun script |
| `Allclean` | Content of the generated Allclean script |

## Example

```json
{
    "BuildAllrun": {
        "Execution": {
            "input_parameters": {
                "casePath": "{Parameters.output.targetDirectory}",
                "caseExecution": {
                    "parallelCase": true,
                    "slurm": false,
                    "getNumberOfSubdomains": 4,
                    "runFile": [
                        {
                            "name": "blockMesh",
                            "couldRunInParallel": false,
                            "parameters": "",
                            "foamJob": false,
                            "screen": true,
                            "wait": true,
                            "slurm": false
                        },
                        {
                            "name": "snappyHexMesh",
                            "couldRunInParallel": true,
                            "parameters": "-overwrite",
                            "foamJob": false,
                            "screen": true,
                            "wait": true,
                            "slurm": false
                        },
                        {
                            "name": "simpleFoam",
                            "couldRunInParallel": true,
                            "parameters": "",
                            "foamJob": true,
                            "screen": false,
                            "wait": true,
                            "slurm": false
                        }
                    ]
                }
            }
        },
        "type": "openFOAM.BuildAllrun"
    }
}
```

The generated `Allrun` script handles:

- Sequential execution of commands in the `runFile` order
- Parallel decomposition with `decomposePar` when `parallelCase` is enabled
- MPI execution with `mpirun -np <subdomains>` for parallel-capable steps
- `foamJob` wrapping for long-running solvers
- The `Allclean` script restores `0.orig` to `0` and cleans processor directories
