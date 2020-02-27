# Hermes

Hermes is a package designed to simplify the construction of a task-based workflow pipelines for executers like 
Luigi or Airflow. The Hermes package focuses on pipelines for CFD/solid applications.

A workflow is described using JSON file. The package consists of tools to transform the JSON-workflow 
to a Luigi (or other execution engine) python file. 
The package also constructs GUI to set the parameters of the workflow. 

Since the workflow is focused on CFD/structural simulations the GUI is based on FreeCAD package. 


## This project contains
1. FreeCad source modifications that allow the functionality of pyHermes

2. pyHermes Python source files and example

## Installation

The provided **install.sh** script can be used to produce and environment to run/develop FreeCad with HermesFlow.
The scriptperforms the following:

1. downloads and installs the docker image from:
    https://gitlab.com/daviddaish/freecad_docker_env 

2. sets up two docker launch scripts:
    docker.sh
    docker_dev.sh

 
3. downloads  the necessary repositories:
    HermesFlow/pyHermes
    HermesFlow/JsonExample
    FreeCad

4. sets up the python environment needed for running/development in "dot_local" directory that is bound to ~/.local of the docker user by means of bind directive in doker launch script, it contains the following python components:
    PyQt5
    jsonpath_rw_ext
    luigi

   to update the dot_local: 
   
   a. modify docker_dev.sh to bind the .local in read-write mode (rw)

   b. "pip3 --user install" the additional packages inside docker
   
   c. exit docker
   
   d. to commit the updated dot_local into git:
   
       i.   tar cvf dot_local.tar.gz
       ii.  move the tarbal into freecad_build_files of thew git tree
       iii. git commit -m "some comment" freecad_build_files/dot_local.tar.gz
       iv.  git push



Usage of install.sh, requires executable permissions of the script:

Usage:
```
    install.sh -d target_directory [-h git_hash] [-b build_destination]
```
Script that installs HermesFlow/pyHermes-enabled FreeCad

Options:
    -o destination          directory which will contain the build files
    -b build_destination    scpecify separate build directory, default: /build
    -d hash                 specify docker image hash to pull, default: ee7e3ecee4ca
    -f hash                 specify freecad source hash to pull, default: 0.18-1194-g5a352ea63
    -p diff-file            specify freecad source diff that fixes compilation problems, default patch file:  /Users/jack/iscfdc/freecad/freecad_5a352ea63_git.diff
    -h,-?                   print this help message

        
to produce a diff file from non-default source dir one should fixe the compilation problems and run:
    git diff > file.diff

To start working default patch file (freecad_build_files/freecad_5a352ea63_git.diff) and install script only are requiered to be located in the same directory, example installation command:
./install.sh -o output_directory

### For users 

Use docker.sh script inside the installation directory. Note: "xhost +"  is required to allow X11 connection from docker to hosts's X11 server to allow displaying graphics. 

### For developers. 

Use docker_dev.sh script inside the installation directory. The script will launch the /mnt/source/build_script.sh wish was produced from the original build_script.sh, it has the following modification:

    -D FREECAD_USE_QTWEBMODULE="Qt\ Webkit" 

Invoking the script will trigger build process. 

