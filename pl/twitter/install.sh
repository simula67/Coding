#!/bin/bash
# This scipt sets up the necessary packages for using the tweeter script
# However you need to install the IO::Interactive module by downloading the source
# You also need the App::Tweet Perl module on which the script is based
# Coded by : simula67
if [ $EUID -ne 0 ]; then
    echo "You need to be root to run this script"
    exit 1
fi
apt-get install libcrypt-cbc-perl libfile-homedir-perl libcrypt-blowfish-perl libfile-slurp-perl libfile-touch-perl libconfig-yaml-perl liblog-log4perl-perl libnet-twitter-perl libstring-random-perl libterm-prompt-perl 
echo -n "Enter your user twitter username : "
read twit_user
echo -n "Enter your username(for Linux) : "
read lin_user
echo "export HISTIGNORE=*twitter.pl*$twit_user*">>/home/$lin_user/.bashrc
