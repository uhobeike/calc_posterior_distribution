#!/bin/bash -evx

mkdir build -p
cd build
cmake ..
make
cp bin/* ~/.local/bin
cd ..
rm -r build