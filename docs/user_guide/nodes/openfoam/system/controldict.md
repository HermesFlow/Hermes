# ControlDict

Generates the OpenFOAM `controlDict` file that manages simulation execution settings including timing, write control, and solver type.

**Type:** `openFOAM.system.ControlDict`

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `application` | string | Solver name (e.g., `simpleFoam`, `icoFoam`, `pimpleFoam`) |
| `startFrom` | string | Start time control (`startTime`, `firstTime`, `latestTime`) |
| `startTime` | number | Start time value |
| `stopAt` | string | Stop control (`endTime`, `writeNow`, `noWriteNow`, `nextWrite`) |
| `endTime` | number | End time value |
| `deltaT` | number | Time step |
| `writeControl` | string | Write trigger (`timeStep`, `runTime`, `adjustableRunTime`) |
| `writeInterval` | number | Write interval |
| `purgeWrite` | integer | Number of write directories to keep (0 = all) |
| `writeFormat` | string | Output format (`ascii`, `binary`) |
| `writePrecision` | integer | Output decimal precision |
| `writeCompression` | string | Compression (`uncompressed`, `compressed`) |
| `timeFormat` | string | Time directory format (`general`, `fixed`, `scientific`) |
| `timePrecision` | integer | Time format precision |
| `runTimeModifiable` | boolean | Allow runtime modification of settings |

## Output

| Field | Description |
|-------|-------------|
| `Result` | The rendered `controlDict` file content |

## Example

```json
{
    "ControlDict": {
        "Execution": {
            "input_parameters": {
                "application": "simpleFoam",
                "startFrom": "startTime",
                "startTime": 0,
                "stopAt": "endTime",
                "endTime": 1000,
                "deltaT": 1,
                "writeControl": "timeStep",
                "writeInterval": 100,
                "purgeWrite": 0,
                "writeFormat": "ascii",
                "writePrecision": 6,
                "writeCompression": "uncompressed",
                "timeFormat": "general",
                "timePrecision": 6,
                "runTimeModifiable": true
            }
        },
        "type": "openFOAM.system.ControlDict"
    }
}
```
