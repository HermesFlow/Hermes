# FAQ

## General

### What is Hermes?

Hermes is a Python framework for building task-based workflow pipelines described in JSON, with a focus on CFD and structural simulation applications. It translates JSON workflows into executable code for engines like Luigi.

### What execution engines does Hermes support?

Currently, Hermes supports **Luigi** as the execution engine. Support for **Apache Airflow** is planned.

### Do I need FreeCAD to use Hermes?

No. FreeCAD is optional and provides a GUI for configuring workflows. You can create and run workflows entirely from JSON files and the command line.

### What is the relationship between Hermes and OpenFOAM?

Hermes includes specialized nodes for generating OpenFOAM case files (mesh, solver settings, boundary conditions, etc.). It automates the creation of OpenFOAM directory structures and configuration files through template-based generation.

## Workflows

### Can I run workflows without Docker?

Yes. The Docker setup is primarily for FreeCAD integration. For command-line workflow execution, a standard Python installation with the required dependencies is sufficient.

### How do I pass parameters between nodes?

Use path expressions: `{NodeName.output.FieldName}`. This creates an automatic dependency — the referenced node will complete before the current node executes.

### Can I run nodes in parallel?

Yes. Luigi handles parallel execution automatically. Nodes that don't depend on each other will run concurrently.

### How do I add custom node types?

See the [Creating Custom Nodes](../developer_guide/creating_nodes.md) guide in the Developer Guide.

## OpenFOAM

### Which OpenFOAM versions are supported?

Hermes supports OpenFOAM versions 7 through 10. Some nodes (like TransportProperties vs. PhysicalProperties) are version-specific.

### Can I use Hermes with other CFD solvers?

While the built-in nodes focus on OpenFOAM, the general-purpose nodes (RunOsCommand, JinjaTransform, FilesWriter) can be used to automate any command-line application. Custom nodes can be created for other solvers.
