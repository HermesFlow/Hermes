After Compiling FreeCAD a directory of FC build is now availabe. 
[ $fc_build --> fc_build=/mnt/build (in the current docker script)]

The files in Resources are the files which define the Hermes module resources.

the location of the files: $fc_build/data/Mod/Hermes/Resources

Steps:

1. Create the Hermes directory inside data/Mod
2. Create the Resources directory inside Hermes
3. Copy the files from github Resources to the Hermes Resources directory.
