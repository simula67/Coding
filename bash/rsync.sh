#!/bin/bash
hour=`date +%k`
while true; do
    if [ $hour -gt "20" -a $hour -lt "8" ]; then
	#rsync
	if [ $? -eq 0 ]; then
	    #Schedule to call this script at 20:00 two days from now
	    exit 0
	fi
    else
	#Schdule to call this script at 20:00 next day
	exit 1
    fi
done
