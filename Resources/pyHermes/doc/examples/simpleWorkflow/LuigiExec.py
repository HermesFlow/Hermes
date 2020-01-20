import os,stat

fullPath="./runLuigi.sh"

os.chmod(fullPath, stat.S_IRWXU)
os.system(fullPath)
