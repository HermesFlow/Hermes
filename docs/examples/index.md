# Examples

Hermes includes several example workflows ranging from simple file operations to complete OpenFOAM simulation setups.

## General Examples

### Copy Directory

A minimal workflow that copies a directory:

```bash
hermes-workflow buildExecute examples/general/copyDir/copyDir.json
```

### All Nodes

Demonstrates all available node types in a single workflow:

```bash
hermes-workflow buildExecute examples/allNodes/allNodes.json
```

## OpenFOAM Examples

### simpleFoam

Steady-state incompressible flow simulation:

```bash
hermes-workflow buildExecute examples/openFOAM/simpleFoam/simpleFoam.json
```

This example sets up a complete simpleFoam case including:

- Mesh generation (BlockMesh)
- Transport and turbulence properties
- Solver settings (SIMPLE algorithm)
- Boundary conditions
- Execution scripts

### scalarTransportFoam

Scalar transport simulation:

```bash
hermes-workflow buildExecute examples/openFOAM/scalarTransportFoam/scalarTransport.json
```

### Stochastic Lagrangian

Particle dispersion using Lagrangian tracking:

```bash
hermes-workflow buildExecute examples/openFOAM/stochasticLagrangian/stochasticLagrangian.json
```

### Indoor Buoyancy (Boussinesq)

Buoyancy-driven indoor airflow simulation:

```bash
hermes-workflow buildExecute examples/openFOAM/indoorFOAMBoussinesq/indoorFOAM.json
```

## Tutorial Workflows

Step-by-step tutorial workflows are available in `examples/Tutorial/`:

- **Tutorial 1** — Copy a directory and run Python code
- **Tutorial 2** — Use parameters, OS commands, and Jinja templates

See the [Quick Start Tutorial](../user_guide/quickstart.md) for a guided walkthrough.

## Exploring Examples

All example workflow JSON files are in the `examples/` directory:

```
examples/
├── general/          # Simple general-purpose workflows
├── allNodes/         # All node types demonstration
├── mesh/             # Mesh generation workflows
├── openFOAM/         # Complete CFD simulation setups
│   ├── simpleFoam/
│   ├── scalarTransportFoam/
│   ├── stochasticLagrangian/
│   └── indoorFOAMBoussinesq/
└── Tutorial/         # Step-by-step tutorials
```
