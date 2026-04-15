# Parameters

Defines general simulation parameters that can be referenced by other nodes. Commonly used to set OpenFOAM version, target directories, and shared configuration values.

**Type:** `general.Parameters`

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `OFversion` | string | OpenFOAM version (e.g., `"10"`) |
| `targetDirectory` | string | Target directory for the simulation case |
| `objectFile` | string | Geometry file path |
| `decomposeProcessors` | integer | Number of processors for parallel decomposition |
| *(custom)* | any | Additional user-defined parameters |

## Output

All input parameters are passed through as outputs, available for reference by other nodes.

## Example

```json
{
    "Parameters": {
        "Execution": {
            "input_parameters": {
                "OFversion": "10",
                "targetDirectory": "myCase",
                "objectFile": "building.stl",
                "decomposeProcessors": 4
            }
        },
        "type": "general.Parameters"
    }
}
```

Other nodes can reference these values:

```json
"Command": "cp {Parameters.output.objectFile} {Parameters.output.targetDirectory}/constant/triSurface/"
```
