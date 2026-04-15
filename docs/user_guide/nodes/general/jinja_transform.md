# JinjaTransform

Applies Jinja2 template transformations to generate output files. This node is central to OpenFOAM file generation, where Jinja templates are used to produce solver configuration files.

**Type:** `general.JinjaTransform`

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `TemplatePath` | string | Path to the Jinja2 template file |
| `Parameters` | object | Variables to pass to the template |

## Output

| Field | Description |
|-------|-------------|
| `Result` | The rendered template content |

## Example

```json
{
    "JinjaTransform": {
        "Execution": {
            "input_parameters": {
                "TemplatePath": "templates/controlDict.j2",
                "Parameters": {
                    "endTime": 1000,
                    "deltaT": 0.01,
                    "writeInterval": 100
                }
            }
        },
        "type": "general.JinjaTransform"
    }
}
```

!!! tip
    Most OpenFOAM nodes use JinjaTransform internally to render their configuration files from templates stored in `hermes/Resources/openFOAM/`.
