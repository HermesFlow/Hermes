#!/bin/sh

fc_source="$PWD/source"
fc_build="$PWD/build"
fc_build_files="$PWD/pyHermes/freecad_build_files/"

sudo docker run -it --rm \
-v $fc_source:/mnt/source \
-v $fc_build:/mnt/build \
-v $fc_build_files:/mnt/build_files \
-v $fc_build_files/bashrc_dev:/root/.bashrc:ro \
-v $fc_build_files/dot_local:/root/.local:ro \
-v $other_files:/mnt/files \
-e "DISPLAY" -e "QT_X11_NO_MITSHM=1" -v /tmp/.X11-unix:/tmp/.X11-unix:ro \
registry.gitlab.com/daviddaish/freecad_docker_env:latest


