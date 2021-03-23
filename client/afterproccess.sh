#!/bin/bash

if [ -n "$1" ]; then
    tarfile=$1
else
    echo "arguments error, exit."
    exit
fi

echo "[Target file] "$tarfile

tar -xzvf $tarfile

if [ -e "/usr/bin/dss" ]; then
    rm /usr/bin/dss
fi
