#!/usr/bin/bash

# trigger the doppler.py script at an interval in seconds
# copy the result to input.csh for use by csh
# -q flag stops debug output of doppler.py
# uncomment line 21 for logging and montior with tail -f doppler.log

if [ -z "$1" ];
then
    my_delay=0.7
else
    my_delay=$1
fi
echo "Starting dopplerd with $my_delay s interval"
while true;
do
    my_time="$(date -uIs)"
    ./doppler.py 55.6167 12.65 -t $my_time -o tmp.csh -d 5 -q
    mv -f tmp.csh input.csh
    echo $my_time `cat input.csh` >> doppler.log
    sleep $my_delay
done

   
