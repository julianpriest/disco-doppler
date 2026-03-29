# Disco Doppler Frequency Shift

This script generates a small csh output file `tmp.csh` that can then be run from within csh to set radio tx and rx frequency doppler correction.
It can be configured with an external TLE file, time in UTC, lat and lon location of observer. A time offset can be added in case of inaccurate TLE.

A simple trigger script is provided which handles creation of an input file for non blocking reads, as well as logging.

## Install

Requires [Skyfield](https://rhodesmill.org/skyfield/)

## Example of command

`./doppler.py 55.6167 12.65 -t 2026-03-25T14:13:32 -o tmp.csh -d 5`
```
usage: doppler.py [-h] [-t [TIME]] [-o OUTPUT] [-d OFFSET] [-q | --quiet | --no-quiet]
                  obs_lat obs_lon

positional arguments:
  obs_lat               observer longitude (degrees)
  obs_lon               observer longitude (degrees)

options:
  -h, --help            show this help message and exit
  -t [TIME], --time [TIME]
                        UTC time of observation (default: now)
  -o OUTPUT, --output OUTPUT
                        Path to output file
  -d OFFSET, --offset OFFSET
                        Offset in seconds
  -q, --quiet, --no-quiet
                        No debug output
```

## Trigger

`./dopplerd.sh -i 2 -d 0 -l`

```
Usage: ./dopplerd.sh [-l] log [-i] interval [-d] offset delta [-h] help
[ctrl-c] quit, tail -f doppler.log to monitor
frequencies output to input.csh
every [interval] s, with offset [delta] s
```
