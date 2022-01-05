#!/bin/sh

#Gets absolute path
get_abs_filename() {
  # $1 : relative filename
  echo "$(cd "$(dirname "$1")" && pwd)/$(basename "$1")"
}
me=`get_abs_filename $0`
wd=`dirname "$me"`

fc_build="$wd/build"
fc_build_files="$wd/Hermes_git/freecad_build_files/"
fc_resources="$wd/Hermes_git/freecad_Resources/"
fc_workbench="$wd/Hermes_git/hermes/Resources/workbench"
hermes="$wd/Hermes_git/hermes"
examples="$wd/Hermes_git/examples"
projects="$wd/projects"


IFACES=$(ifconfig | egrep -e "^en|^eth" | cut -d: -f1)
[ "$IFACES" ] || \
    usage "Cannot find a network interface for DISPLAY with ifconfig" \
          "Please report an issue at http://bugs.openfoam.org" \
          "    providing the output of the command: ifconfig"

for I in $IFACES
do
    IP=$(ifconfig "$I" | grep inet | awk '$1=="inet" {print $2}')
    [ "$IP" ] && break
done

[ "$IP" ] || \
    usage "Cannot find a network IP for DISPLAY with ifconfig" \
          "Please report an issue at http://bugs.openfoam.org" \
          "    providing the output of the command: ifconfig"

xhost + "$IP"

docker run -it --rm \
-v "$fc_build":/mnt/build \
-v "$fc_resources":/mnt/build/data/Mod/Hermes/Resources \
-v "$examples":/mnt/examples \
-v "$hermes":/mnt/build/hermes \
-v "$projects":/mnt/projects \
-v "$fc_workbench":/mnt/workbench \
-v "$fc_build_files/bashrc":/root/.bashrc:ro \
-v "$wd/dot_local":/root/.local:ro \
-v "$PWD":/mnt/pwd \
$* \
-e "DISPLAY" -e "QT_X11_NO_MITSHM=1" -v /tmp/.X11-unix:/tmp/.X11-unix:ro \
registry.gitlab.com/daviddaish/freecad_docker_env:latest


