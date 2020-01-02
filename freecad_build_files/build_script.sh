#!/bin/bash
( apt-get update && apt-get install libqt5webkit5-dev)
set -e

cmake -j$(nproc) \
    -D BOOST_ROOT=/usr/local/include/boost \
    -D BUILD_QT5=ON -DBUILD_FEM=OFF -DBUILD_SANDBOX=ON \
    -D PYTHON_LIBRARY=/usr/local/lib/libpython3.7.a \
    -D PYTHON_INCLUDE_DIR=/usr/local/include/python3.7 \
    -D PYTHON_PACKAGES_PATH=/usr/local/lib/python3.7/site-packages \
    -D PYTHON_EXECUTABLE=/usr/local/bin/python3 \
    -D SHIBOKEN_INCLUDE_DIR=/usr/local/lib/python3.7/site-packages/shiboken2_generator/include \
    -D SHIBOKEN_LIBRARY=/usr/local/lib/python3.7/\
site-packages/shiboken2/libshiboken2.cpython-37-x86_64-linux-gnu.so.5.12 \
    -D PYSIDE_INCLUDE_DIR=/usr/local/lib/python3.7/site-packages/PySide2/include \
    -D PYSIDE_LIBRARY=/usr/local/lib/python3.7/site-packages\
/PySide2/libpyside2.cpython-37-x86_64-linux-gnu.so.5.12 \
    -D PYSIDE2RCCBINARY=/usr/local/lib/python3.7/site-packages/PySide2/pyside2-rcc \
    -D FREECAD_USE_QTWEBMODULE="Qt\ Webkit" \
    -S /mnt/source \
    -B /mnt/build

cd /mnt/build

make -j $(nproc)

# Note, had to add this to freecad source CMakeLists.txt:
# add_compile_options(-fpermissive -fPIC)

