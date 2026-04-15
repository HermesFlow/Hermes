# Troubleshooting

## Common Issues

### `hermes-workflow` command not found

Make sure Hermes is installed and the `bin` directory is on your PATH:

```bash
pip install -e .
```

Or run directly:

```bash
python -m hermes.bin.hermes-workflow --help
```

### Luigi not found

Install Luigi:

```bash
pip install luigi
```

### Template not found errors

Ensure the workflow JSON references valid node types. Check available templates:

```bash
ls hermes/Resources/general/
ls hermes/Resources/openFOAM/
```

### Parameter reference errors

Parameter references use the format `{NodeName.output.FieldName}`. Common issues:

- **Misspelled node name** — the node name must match exactly (case-sensitive)
- **Node not in nodeList** — referenced nodes must be declared in the `nodeList` array
- **Circular dependencies** — nodes cannot reference each other's outputs

### FreeCAD Docker display issues

If the FreeCAD GUI doesn't appear, ensure X11 forwarding is enabled:

```bash
xhost +
./docker.sh
```

### Workflow execution hangs

- Check Luigi's scheduler status
- Verify all node dependencies can be satisfied
- Check for circular dependencies in parameter references
- Use `--force` flag to re-execute: `hermes-workflow execute myCase --force`

## Getting Help

- **GitHub Issues**: [HermesFlow/Hermes](https://github.com/HermesFlow/Hermes/issues)
- **Examples**: Check the `examples/` directory for working workflow references
