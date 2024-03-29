#!/bin/bash
ARGS="$*"
ME=`basename $0`
usage() {
        cat <<EOF

Usage:
    $ME -o destination [-f freecad_hash] [-d docker_digest] [-i docker_id] [-p diff_file]  [-b hermes_branch]

Script that installs $HERMES_REPO-enabled FreeCad  

Options:
    -o destination          directory which will contain the build files
    -b hermes_branch        scpecify $HERMES_REPO branch
    -i docker_id            specify docker image id to use, default: $DOCKER_IMAGE_ID
    -d docker_digest        specify docker image digest to pull, default: $DOCKER_IMAGE_DIGEST
    -f freecad_hash         specify freecad source hash to pull, default: $FREECAD_SOURCE_HASH
    -p diff-file            specify freecad source diff that fixes compilation problems, default patch file:  destination/Hermes_git/$FREECAD_SOURCE_PATCH
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
    branchopts=
    if [ "x$HERMES_BRANCH" != "xmaster" ]; then 
        branchopts="-b $HERMES_BRANCH"
    fi


    git_clone_output=`git clone $branchopts "https://github.com/$1.git" $2 2>&1`

    echo "$git_clone_output"
    
    if [[ "x$git_clone_output" = x*fatal:* && "x$git_clone_output" = *"Repository not found"* ]]; then
        res=1

    elif [[ "x$git_clone_output" = x*fatal:* && "x$git_clone_output" = *"already exists and is not an empty directory"* ]]; then
        echo "Git tree $1 exist, trying to pull"
        
        git_clone_output=`(cd "$2" && git pull )`
        echo "$git_clone_output"

    elif [[ "x$git_clone_output" = xfatal:* ||  "x$git_clone_output" = *error:* ]]; then
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
    docker_image="registry.gitlab.com/daviddaish/freecad_docker_env"
    if [[ "x$DOCKER_IMAGE_DIGEST" != "x" ]]; then
        docker_image="$docker_image""@""$DOCKER_IMAGE_DIGEST"
    else
        DOCKER_IMAGE_DIGEST=":latest"
        docker_image="$docker_image$DOCKER_IMAGE_DIGEST"
    fi
    echo "Will try to pull docker image $docker_image"
    echo docker pull $docker_image 
    docker pull $docker_image  || res=1
    if [ $res -eq  1 ];  then
        echo "Docker image pull failed"
    fi
    return $res
    }

#Docker launch scripts
setup_docker_launch() {
    res=0
    for dockerscript in freecad.sh freecad_dev.sh freecad_dev_compile.sh; do
        cat "$DESTINATION_FULL/Hermes_git/freecad_build_files/$dockerscript"   | sed "s/:latest/@$DOCKER_IMAGE_DIGEST/1" | sed "s/@:/:/g" > "$DESTINATION_FULL/$dockerscript" || res=1
        if [ ! $res -eq 0 ]; then
            echo "Docker launch script \"$dockerscript\" creation failed"
            return $res
        fi

        chmod +x  "$DESTINATION_FULL/$dockerscript" || res=1
        if [ ! $res -eq 0 ]; then
            echo "Docker launch script \"$dockerscript\" permissions setup failed"
            return $res
        fi

        echo "Docker launch script \"$dockerscript\" generation"
    done

    return $res
    }

#FC source + source additions
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
        fchash=`(cd "$DESTINATION_FULL/source";  git describe --tags --long 2>/dev/null)`
    fi
    #verify
    if [ "x$fchash" != "x$FREECAD_SOURCE_HASH" ]; then
        echo "Hash  $FREECAD_SOURCE_HASH wasn't cheked out"
        return 1
    fi
    cp -a "$DESTINATION_FULL/Hermes_git/freecad_build_files/build_script.sh"  "$DESTINATION_FULL/source"
    if [[ ! "x$FREECAD_SOURCE_PATCH" = "x" ]]; then
        echo "Trying to patch the source with \"$FREECAD_SOURCE_PATCH\"..."
        if [[ ! -f "$FREECAD_SOURCE_PATCH" ]]; then 
           echo "Hash  $FREECAD_SOURCE_PATCH doesn't exist"
           return 1
        fi

        (cd "$DESTINATION_FULL/source" && patch -p1 -N -r - < "$FREECAD_SOURCE_PATCH" )
        echo success
    fi 
    echo Copying  "$DESTINATION_FULL/Hermes_git/freecad_source_hermes/src" to   "$DESTINATION_FULL/source"
    cp -a   "$DESTINATION_FULL/Hermes_git/freecad_source_hermes/src" "$DESTINATION_FULL/source" || return 1
    return 0

    }

