#!/bin/bash
ARGS="$*"
ME=`basename $0`
usage() {
        cat <<EOF

Usage:
    $ME -d target_directory [-h git_hash] [-b build_destination]

Script that installs HermesFlow/pyHermes-enabled FreeCad  

Options:
    -o destination          directory which will contain the build files
    -b build_destination    scpecify separate build directory, default: $destination/build
    -d hash                 specify docker image hash to pull, default: $DOCKER_IMAGE_HASH
    -f hash                 specify freecad source hash to pull, default: $FREECAD_SOURCE_HASH
    -h,-?                   print this help message
    
Author: Yakov Mindelis
ISCFDC - Israeli CFD Center LTD

EOF
exit 1
}

myexit() {
    echo "Encountered an error, leaving \"$PWD\""
    exit
    }

    
git_pull() {
    res=0
    git_clone_output=`git clone "https://github.com/HermesFlow/$1.git" 2>&1`

    echo "$git_clone_output"
    

    if [[ "x$git_clone_output" = xfatal:* && "x$git_clone_output" = *"already exists and is not an empty directory"* ]]; then
        echo "Git tree $1 exist, trying to pull"
        
        git_clone_output=`(cd "$1" && git pull )`
        echo "$git_clone_output"
        fi

    if [[ "x$git_clone_output" = xfatal:* ||  "x$git_clone_output" = *error:* ]]; then
        echo "Git clone/pull failed for: $1"
        
        res=1
        fi
    return $res
    }

#verify docker command
check_docker() {
    docker=`which docker`
    if [ -z "$docker" ]; then 
        echo "Docker command not found"
        return 1
        fi
        
    return 0
    }
#verify docker image exists, download if needed
setup_docker() {
#docker image inspect -f "{{.Id}}" 518df783c4d6
    sudo=
    [ "x$OS" = "xLinux" ] && sudo=sudo
    docker_inspect_cmd=$sudo' docker image inspect -f "{{.Id}}" registry.gitlab.com/daviddaish/freecad_docker_env'
    echo $docker_inspect_cmd  "$docker_inspect_cmd" > docker_inspect_cmd
    docker_inspect=`$docker_inspect_cmd`
    echo $docker_inspect
#    if [[ "x$docker_inspect" = x*518df783c4d6* ]]; then 
    if [[ "x$docker_inspect" = x*ee7e3ecee4ca* ]]; then 
        echo "Docker image exists"
        return 0
        fi
        
    res=0
    echo "Docker image doesn't exist, will try to download"
    $sudo docker pull registry.gitlab.com/daviddaish/freecad_docker_env:$DOCKER_IMAGE_HASH  || ( echo "Docker image pull failed"  ; res=1)

    return $res
    }

setup_docker_launch() {
    #cat "$DESTINATION_FULL/pyHermes/freecad_build_files/docker.sh"     | sed "s#"\$"wd#"$DESTINATION_FULL/"#g"  \
    #> "$DOCKER"     || ( echo "Docker launch script generation for users failed"; return 1)
    cp -a "$DESTINATION_FULL/pyHermes/freecad_build_files/docker.sh"  "$DESTINATION_FULL/"
    chmod +x "$DOCKER"
    echo "Docker launch script generation for users"

    #cat "$DESTINATION_FULL/pyHermes/freecad_build_files/docker_dev.sh" | sed "s#"\$"wd#"$DESTINATION_FULL/"#g"  \
    #> "$DOCKER_DEV" || ( echo "Docker launch script generation for developers failed"; return 1)
    cp -a "$DESTINATION_FULL/pyHermes/freecad_build_files/docker_dev.sh"  "$DESTINATION_FULL/"
    chmod +x "$DOCKER_DEV"
    echo "Docker launch script generation for developers"
    return 0
    }

setup_source() {

    if [ ! -d "$DESTINATION_FULL/source/.git" ]; then 
        git clone https://github.com/FreeCAD/FreeCAD.git "$DESTINATION_FULL/source"

    else
        echo "\"$DESTINATION_FULL/source\" appears to be a git tree, will try to checkout"
    fi
    HASH=`(cd "$DESTINATION_FULL/source";  git describe --tags --long 2>/dev/null)`
    echo "HASH $HASH"
    set -x
    if [ "x$HASH" = "x$FREECAD_SOURCE_HASH" ]; then
        echo "Hash  $FREECAD_SOURCE_HASH already cheked out"
    else
        (cd "$DESTINATION_FULL/source"; git checkout $FREECAD_SOURCE_HASH)
    fi
    #verify
    if [ "x$HASH" != "x$FREECAD_SOURCE_HASH" ]; then
        echo "Hash  $FREECAD_SOURCE_HASH wasn't cheked out"
        return 1
    fi

    cp -a "$DESTINATION_FULL/pyHermes/freecad_build_files/build_script.sh"  "$DESTINATION_FULL/source"

    return 0

    }

setup_python() {
     ( cd "$DESTINATION_FULL" && tar xvf pyHermes/freecad_build_files/dot_local.tar.gz )
    return 0

    }
setup_examples() {
    rm -rf  "$DESTINATION_FULL/examples"
    mkdir -p  "$DESTINATION_FULL/examples"
    for e in JsonExample; do
        cp -a  "$DESTINATION_FULL/$e"  "$DESTINATION_FULL/examples"
    done
    return 0

    }

if [ "x$ARGS" = "x" ]; then
    usage
fi

#defaults
FREECAD_SOURCE_HASH="0.18-1194-g5a352ea63"
DOCKER_IMAGE_HASH=518df783c4d6

# Process the options
while getopts "o:b:d:f:h" opt
do
    case $opt in
#columns    
        o)      DESTINATION="$OPTARG";; 
        b)      BUILD_DESTINATION="$OPTARG";; 
        d)      HASH="$OPTARG";; 
        f)      FREECAD_SOURCE_HASH="$OPTARG";; 
        h|\?)   usage ;;
    esac
done


#setup destination
OS=`uname -s`
DESTINATION_FULL=
DOCKER_DEV=
DOCKER=
DESTINATION_FULL="$DESTINATION"
if [[ "x$DESTINATION" = x.* ]] || [[ ! "x$DESTINATION" = x~* ]] || [[ ! "x$DESTINATION" = x\/* ]]  ; then 
    DESTINATION_FULL="$PWD/$DESTINATION"
    fi
mkdir -p "$DESTINATION"
cd "$DESTINATION"

DOCKER="$DESTINATION_FULL/docker.sh"
DOCKER_DEV="$DESTINATION_FULL/docker_dev.sh"


repos="pyHermes JsonExample"
for repo in $repos; do
    git_pull "$repo" || myexit
done

check_docker || myexit
setup_docker || myexit
setup_docker_launch || myexit
setup_source || myexit
setup_python || myexit
setup_examples || myexit

"$DOCKER_DEV"





