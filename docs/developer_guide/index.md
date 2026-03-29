# Developer Guide

This section is for developers working on or extending the Hermes framework. It covers architecture, internals, and how to create custom nodes.

---

## Architecture

- **[Core Concepts](architecture/core_concepts.md)** — The `workflow`, `TaskWrapper`, and node system
- **[Workflow Engine](architecture/workflow_engine.md)** — How workflows are loaded, resolved, and executed
- **[Execution Engines](architecture/execution_engines.md)** — Luigi integration and the engine abstraction layer

## Extending Hermes

- **[JSON Structure](json_structure.md)** — Complete JSON schema reference for workflows and nodes
- **[Creating Custom Nodes](creating_nodes.md)** — Step-by-step guide to adding new node types

## API Reference

- **[Workflow API](api/workflow.md)** — `workflow` and `hermesNode` classes
- **[TaskWrapper API](api/taskwrapper.md)** — `hermesTaskWrapper` class
- **[Engines API](api/engines.md)** — Luigi builder and transformer classes

## Roadmap

- **[Roadmap](roadmap.md)** — Planned improvements and future features