setup_mod_hermes() {
    res=0

    dirmod="$DESTINATION_FULL/build/Mod"
    dirhermes="$DESTINATION_FULL/build/hermes"
    dirmodhermes="$dirmod/Hermes_git"
    dirdatamodhermes="$DESTINATION_FULL/build/data/Mod/Hermes"
    dirdatamodhermesresources="$dirdatamodhermes/Resources"
    direxamples="$DESTINATION_FULL/build/examples"

#SETUP build/Mod/Hermes_git
#if exists remove
    dir="$dirmodhermes"
    if [ -d  $dir ]; then 
        echo Removing  "$dir" 
        rm  -rf  "$dir" 
    fi

#mkdir the build/Mod on demand
    dir="$dirmod"
    mkdir -p  "$dir" || res=1
    if [ ! $res -eq 0 ]; then
        echo mkdir  \"$dir\" failed
        return $res
    fi


#SETUP build/hermes
#if exists remove
    dir="$dirhermes"
    mkdir -p "$dir"
    if ! find -- "$dir" -prune -type d -empty | grep -q . ; then 
        res=1
        echo Non-empty  "$dir" 
        return $res
    fi
    
 #SETUP link Mod/Hermes_git
    dir="$dirmodhermes"

    rm -f  "$dir" || res=1
    if [ ! $res -eq 0 ]; then
        echo rm -f  \"$dir\" failed
        return $res
    fi

    ln -s /mnt/workbench   "$dir" || res=1
    if [ ! $res -eq 0 ]; then
        echo ln -s /mnt/workbench  \"$dir\" failed
        return $res
    fi

#SETUP data/Mod/Hermes_git
    #if exists remove
    dir="$dirdatamodhermes"
    if [ -d  $dir ]; then 
        echo Removing  "$dir" 
        rm  -rf  "$dir" 
    fi

#mkdir the build/data/Mod/Hermes_git on demand
    dir="$dirdatamodhermes"
    mkdir -p  "$dir" || res=1
    if [ ! $res -eq 0 ]; then
        echo mkdir  \"$dir\" failed
        return $res
    fi

#copy the Resources
    freecadResources="$DESTINATION_FULL/Hermes_git/freecad_Resources"
    cp -a "$freecadResources"  "$dirdatamodhermesresources" || res=1
    if [ ! $res -eq 0 ]; then
        echo  Copying  \"$freecadResources\"  to \"$dirdatamodhermesresources\" failed
        return $res
    fi
    
    return $res

}
 
setup_python() {
    res=0

    ( cd "$DESTINATION_FULL" && tar xf Hermes_git/freecad_build_files/dot_local.tar.gz ) || res=1
    if [ ! $res -eq 0 ]; then
        echo "Setting up the .local with python stuff  failed"
    fi

    return $res

    }

#defaults
FREECAD_SOURCE_HASH="0.18-1194-g5a352ea639"
FREECAD_SOURCE_PATCH="freecad_5a352ea63_git.diff"
DOCKER_IMAGE_ID=ee7e3ecee4ca
#DOCKER_IMAGE_DIGEST="sha256:6537079d971a332ba198967ede01748bb87c3a6618564cd2b11f8edcb42a80d0"
DOCKER_IMAGE_DIGEST=
HERMES_BRANCH=master
HERMES_REPO="HermesFlow/Hermes"
# Process the options
if [ "x$ARGS" = "x" ]; then
    usage
fi

while getopts "o:b:d:f:p:i:vh" opt
do
    case $opt in
#columns    
        o)      DESTINATION="$OPTARG";; 
        b)      HERMES_BRANCH="$OPTARG";; 
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
FREECAD_SOURCE_PATCH="$DESTINATION_FULL/Hermes_git/freecad_5a352ea63_git.diff"
mkdir -p "$DESTINATION_FULL"
cd "$DESTINATION_FULL"

DOCKER="$DESTINATION_FULL/freecad.sh"
DOCKER_DEV="$DESTINATION_FULL/freecad_dev.sh"
DOCKER_DEV_COMPILE="$DESTINATION_FULL/freecad_dev_compile.sh"

git_pull "$HERMES_REPO" Hermes_git || myexit

check_docker || myexit
setup_docker || myexit
setup_docker_launch || myexit
setup_source || myexit
setup_mod_hermes || myexit
setup_python || myexit

"$DOCKER_DEV_COMPILE"






