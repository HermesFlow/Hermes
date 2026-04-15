# Roadmap

Planned improvements and future features for Hermes.

## Execution Engines

- **Apache Airflow support** — Add Airflow DAG generation as an alternative to Luigi
- **Dask support** — Explore Dask as a lightweight execution engine for local workflows

## Node System

- **Node registry** — Centralized registry for discovering and validating node types
- **Node versioning** — Version tracking for node templates to manage compatibility
- **Typed interfaces** — Contract-first approach with typed input/output schemas

## Workflow Features

- **Conditional execution** — Support for `if/else` branching in workflows
- **Loop support** — Iterative execution patterns
- **Sub-workflows** — Nested workflow composition
- **Workflow validation** — Pre-execution validation of the complete dependency graph

## OpenFOAM Integration

- **OpenFOAM version detection** — Auto-detect installed OpenFOAM version
- **Extended solver support** — Add nodes for additional OpenFOAM solvers
- **Post-processing nodes** — Built-in nodes for common post-processing tasks (e.g., paraFoam, sample)

## GUI and Tooling

- **Web-based GUI** — Browser-based workflow editor as an alternative to FreeCAD
- **VS Code extension** — Workflow editing and validation within VS Code
- **Workflow visualization** — Interactive dependency graph viewer

## Infrastructure

- **CI/CD pipeline** — Automated testing and deployment
- **Package distribution** — PyPI package for easier installation
- **Documentation** — Expanded tutorials and API documentation

## Version History

| Version | Key Changes |
|---------|-------------|
| 3.4.0 | System command execution fixes |
| 3.3.1 | ScalarTransport example, coded boundary condition fixes |
| 3.3.0 | Variables and `#calc` support, OF10 compatibility |
| 3.2.0 | Write capability, removed hera-metadata |
| 3.1.0 | RunAll build nodes, workflow type attribute |
| 3.0.0 | Major internal refactoring |
| 2.0.0 | Hermes 2.0 release |
