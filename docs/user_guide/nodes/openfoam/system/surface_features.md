# SurfaceFeatures

Generates an OpenFOAM `surfaceFeaturesDict` (or `surfaceFeatureExtractDict` depending on version) for extracting surface features used in mesh generation.

**Type:** `openFOAM.system.SurfaceFeatures`

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `OFversion` | string | `"of10"` | OpenFOAM version identifier (affects dictionary format) |

## Output

| Field | Description |
|-------|-------------|
| `Result` | The rendered surface features dictionary file content |

## Example

```json
{
    "SurfaceFeatures": {
        "Execution": {
            "input_parameters": {
                "OFversion": "of10"
            }
        },
        "type": "openFOAM.system.SurfaceFeatures"
    }
}
```

!!! note
    The dictionary name changed between OpenFOAM versions — earlier versions use `surfaceFeatureExtractDict` while newer versions use `surfaceFeaturesDict`. The `OFversion` parameter controls which format is generated.
