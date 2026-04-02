# GeometryDefiner

Provides a FreeCAD workbench interface for defining simulation geometry entities used in mesh generation.

**Type:** `openFOAM.mesh.GeometryDefiner`

## Overview

GeometryDefiner is primarily a GUI node that integrates with the FreeCAD workbench. It allows users to define geometry objects (STL surfaces, bounding boxes, refinement regions) that are referenced by mesh generation nodes like [SnappyHexMesh](snappyhexmesh.md).

## Parameters

Geometry parameters are defined through the FreeCAD workbench interface.

## Output

| Field | Description |
|-------|-------------|
| `Result` | Geometry definition output |

## Example

```json
{
    "GeometryDefiner": {
        "Execution": {
            "input_parameters": {}
        },
        "type": "openFOAM.mesh.GeometryDefiner"
    }
}
```

!!! note
    This node is primarily used through the [FreeCAD workbench](../../../freecad.md) GUI. For command-line workflows, geometry is typically handled via [CopyFile](../../general/copy_file.md) to place STL files in the case directory.
