# FreeCAD Integration

Hermes provides a custom workbench for [FreeCAD](https://www.freecad.org/) that enables visual configuration of workflow parameters, particularly useful for CFD simulations where 3D geometry is involved.

## Overview

The FreeCAD workbench allows you to:

- Set workflow parameters using a graphical interface
- Define boundary conditions on 3D geometry faces
- Configure mesh generation settings visually
- Manage OpenFOAM simulation parameters
- Export workflows as JSON files

Since Hermes workflows are focused on CFD and structural simulations, FreeCAD's 3D capabilities make it a natural fit for the GUI layer.

## Installation

The FreeCAD integration is installed as part of the Docker-based setup. See [Installation & Setup](installation.md) for details on the install script.

The workbench source is located in:

- `freecad_source_hermes/` — FreeCAD source modifications
- `hermes/Resources/workbench/` — Workbench node implementations

## Workbench Nodes

The FreeCAD workbench provides GUI wrappers for the following node types:

| Workbench Node | Underlying Node Type |
|----------------|---------------------|
| HermesBlockMesh | BlockMesh |
| HermesSnappyHexMesh | SnappyHexMesh |
| HermesGeometryDefiner | GeometryDefiner |
| HermesFvSolution | FvSolution |
| HermesFvSchemes | FvSchemes |
| HermesBC | Boundary Conditions |
| HermesGeneral | General nodes |

## Workflow

1. **Open FreeCAD** with the Hermes workbench active
2. **Import or create** 3D geometry for your simulation domain
3. **Add workflow nodes** using the workbench toolbar
4. **Configure parameters** in each node's property panel
5. **Define boundary conditions** by selecting geometry faces
6. **Export** the workflow as a JSON file
7. **Execute** using `hermes-workflow buildExecute workflow.json`

## WebGui Nodes

For simpler workflows, Hermes also provides web-based GUI nodes for configuring:

- **Transport Properties** — fluid properties and transport models
- **Turbulence** — turbulence model selection and parameters

These are accessible through the simple workflow interface and generate the same JSON output as the FreeCAD workbench.
