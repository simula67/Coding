#!/bin/bash
if [ `whoami` != 'root' ]; then
    echo "You are not root!!"
    exit 1
fi
while true; do
    xset dpms force off
    sleep 29
done
