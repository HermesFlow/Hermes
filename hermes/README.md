# pyHermes

The Python execution engine for the Hermes workflow framework.

Translates JSON workflow definitions into executable [Luigi](https://luigi.readthedocs.io/) pipelines, automating the construction of task-based workflows for CFD and structural simulation applications.

**Full documentation: [https://hermesflow.github.io/Hermes/](https://hermesflow.github.io/Hermes/)**

## Package Structure

```
hermes/
├── bin/                    # CLI entry point (hermes-workflow)
├── workflow/               # Core workflow engine
│   ├── workflow.py         # Workflow class — loads JSON, builds dependency graph
│   ├── expandWorkflow.py   # Template expansion
│   └── reverse.py          # Reverse-engineer workflows from existing cases
├── taskwrapper/            # Task wrapper abstraction
│   ├── wrapper.py          # hermesTaskWrapper — holds task metadata & connectivity
│   ├── wrapperHome.py      # Wrapper factory
│   └── specializedwrapper/ # Domain-specific wrappers (OpenFOAM)
├── engines/                # Execution engine implementations
│   └── luigi/              # Luigi engine (builder, transformers, utilities)
├── Resources/              # Node type definitions & templates
│   ├── general/            # General nodes (CopyDirectory, RunOsCommand, Jinja, etc.)
│   ├── openFOAM/           # OpenFOAM nodes (mesh, system, constant, dispersion)
│   ├── BC/                 # Boundary condition nodes
│   ├── executers/          # Shared execution logic
│   └── workbench/          # FreeCAD workbench GUI nodes
├── utils/                  # Utility modules (JSON, workflow assembly)
└── hermesLogging/          # Logging configuration
```

## Installation

```bash
pip install -e .
```

## Usage

```bash
# Build and execute a workflow
hermes-workflow buildExecute workflow.json

# Or step by step
hermes-workflow expand workflow.json myCase
hermes-workflow build workflow.json myCase
hermes-workflow execute myCase
```

## Key Classes

- **`workflow`** (`workflow/workflow.py`) — central engine that loads JSON, resolves templates, and builds the task network
- **`hermesTaskWrapper`** (`taskwrapper/wrapper.py`) — wraps each node with metadata, parameters, and dependency information
- **`hermesNode`** (`workflow/workflow.py`) — interface to individual node JSON definitions
- **`LuigiBuilder`** (`engines/luigi/builder.py`) — generates Luigi Python code from the task network

See the [Developer Guide](https://hermesflow.github.io/Hermes/developer_guide/) for architecture details and API reference.
