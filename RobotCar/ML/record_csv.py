#!/usr/bin/env python3
"""Records measurements to a given file in csv format. Usage example:

$ ./record_csv.py out.txt"""
import sys
from rplidar import RPLidar
import numpy as np

PORT_NAME = '/dev/ttyUSB0'
# constant based on lidar resolution
LIDAR_RESOLUTION = 360


def nvl(value, default):
    return value if value is not None else default


stop_flag = False


def stop_record():
    global stop_flag
    stop_flag = True


def start_record(path='out.txt', metrics=None):
    global stop_flag
    """Main function"""
    if metrics is None:
        metrics = {'turn': 0.0, 'speed': 1.0}
    lidar = RPLidar(PORT_NAME)
    outfile = open(path, 'w')

    try:
        print('Recording measurements into csv format... Press Crl+C to stop.')
        skip = True
        count = 0
        line = ''
        arr = np.empty(LIDAR_RESOLUTION, dtype=object)
        for measurement in lidar.iter_measures():
            if stop_flag:
                break
            if measurement[0]:
                line = ''
                if not skip:
                    for v in arr:
                        line += str(nvl(v, 0)) + ','
                    line += "{:.2f}".format(metrics['turn']) + '\n'
                    print(line)
                    outfile.write(line)

                skip = False
                count = 0
                arr = np.empty(LIDAR_RESOLUTION, dtype=object)
            elif not skip:
                arr[min(round(measurement[2]), 359)] = measurement[3]
                count += 1

    except KeyboardInterrupt:
        print('Stopping.')
    finally:
        lidar.stop()
        lidar.disconnect()
        outfile.close()
        stop_flag = False


if __name__ == '__main__':
    start_record(sys.argv[1])
