# Installation & Setup

## Requirements

- Python 3.7+
- [Luigi](https://luigi.readthedocs.io/) (for workflow execution)
- [Jinja2](https://jinja.palletsprojects.com/) (for template processing)
- [FreeCAD](https://www.freecad.org/) (optional, for GUI workbench)

## Quick Install

Clone the repository and install:

```bash
git clone https://github.com/HermesFlow/Hermes.git
cd Hermes
pip install -e .
```

## Docker-Based Installation (with FreeCAD)

For the full environment including FreeCAD GUI support, use the provided install script:

```bash
chmod +x install.sh
./install.sh -o /path/to/destination
```

### Install Script Options

| Option | Description | Default |
|--------|-------------|---------|
| `-o destination` | Installation directory (required) | — |
| `-b hermes_branch` | Hermes branch to use | `master` |
| `-i docker_id` | Docker image ID | `ee7e3ecee4ca` |
| `-d docker_digest` | Docker image digest | (see script) |
| `-f freecad_hash` | FreeCAD source hash | `0.18-1194-g5a352ea63` |
| `-p diff_file` | FreeCAD source patch file | (auto-detected) |
| `-v` | Debug mode | off |

The install script:

1. Downloads and installs the Docker image from [FreeCAD Docker](https://gitlab.com/daviddaish/freecad_docker_env)
2. Sets up Docker launch scripts (`docker.sh`, `docker_dev.sh`)
3. Downloads required repositories (HermesFlow/pyHermes, HermesFlow/JsonExample, FreeCAD)
4. Sets up the Python environment in `dot_local` directory

## Verifying the Installation

```bash
hermes-workflow --help
```

You should see the available commands: `expand`, `build`, `execute`, and `buildExecute`.

## For Users (Running Workflows)

Use `docker.sh` inside the installation directory:

!!! note
    `xhost +` is required to allow X11 connection from Docker to the host's X11 server for displaying graphics.

```bash
xhost +
./docker.sh
```

## For Developers

Use `docker_dev.sh` which launches the build process:

```bash
./docker_dev.sh
```

This runs `/mnt/source/build_script.sh` with the FreeCAD Qt Webkit module configuration.

### Updating the Python Environment

1. Modify `docker_dev.sh` to bind `.local` in read-write mode (`rw`)
2. Install additional packages inside Docker: `pip3 install --user <package>`
3. Exit Docker
4. Archive the updated environment: `tar cvf dot_local.tar.gz`
5. Move the tarball into `freecad_build_files/` and commit
