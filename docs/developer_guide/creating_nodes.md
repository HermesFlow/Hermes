# Creating Custom Nodes

This guide walks through creating a new node type for Hermes.

## Node Structure

Each node type lives in `hermes/Resources/` and consists of:

```
hermes/Resources/<category>/<NodeName>/
├── jsonForm.json    # Template with schema and default values
└── executer.py      # (Optional) Custom execution logic
```

## Step 1: Create the Directory

```bash
mkdir -p hermes/Resources/general/MyCustomNode
```

## Step 2: Define the Template (`jsonForm.json`)

The template defines the node's parameters, default values, and optional GUI configuration:

```json
{
    "type": "general.MyCustomNode",
    "Execution": {
        "input_parameters": {
            "inputFile": "",
            "outputFile": "",
            "processMode": "default"
        }
    },
    "GUI": {
        "Schema": {
            "type": "object",
            "properties": {
                "inputFile": {
                    "type": "string",
                    "title": "Input File Path"
                },
                "outputFile": {
                    "type": "string",
                    "title": "Output File Path"
                },
                "processMode": {
                    "type": "string",
                    "title": "Processing Mode",
                    "enum": ["default", "fast", "thorough"]
                }
            }
        },
        "uiSchema": {},
        "formData": {
            "inputFile": "",
            "outputFile": "",
            "processMode": "default"
        }
    }
}
```

## Step 3: Implement the Executer (Optional)

If your node needs custom execution logic beyond what the general executers provide, create an `executer.py`:

```python
class executer:
    """Executer for MyCustomNode."""

    @staticmethod
    def inputs():
        """Define expected input parameters."""
        return ["inputFile", "outputFile", "processMode"]

    @staticmethod
    def outputs():
        """Define output fields."""
        return ["Result", "inputFile", "outputFile"]

    @staticmethod
    def run(input_parameters):
        """Execute the node logic.

        Args:
            input_parameters: dict of resolved input parameters

        Returns:
            dict of output values
        """
        input_file = input_parameters["inputFile"]
        output_file = input_parameters["outputFile"]
        mode = input_parameters["processMode"]

        # Your custom logic here
        result = process_file(input_file, output_file, mode)

        return {
            "Result": result,
            "inputFile": input_file,
            "outputFile": output_file
        }
```

## Step 4: Use the Node in a Workflow

Reference your node by its type path:

```json
{
    "MyStep": {
        "type": "general.MyCustomNode",
        "Execution": {
            "input_parameters": {
                "inputFile": "data/input.csv",
                "outputFile": "results/output.csv",
                "processMode": "fast"
            }
        }
    }
}
```

Or reference the template:

```json
{
    "MyStep": {
        "Template": "general.MyCustomNode.jsonForm"
    }
}
```

## Step 5: Add a Specialized Wrapper (Optional)

For nodes that need custom dependency handling or engine-specific code generation, create a specialized wrapper in `hermes/taskwrapper/specializedwrapper/`:

```python
from hermes.taskwrapper.wrapper import hermesTaskWrapper

class MyCustomNodeWrapper(hermesTaskWrapper):
    """Specialized wrapper for MyCustomNode."""

    def getRequiredTasks(self, taskJSON):
        """Custom dependency extraction."""
        required = super().getRequiredTasks(taskJSON)
        # Add custom logic
        return required
```

## Step 6: Add a Luigi Transformer (Optional)

For nodes that need custom Luigi code generation, add a transformer in `hermes/engines/luigi/`:

```python
from hermes.engines.luigi.pythonClassBase import pythonClassBase

class MyCustomNodeTransformer(pythonClassBase):
    """Generates Luigi task code for MyCustomNode."""

    def transform(self, taskWrapper):
        """Generate Luigi task class code."""
        # Custom code generation
        pass
```

## Adding OpenFOAM Nodes

OpenFOAM nodes typically use Jinja2 templates for file generation. The pattern is:

1. Create a Jinja2 template in the node directory (e.g., `template.j2`)
2. The executer renders the template with the input parameters
3. The output `Result` field contains the rendered file content

```
hermes/Resources/openFOAM/system/MyDict/
├── jsonForm.json
├── executer.py
└── template.j2
```

## Testing

Test your node by creating a workflow JSON and running it:

```bash
hermes-workflow buildExecute test_workflow.json
```

Check the output JSON files to verify the node produced correct results.
