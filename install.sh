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
    -i hash                 specify docker image id to use, default: $DOCKER_IMAGE_ID
    -d hash                 specify docker image digest to pull, default: $DOCKER_IMAGE_DIGEST
    -f hash                 specify freecad source hash to pull, default: $FREECAD_SOURCE_HASH
    -p diff-file            specify freecad source diff that fixes compilation problems, default patch file:  destination/pyHermes/$FREECAD_SOURCE_PATCH
    -v                      debug mode (implies "set -x")
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

#Gets absolute path
get_abs_filename() {
  # $1 : relative filename
  echo "$(cd "$(dirname "$1")" && pwd)/$(basename "$1")"
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
    docker_inspect_cmd='docker image inspect -f "{{.Id}}" registry.gitlab.com/daviddaish/freecad_docker_env'
    docker_id=`$docker_inspect_cmd`
    echo Docker image ID: $docker_id 

    docker_inspect_cmd='docker image inspect -f "{{.RepoDigests}}" registry.gitlab.com/daviddaish/freecad_docker_env'
    docker_digest=`$docker_inspect_cmd`
    echo Docker image digest: $docker_digest

#    if [[ "x$docker_inspect" = x*518df783c4d6* ]]; then 
    if [[ "x$docker_id" = x*"$DOCKER_IMAGE_ID"* ]]; then 
        echo "Docker image exists"
        if [[ "x$docker_digest" = x*"$DOCKER_IMAGE_DIGEST"* ]]; then 
            echo "Docker digest is correct"
            return 0
        else
            echo "Docker digest is wrong"
        fi
    fi
        
    res=0
    docker_image="registry.gitlab.com/daviddaish/freecad_docker_env@$DOCKER_IMAGE_DIGEST"
    echo "Will try to pull docker image $docker_image"
    docker pull $docker_image  || ( echo "Docker image pull failed"  ; res=1)

    return $res
    }

setup_docker_launch() {
    cat "$DESTINATION_FULL/pyHermes/freecad_build_files/docker.sh"   | sed "s/:latest/@$DOCKER_IMAGE_DIGEST/1" > "$DOCKER"
    chmod +x "$DOCKER"
    echo "Docker launch script generation for users"

    cat "$DESTINATION_FULL/pyHermes/freecad_build_files/docker_dev.sh" | sed "s/:latest/@$DOCKER_IMAGE_DIGEST/1" > "$DOCKER_DEV"
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

    fchash=`(cd "$DESTINATION_FULL/source";  git describe --tags --long 2>/dev/null)`
    if [ "x$fchash" = "x$FREECAD_SOURCE_HASH" ]; then
        echo "Hash  $FREECAD_SOURCE_HASH already cheked out"
    else
        (cd "$DESTINATION_FULL/source"; git reset --hard $FREECAD_SOURCE_HASH)
    fi
    #verify
    if [ "x$fchash" != "x$FREECAD_SOURCE_HASH" ]; then
        echo "Hash  $FREECAD_SOURCE_HASH wasn't cheked out"
        return 1
    fi
    cp -a "$DESTINATION_FULL/pyHermes/freecad_build_files/build_script.sh"  "$DESTINATION_FULL/source"
    if [[ ! "x$FREECAD_SOURCE_PATCH" = "x" ]]; then
        echo "Trying to patch the source with \"$FREECAD_SOURCE_PATCH\"..."
        if [[ ! -f "$FREECAD_SOURCE_PATCH" ]]; then 
           echo "Hash  $FREECAD_SOURCE_PATCH doesn't exist"
           return 1
        fi

        (cd "$DESTINATION_FULL/source" && patch -p1 -N -r - < "$FREECAD_SOURCE_PATCH" )
        echo success
    fi 
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
FREECAD_SOURCE_PATCH="freecad_5a352ea63_git.diff"
DOCKER_IMAGE_ID=ee7e3ecee4ca
DOCKER_IMAGE_DIGEST="sha256:6537079d971a332ba198967ede01748bb87c3a6618564cd2b11f8edcb42a80d0"
# Process the options
while getopts "o:b:d:f:p:i:vh" opt
do
    case $opt in
#columns    
        o)      DESTINATION="$OPTARG";; 
        b)      BUILD_DESTINATION="$OPTARG";; 
        d)      DOCKER_IMAGE_DIGEST="$OPTARG";;
        i)      DOCKER_IMAGE_ID="$OPTARG";;
        f)      FREECAD_SOURCE_HASH="$OPTARG";; 
        p)      FREECAD_SOURCE_PATCH=`get_abs_filename "$OPTARG"`;; 
        v)      set -x;;
        h|\?)   usage ;;
    esac
done


#setup destination
OS=`uname -s`
DESTINATION_FULL=
DOCKER_DEV=
DOCKER=
DESTINATION_FULL=`get_abs_filename "$DESTINATION"`
FREECAD_SOURCE_PATCH="$DESTINATION_FULL/pyHermes/freecad_5a352ea63_git.diff"
mkdir -p "$DESTINATION_FULL"
cd "$DESTINATION_FULL"

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





