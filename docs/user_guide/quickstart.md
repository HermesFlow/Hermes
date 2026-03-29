# Quick Start Tutorial

This tutorial shows how to create and run a simple Hermes workflow that copies a directory and then executes Python code.

## Step 1: Create the Workflow JSON

Create a file called `my_workflow.json`:

```json
{
    "workflow": {
        "root": null,
        "nodeList": [
            "CopyDirectory",
            "RunPythonCode"
        ],
        "nodes": {
            "CopyDirectory": {
                "Execution": {
                    "input_parameters": {
                        "Source": "source",
                        "Target": "target",
                        "dirs_exist_ok": true
                    }
                },
                "type": "general.CopyDirectory"
            },
            "RunPythonCode": {
                "Execution": {
                    "input_parameters": {
                        "ModulePath": "tutorial1",
                        "ClassName": "tutorialPrinter",
                        "MethodName": "printDirectories",
                        "Parameters": {
                            "source": "{CopyDirectory.output.Source}",
                            "target": "{CopyDirectory.output.Target}"
                        }
                    }
                },
                "type": "general.RunPythonCode"
            }
        }
    }
}
```

This workflow:

1. **CopyDirectory** — copies `source/` to `target/`
2. **RunPythonCode** — runs a Python method, receiving the copy outputs as parameters

Note how `RunPythonCode` references `{CopyDirectory.output.Source}` — this creates an automatic dependency.

## Step 2: Create the Source Directory

```bash
mkdir source
echo "Hello from Hermes!" > source/hello.txt
```

## Step 3: Build and Execute

Use the combined build-and-execute command:

```bash
hermes-workflow buildExecute my_workflow.json
```

Or run the steps separately:

```bash
# Expand the workflow with default values
hermes-workflow expand my_workflow.json my_case

# Build the Luigi Python file
hermes-workflow build my_workflow.json my_case

# Execute the workflow
hermes-workflow execute my_case
```

## Step 4: Check Results

The `target/` directory should now contain a copy of `source/`, and the Python code output should appear in the console.

## Next Steps

- **[Node Reference](nodes/index.md)** — explore all available node types
- **[Examples](../examples/index.md)** — see more complex workflow examples
- **[CLI Reference](cli.md)** — learn all command-line options
- **[Key Concepts](concepts.md)** — understand the architecture in depth
