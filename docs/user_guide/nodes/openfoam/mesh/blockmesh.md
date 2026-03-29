# BlockMesh

Generates an OpenFOAM `blockMeshDict` file for structured hexahedral mesh generation.

**Type:** `openFOAM.mesh.BlockMesh`

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `vertices` | array | List of 3D vertex coordinates defining the block geometry |
| `blocks` | array | Block definitions with cell counts and grading |
| `boundary` | array | Boundary face definitions with type and face vertices |
| `convertToMeters` | number | Scale factor for vertex coordinates |

### Vertices

Each vertex is a 3-element array `[x, y, z]`:

```json
"vertices": [
    [0, 0, 0],
    [1, 0, 0],
    [1, 1, 0],
    [0, 1, 0],
    [0, 0, 1],
    [1, 0, 1],
    [1, 1, 1],
    [0, 1, 1]
]
```

### Blocks

Each block defines the vertex indices, cell counts, and grading:

```json
"blocks": [
    {
        "vertices": [0, 1, 2, 3, 4, 5, 6, 7],
        "cells": [20, 20, 20],
        "grading": "simpleGrading (1 1 1)"
    }
]
```

### Boundary

Each boundary entry defines the patch name, type, and faces:

```json
"boundary": [
    {
        "name": "inlet",
        "type": "patch",
        "faces": [[0, 4, 7, 3]]
    },
    {
        "name": "outlet",
        "type": "patch",
        "faces": [[1, 2, 6, 5]]
    },
    {
        "name": "walls",
        "type": "wall",
        "faces": [[0, 1, 5, 4], [2, 3, 7, 6], [0, 3, 2, 1], [4, 5, 6, 7]]
    }
]
```

## Output

| Field | Description |
|-------|-------------|
| `Result` | The rendered `blockMeshDict` file content |

## Example

```json
{
    "BlockMesh": {
        "Execution": {
            "input_parameters": {
                "convertToMeters": 1,
                "vertices": [
                    [0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0],
                    [0, 0, 1], [1, 0, 1], [1, 1, 1], [0, 1, 1]
                ],
                "blocks": [
                    {
                        "vertices": [0, 1, 2, 3, 4, 5, 6, 7],
                        "cells": [20, 20, 20],
                        "grading": "simpleGrading (1 1 1)"
                    }
                ],
                "boundary": [
                    {"name": "inlet", "type": "patch", "faces": [[0, 4, 7, 3]]},
                    {"name": "outlet", "type": "patch", "faces": [[1, 2, 6, 5]]},
                    {"name": "walls", "type": "wall", "faces": [[0, 1, 5, 4], [2, 3, 7, 6]]}
                ]
            }
        },
        "type": "openFOAM.mesh.BlockMesh"
    }
}
```
