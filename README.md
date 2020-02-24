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

The provided install.sh script can be used to produce a directory with all the necessary repositories (HermesFlow/pyHermes, HermesFlow/JsonExample, FreeCad), installs the docker image from https://gitlab.com/daviddaish/freecad_docker_env and sets up 2 docker scripts. 


### For users 


### For developers. 

