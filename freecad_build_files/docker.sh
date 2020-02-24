#!/bin/sh

wd=`dirname $0`
if [ ! "x$wd" = x\/* && ! "x$wd" = x~ ]; then
    wd="$PWD/$wd"
    fi

    
fc_build="$wd/build"

docker run -it --rm \
-v "$fc_build":/mnt/build \
-v "$other_files":/mnt/files \
-v "$fc_build_files/bashrc":/root/.bashrc:ro \
-v "$wd/dot_local":/root/.local:rw \
-e "DISPLAY" -e "QT_X11_NO_MITSHM=1" -v /tmp/.X11-unix:/tmp/.X11-unix:ro \
registry.gitlab.com/daviddaish/freecad_docker_env:latest


