# SetFields

Generates an OpenFOAM `setFieldsDict` file for setting initial field values in specific regions of the domain.

**Type:** `openFOAM.system.SetFields`

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `defaultFieldValues` | array | `[]` | Default field values to apply across the entire domain |

Additional region-specific field values can be defined through the template.

## Output

| Field | Description |
|-------|-------------|
| `Result` | The rendered `setFieldsDict` file content |

## Example

```json
{
    "SetFields": {
        "Execution": {
            "input_parameters": {
                "defaultFieldValues": [
                    "volScalarFieldValue alpha.water 0",
                    "volVectorFieldValue U (0 0 0)"
                ]
            }
        },
        "type": "openFOAM.system.SetFields"
    }
}
```
