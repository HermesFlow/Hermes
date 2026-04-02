# RefineMesh

Generates mesh refinement instructions for refining specific regions of an OpenFOAM mesh.

**Type:** `openFOAM.mesh.RefineMesh`

## Overview

RefineMesh renders a template to produce mesh refinement configuration, typically used after initial mesh generation to increase resolution in areas of interest.

## Parameters

Refinement parameters are configured through the Jinja template.

## Output

| Field | Description |
|-------|-------------|
| `openFOAMfile` | The rendered mesh refinement configuration |

## Example

```json
{
    "RefineMesh": {
        "Execution": {
            "input_parameters": {}
        },
        "type": "openFOAM.mesh.RefineMesh"
    }
}
```

!!! tip
    Use with [TopoSetDict](../system/topo_set_dict.md) to define refinement regions before applying refinement.
