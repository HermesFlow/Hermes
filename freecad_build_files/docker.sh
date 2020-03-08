#!/bin/sh

#Gets absolute path
get_abs_filename() {
  # $1 : relative filename
  echo "$(cd "$(dirname "$1")" && pwd)/$(basename "$1")"
}
me=`get_abs_filename $0`
wd=`dirname "$me"`

fc_examples="$wd/examples"    
fc_build="$wd/build"
fc_build_files="$wd/pyHermes/freecad_build_files/"

docker run -it --rm \
-v "$fc_build":/mnt/build \
-v "$fc_examples":/mnt/examples \
-v "$fc_build_files/bashrc":/root/.bashrc:ro \
-v "$other_files":/mnt/files \
-v "$wd/dot_local":/root/.local:ro \
-e "DISPLAY" -e "QT_X11_NO_MITSHM=1" -v /tmp/.X11-unix:/tmp/.X11-unix:ro \
registry.gitlab.com/daviddaish/freecad_docker_env:latest


