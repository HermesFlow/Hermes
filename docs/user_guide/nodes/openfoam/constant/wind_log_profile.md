# HomogenousWindLogProfile

Generates the OpenFOAM `homogenousWindLogProfileDict` file for configuring atmospheric boundary layer wind profiles based on the logarithmic wind law.

**Type:** `openFOAM.constant.homogenousWindLogProfileDict`

## Parameters

The wind profile parameters are configured through the Jinja template with standard atmospheric boundary layer fields.

## Output

| Field | Description |
|-------|-------------|
| `Result` | The rendered `homogenousWindLogProfileDict` file content |

## Example

```json
{
    "WindProfile": {
        "Execution": {
            "input_parameters": {}
        },
        "type": "openFOAM.constant.homogenousWindLogProfileDict"
    }
}
```

!!! note
    This node is used in atmospheric dispersion simulations to define the inlet wind profile following the logarithmic law for the atmospheric boundary layer.
