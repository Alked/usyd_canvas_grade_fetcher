#!/bin/bash

if command -v python3 >/dev/null 2>&1; then
	echo 'Python3.x has been installed.'
else
	echo 'FATAL: Python3.x is not installed.'
	echo 'Script terminated'
	exit
fi

echo 'Internet connection under testing...'
ping -c5 canvas.sydney.edu.au &> /dev/null
if [ "$?" == "0" ]; then
	echo "Connection seems valid";
	echo "Starting main program";
	sleep 3;
	python3 -u main.py
else
	echo "Cannot reach canvas.sydney.edu.au";
fi

