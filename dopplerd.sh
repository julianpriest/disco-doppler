#!/usr/bin/bash

# trigger the doppler.py script at an interval in seconds
# copy the result to input.csh for use by csh
# -q flag stops debug output of doppler.py

usage()
{
    echo "Usage: $0 [-l] log [-i] interval [-d] offset delta [-h] help"
    echo "[ctrl-c] quit, tail -f doppler.log to monitor"
    echo "frequencies output to input.csh"
    echo "every [interval] s, with offset [delta] s"
    exit 1
}
# defaults
my_log=0
my_interval=0.7
my_delta=0

while getopts "li:d:h" opt;
do
    case $opt in
	l) my_log=1; echo "Logging enabled"; echo $my_log;;
	i) my_interval=$OPTARG; echo "Interval: $my_interval";;
	d) my_delta=$OPTARG; echo "Delta offset: $my_delta";;
	h) usage;;
	:) echo "#Option -$OPTARG requires an argument." >&2;;
    esac
done

echo "Starting dopplerd with $my_interval s interval and offset $my_delta"

while true;
do
    my_time="$(date -uIs)"
    ./doppler.py 55.6167 12.65 -t $my_time -o tmp.csh -d $my_delta
    mv -f tmp.csh input.csh
    if [ $my_log -eq 1 ];
    then
       echo $my_time `cat input.csh` >> doppler.log
    fi
    sleep $my_interval
done

   
