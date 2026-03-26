#!/usr/bin/bash

# trigger the doppler.py script at an interval in seconds
# copy the result to input.csh for use by csh
# -q flag stops debug output of doppler.py

usage()
{
    echo "Usage: $0 [-l] log [-d] delay [-h] help"
    echo "[ctrl-c] quit, tail -f doppler.log to monitor"
    echo "frequencies output to input.csh every [delay] s"
    exit 1
}

# defaults
my_log=0
my_delay=0.7

while getopts "ld:h" opt;
do
    case $opt in
	l) my_log=1; echo "Logging enabled"; echo $my_log;;
	d) my_delay=$OPTARG; echo "Delay: $my_delay";;
	h) usage;;
	:) echo "#Option -$OPTARG requires an argument." >&2;;
    esac
done

echo "Starting dopplerd with $my_delay s interval"

while true;
do
    my_time="$(date -uIs)"
    ./doppler.py 55.6167 12.65 -t $my_time -o tmp.csh -d 5 -q
    mv -f tmp.csh input.csh
    if [ $my_log -eq 1 ];
    then
       echo $my_time `cat input.csh` >> doppler.log
    fi
    sleep $my_delay
done

   
