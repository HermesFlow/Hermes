# MakeFlowDispersion

Prepares flow fields for dispersion simulations by extracting and transforming data from a base flow solution.

**Type:** `openFOAM.dispersion.MakeFlowDispersion`

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `baseFlow` | object | — | Base flow case configuration (see below) |
| `dispersionFields` | object | `{"CellHeights": {}}` | Fields to generate for dispersion |
| `Hmix` | object | `{"internalField": 1000}` | Mixing height field definition |
| `ustar` | object | `{"internalField": 0.1}` | Friction velocity field definition |

### baseFlow

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `name` | string | `"../flow/simpleStation"` | Path to the base flow case |
| `useTime` | number | `50` | Time step to extract from the flow solution |
| `maximalDispersionTime` | number | `3600` | Maximum time for the dispersion simulation [s] |

## Output

| Field | Description |
|-------|-------------|
| `casePath` | Path to the prepared dispersion case directory |

## Example

```json
{
    "MakeFlowDispersion": {
        "Execution": {
            "input_parameters": {
                "baseFlow": {
                    "name": "../flow/steadyState",
                    "useTime": 100,
                    "maximalDispersionTime": 7200
                },
                "dispersionFields": {
                    "CellHeights": {}
                },
                "Hmix": {
                    "internalField": 1500
                },
                "ustar": {
                    "internalField": 0.3
                }
            }
        },
        "type": "openFOAM.dispersion.MakeFlowDispersion"
    }
}
```

!!! note
    This node integrates with the Hera toolkit to prepare flow fields. It optionally runs the `indoorDistanceFromWalls` OpenFOAM utility when the `buildDistanceFromWalls` flag is enabled.
