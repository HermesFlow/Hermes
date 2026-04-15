# General Nodes

General nodes provide basic file operations, code execution, and template processing capabilities. These nodes are not specific to any simulation domain and can be used in any workflow.

## Available Nodes

| Node | Type | Description |
|------|------|-------------|
| [CopyDirectory](copy_directory.md) | `general.CopyDirectory` | Copy an entire directory to a new location |
| [CopyFile](copy_file.md) | `general.CopyFile` | Copy a single file |
| [RunOsCommand](run_os_command.md) | `general.RunOsCommand` | Execute a system/shell command |
| [RunPythonCode](run_python_code.md) | `general.RunPythonCode` | Execute a Python method from a module |
| [JinjaTransform](jinja_transform.md) | `general.JinjaTransform` | Apply Jinja2 template transformations |
| [FilesWriter](files_writer.md) | `general.FilesWriter` | Write files using content from node outputs |
| [Parameters](parameters.md) | `general.Parameters` | Define general simulation parameters |

## Common Patterns

### Chaining File Operations

```json
{
    "nodeList": ["CopyDirectory", "RunOsCommand"],
    "nodes": {
        "CopyDirectory": {
            "Execution": {
                "input_parameters": {
                    "Source": "template_case",
                    "Target": "my_case"
                }
            },
            "type": "general.CopyDirectory"
        },
        "RunOsCommand": {
            "Execution": {
                "input_parameters": {
                    "Command": "ls -la {CopyDirectory.output.Target}"
                }
            },
            "type": "general.RunOsCommand"
        }
    }
}
```

### Template-Based File Generation

```json
{
    "nodeList": ["Parameters", "JinjaTransform", "FilesWriter"],
    "nodes": {
        "Parameters": {
            "Execution": {
                "input_parameters": {
                    "velocity": 10.0,
                    "viscosity": 1e-6
                }
            },
            "type": "general.Parameters"
        },
        "JinjaTransform": {
            "Execution": {
                "input_parameters": {
                    "TemplatePath": "templates/config.j2",
                    "Parameters": "{Parameters.output}"
                }
            },
            "type": "general.JinjaTransform"
        },
        "FilesWriter": {
            "Execution": {
                "input_parameters": {
                    "Files": [
                        {
                            "Path": "output/config.txt",
                            "Content": "{JinjaTransform.output.Result}"
                        }
                    ]
                }
            },
            "type": "general.FilesWriter"
        }
    }
}
```
