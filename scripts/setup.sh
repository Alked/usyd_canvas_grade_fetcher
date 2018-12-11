#!/bin/bash

if command -v python3 >/dev/null 2>&1; then
	echo 'Python3.x has been installed...'
else
	echo 'FATAL: Python3.x is not installed.'
	echo 'Please install Python3.x first via python.org'
	sleep 2
	echo 'Script terminated'
	exit
fi

echo 'Internet connection under testing...'
ping -c5 13.237.119.117:443 &> /dev/null
if [ "$?" == "0" ]; then
	echo "Connection seems valid..."
	sleep 1
	echo "Starting main program..."
	sleep 3
	python3 -u main.py
else
	echo "Cannot reach canvas.sydney.edu.au";
	echo "Please check Internet connection."
fi

