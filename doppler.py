#!/usr/bin/env python3

# TODO: Make logger output to stdout

from skyfield.api import Topos, load
from datetime import datetime, timedelta, UTC
from dateutil.parser import parse
import numpy as np
import argparse
import math

C = 299_792_458
NODE_NUMBER = 4032
TLE_FILE_PATH = "disco-test.tle"
CENTER_FREQ = 437

def get_range_rate(obs_lat, obs_lon, time, tle=TLE_FILE_PATH, time_offset=1):

    ts = load.timescale()

    if isinstance(time, str):
        time = parse(time)
    time = time.replace(tzinfo=UTC)
    time = ts.utc(time) if time is not None else ts.now()

    #print(f"OG time: {time.utc_strftime('%Y-%m-%d %H:%M:%S')}")

    if time_offset:
        time = time - timedelta(seconds=time_offset)

    #print(f"offset time: {time.utc_strftime('%Y-%m-%d %H:%M:%S')}")

    if isinstance(tle, str):
        sat = load.tle_file(tle)
        sat = sat[0] #its read as a len=1 list, this bypasses the list
    #else:
    #    stations_url = "http://celestrak.com/NORAD/elements/stations.txt"
    #    satellites = load.tle(stations_url)
    #    sat = satellites[sat_name]
    #print(sat)
    
    observer = Topos(obs_lat, obs_lon)

    relative = (sat - observer).at(time)

    relative_position = relative.position.km
    relative_velocity = relative.velocity.km_per_s

    range_rate = np.dot(relative_velocity, relative_position) / np.linalg.norm(relative_position)
    
    return range_rate, relative_velocity

def get_range_speed(relative_velocity) :
    return math.sqrt(relative_velocity[0]**2 + relative_velocity[1]**2 + relative_velocity[2]**2)

def get_tx_freq(range_rate, freq):
    return (1 + range_rate * 1e3 / C) * freq

def get_rx_freq(range_rate, freq):
    return (1 - range_rate * 1e3 / C) * freq

def write_to_csh(output_path, adjusted_tx_freq, adjusted_rx_freq):
    with open(output_path, "w") as f:
        f.write(
                f"node {NODE_NUMBER}\n"
                f"set rx_freq {adjusted_rx_freq}\n"
                f"set tx_freq {adjusted_tx_freq}\n"
                )
                
if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    #parser.add_argument("satname", help="TLE name of satellie e.g. ISS (ZARYA)")
    parser.add_argument("obs_lat", help="observer longitude (degrees)", type=float)
    parser.add_argument("obs_lon", help="observer longitude (degrees)", type=float)
    #parser.add_argument("freq", help="frequency in MHz to compute Doppler shift for", nargs="?", type=float)
    #parser.add_argument("-tle", help="Path to TLE file", type=str)
    parser.add_argument("-t", "--time", help="UTC time of observation (default: now)", nargs="?")
    parser.add_argument("-o", "--output", help="Path to output file", type=str)
    parser.add_argument("-d", "--offset", help="Offset in seconds", type=int)
    parser.add_argument("-q", "--quiet", help="No debug output", action=argparse.BooleanOptionalAction)
    args = parser.parse_args()

    range_rate, relative_velocity = get_range_rate(args.obs_lat, args.obs_lon, args.time, TLE_FILE_PATH ,args.offset)

    range_speed = get_range_speed(relative_velocity)

    adjusted_tx_freq = get_tx_freq(range_rate, CENTER_FREQ)
    adjusted_rx_freq = get_rx_freq(range_rate, CENTER_FREQ)

    write_to_csh(args.output, adjusted_tx_freq, adjusted_rx_freq)

    #print(f"quiet: {args.quiet}")
    if not args.quiet:
        print(f"time: {args.time}")
        print(f"TX freq: {adjusted_tx_freq}")
        print(f"RX freq: {adjusted_rx_freq}")
        print(f"output file: {args.output}")
