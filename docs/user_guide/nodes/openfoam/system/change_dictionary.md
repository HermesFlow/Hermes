# ChangeDictionary

Generates an OpenFOAM `changeDictionaryDict` file for modifying field values and boundary conditions in an existing case.

**Type:** `openFOAM.system.ChangeDictionary`

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `fields` | object | `{}` | Dictionary of field modifications to apply |

The `fields` object maps field names to their boundary condition changes, following the OpenFOAM changeDictionary format.

## Output

| Field | Description |
|-------|-------------|
| `Result` | The rendered `changeDictionaryDict` file content |

## Example

```json
{
    "ChangeDictionary": {
        "Execution": {
            "input_parameters": {
                "fields": {
                    "U": {
                        "inlet": {
                            "type": "fixedValue",
                            "value": "uniform (10 0 0)"
                        },
                        "outlet": {
                            "type": "zeroGradient"
                        }
                    },
                    "p": {
                        "outlet": {
                            "type": "fixedValue",
                            "value": "uniform 0"
                        }
                    }
                }
            }
        },
        "type": "openFOAM.system.ChangeDictionary"
    }
}
```

!!! note
    This node is commonly used together with the [Boundary Conditions](../boundary_conditions.md) node for setting field values on mesh patches.
