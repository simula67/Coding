#!/bin/bash
while true;do
    echo -n "`whoami`@`hostname`:bashELL~$"
    read command
    if [ "$command" = "exit" ]; then
	exit;
    fi
    $command
done