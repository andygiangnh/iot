#!/usr/bin/env python3
"""Records measurements to a given file in csv format. Usage example:

$ ./record_csv.py out.txt"""
import sys
from rplidar import RPLidar
import numpy as np
from threading import Thread

PORT_NAME = '/dev/ttyUSB0'
# constant based on lidar resolution
LIDAR_RESOLUTION = 360


def nvl(value, default):
    return value if value is not None else default


class RecordCSV(Thread):
    def __init__(self, port=PORT_NAME, path='out.txt', stop_flag=False, metrics=None):
        Thread.__init__(self)
        self.port = port
        self.path = path
        self.stop_flag = stop_flag
        self.metrics = metrics

    def run(self):
        """Main function"""
        if self.metrics is None:
            self.metrics = {'turn': 0.0, 'speed': 1.0}
        lidar = RPLidar(self.port)
        outfile = open(self.path, 'w')

        try:
            print('Recording measurements into csv format... Press Crl+C to stop.')
            skip = True
            count = 0
            line = ''
            arr = np.empty(LIDAR_RESOLUTION, dtype=object)
            for measurement in lidar.iter_measures():
                if self.stop_flag:
                    break
                if measurement[0]:
                    line = ''
                    if not skip:
                        for v in arr:
                            line += str(nvl(v, 0)) + ','
                        line += "{:.2f}".format(self.metrics['turn']) + '\n'
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

    def stop_record(self):
        self.stop_flag = True


if __name__ == '__main__':
    recorder = RecordCSV(port='COM6')
    recorder.start()

