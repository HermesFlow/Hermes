Instruction for setting up deveoper environment of PyHermes2
============================================================

FreeCad source
--------------
Download source and checkout the hash 5a352ea63:

1. git clone 5a352ea63

2. mkdir build

3. mv FreeCAD freecad_source

4. ln -s freecad_source source 

6. cd !$ 

(running:
git describe --tags --long
should produce: 
0.19_pre-813-g5a352ea63)

4. export FCSRC="$PWD" 
or in tcsh: 
set FCSRC="$PWD" 

Copy  code modifications into FreeCad source:

cp -ai freecad_source_hermes/src/Mod/Web/Gui/AppWebGui.cpp PythonConsole.cppfreecad_source_hermes/src/Mod/Web/Gui/BrowserView.*  $FCSRC/src/Mod/Web/Gui
(3 files)

cp -ai freecad_source_hermes/src/Gui/PythonConsole.*  $FCSRC/src/Gui
(2 files)

Copy the modified build script 
cp -ai freecad_build_files/build_script.sh $FCSRC

(Modification made to the build script:
1. inserted "Qt Webkit" build optiofor buldern into cmake split command before 
"-S /mnt/source" line:

-D FREECAD_USE_QTWEBMODULE="Qt\ Webkit" \

2.  added package installation command: 

( apt-get update && apt-get install libqt5webkit5-dev)

)

Copy docker launch scripts:
docker.sh
docker_build.sh

Docker for builders: 
-------------------
1. docker pull registry.gitlab.com/daviddaish/freecad_docker_env:latest

2. change directory to the location where FreeCad source resides ($FCSRC/..)

2. launch freecad_build_files/docker_dev.sh
(verify $fc_source and $fc_build)

2. copy build_script.sh from freecad_build_files to $FCSRC and:

3. to bulld launch the docker and: 

cd /mnt/source
./build_script.sh

Docker for users: 
-------------------
1. docker pull registry.gitlab.com/daviddaish/freecad_docker_env:latest

2. launch freecad_build_files/docker.sh
(verify $fc_build)

3. run the command:
( apt-get update && apt-get install libqt5webkit5-dev)
(commit it to your docker image?)


4. /mnt/build/bin/FreeCad

