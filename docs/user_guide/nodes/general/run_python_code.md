# RunPythonCode

Executes a Python method from a specified module and class.

**Type:** `general.RunPythonCode`

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `ModulePath` | string | Python module path (importable) |
| `ClassName` | string | Class name within the module |
| `MethodName` | string | Method to call on the class |
| `Parameters` | object | Dictionary of parameters passed to the method |

## Output

The output depends on the return value of the called method.

## Example

```json
{
    "RunPythonCode": {
        "Execution": {
            "input_parameters": {
                "ModulePath": "my_module",
                "ClassName": "MyProcessor",
                "MethodName": "process",
                "Parameters": {
                    "input_dir": "{CopyDirectory.output.Target}",
                    "threshold": 0.5
                }
            }
        },
        "type": "general.RunPythonCode"
    }
}
```
