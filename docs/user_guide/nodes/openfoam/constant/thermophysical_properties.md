# ThermophysicalProperties

Generates the OpenFOAM `thermophysicalProperties` file for configuring thermodynamic and transport models in heat transfer simulations.

**Type:** `openFOAM.constant.ThermophysicalProperties`

## Parameters

The thermophysical parameters are configured through the Jinja template with standard OpenFOAM thermophysicalProperties fields.

## Output

| Field | Description |
|-------|-------------|
| `Result` | The rendered `thermophysicalProperties` file content |

## Example

```json
{
    "ThermophysicalProperties": {
        "Execution": {
            "input_parameters": {}
        },
        "type": "openFOAM.constant.ThermophysicalProperties"
    }
}
```

!!! note
    Required for solvers that include heat transfer (e.g., `buoyantSimpleFoam`, `buoyantPimpleFoam`). Defines the equation of state, transport model, and thermodynamic properties of the fluid.
