# MeshQualityDict

Generates an OpenFOAM `meshQualityDict` file that defines mesh quality criteria used by mesh generation tools like snappyHexMesh.

**Type:** `openFOAM.system.MeshQualityDict`

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `maxNonOrtho` | number | `65` | Maximum non-orthogonality angle (degrees) |
| `maxBoundarySkewness` | number | `20` | Maximum boundary face skewness |
| `minVol` | number | `1e-13` | Minimum cell volume |

## Output

| Field | Description |
|-------|-------------|
| `Result` | The rendered `meshQualityDict` file content |

## Example

```json
{
    "MeshQualityDict": {
        "Execution": {
            "input_parameters": {
                "maxNonOrtho": 65,
                "maxBoundarySkewness": 20,
                "minVol": 1e-13
            }
        },
        "type": "openFOAM.system.MeshQualityDict"
    }
}
```

!!! tip
    This node is typically used alongside [SnappyHexMesh](../mesh/snappyhexmesh.md) to control mesh quality during automatic mesh generation.
