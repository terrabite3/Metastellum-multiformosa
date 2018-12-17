#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"
cd $DIR

if ps -e | grep -P "(python3|fbi)" ; then
    echo "Metastellum is already running"
    exit 1

./metastellum.py &

# Remove any leftover links from last time
rm link*.png

# Wait for the python script to create the links to the first frame
while [ ! -e "link3.png" ]
do
    sleep 1
done

# Start the image viewer
fbi link*.png