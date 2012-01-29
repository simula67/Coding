#!/bin/bash
if [ $EUID -ne 0 ];
then
    echo "Need to be root to install stuff"
    exit 1
fi
sudo apt-get install xfce4-dev-tools gtk-doc-tools libxfce4util-dev libexo-1-dev libxfce4ui-1-dev 
