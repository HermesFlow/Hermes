# SnappyHexMesh

Generates an OpenFOAM `snappyHexMeshDict` file for automated mesh generation with castellated mesh, surface snapping, and boundary layer addition.

**Type:** `openFOAM.mesh.SnappyHexMesh`

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `castellatedMesh` | boolean | Enable castellated mesh step |
| `snap` | boolean | Enable surface snapping step |
| `addLayers` | boolean | Enable boundary layer addition |
| `castellatedMeshControls` | object | Controls for the castellated mesh step |
| `snapControls` | object | Controls for the snapping step |
| `addLayersControls` | object | Controls for boundary layer addition |
| `meshQualityControls` | object | Mesh quality criteria |

### Castellated Mesh Controls

| Field | Type | Description |
|-------|------|-------------|
| `maxLocalCells` | integer | Max cells per processor during refinement |
| `maxGlobalCells` | integer | Max total cells |
| `minRefinementCells` | integer | Min cells to refine |
| `nCellsBetweenLevels` | integer | Buffer layers between refinement levels |
| `refinementSurfaces` | object | Surface refinement settings |
| `refinementRegions` | object | Volume refinement regions |
| `locationInMesh` | array | Point `[x, y, z]` inside the mesh domain |

### Snap Controls

| Field | Type | Description |
|-------|------|-------------|
| `nSmoothPatch` | integer | Smoothing iterations |
| `tolerance` | number | Snapping distance tolerance |
| `nSolveIter` | integer | Mesh displacement solver iterations |
| `nRelaxIter` | integer | Snapping relaxation iterations |

### Add Layers Controls

| Field | Type | Description |
|-------|------|-------------|
| `layers` | object | Per-patch layer settings |
| `relativeSizes` | boolean | Use relative layer sizes |
| `expansionRatio` | number | Layer expansion ratio |
| `finalLayerThickness` | number | Thickness of the final layer |
| `minThickness` | number | Minimum layer thickness |

## Output

| Field | Description |
|-------|-------------|
| `Result` | The rendered `snappyHexMeshDict` file content |

## Example

```json
{
    "SnappyHexMesh": {
        "Execution": {
            "input_parameters": {
                "castellatedMesh": true,
                "snap": true,
                "addLayers": true,
                "castellatedMeshControls": {
                    "maxLocalCells": 100000,
                    "maxGlobalCells": 2000000,
                    "minRefinementCells": 10,
                    "nCellsBetweenLevels": 3,
                    "locationInMesh": [0.5, 0.5, 0.5]
                },
                "snapControls": {
                    "nSmoothPatch": 3,
                    "tolerance": 2.0,
                    "nSolveIter": 30,
                    "nRelaxIter": 5
                },
                "meshQualityControls": {
                    "maxNonOrtho": 65,
                    "maxBoundarySkewness": 20
                }
            }
        },
        "type": "openFOAM.mesh.SnappyHexMesh"
    }
}
```
