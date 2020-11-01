#!/bin/sh

#Gets absolute path
get_abs_filename() {
  # $1 : relative filename
  echo "$(cd "$(dirname "$1")" && pwd)/$(basename "$1")"
}
me=`get_abs_filename $0`
wd=`dirname "$me"`

fc_source="$wd/source"
fc_build="$wd/build"
hermes="$wd/Hermes_git/hermes"
examples="$wd/Hermes_git/examples"
projects="$wd/projects"
fc_build_files="$wd/Hermes_git/freecad_build_files/"
fc_workbench="$wd/Hermes_git/hermes/Resources/workbench"

docker run -it --rm \
-v "$fc_source":/mnt/source \
-v "$fc_build":/mnt/build \
-v "$examples":/mnt/examples \
-v "$hermes":/mnt/build/hermes \
-v "$projects":/mnt/projects \
-v "$fc_workbench":/mnt/workbench \
-v "$fc_build_files/bashrc_dev":/root/.bashrc:ro \
-v "$wd/dot_local":/root/.local:ro \
-v "$other_files":/mnt/files \
-v "$PWD":/mnt/pwd \
$* \
-e "DISPLAY" -e "QT_X11_NO_MITSHM=1" -v /tmp/.X11-unix:/tmp/.X11-unix:ro \
registry.gitlab.com/daviddaish/freecad_docker_env:latest


