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


class RecordCSV:
    def __init__(self, port=PORT_NAME, path='out.txt', stop_flag=False, metrics=None):
        self.outfile = None
        self.lidar = None
        self.port = port
        self.path = path
        self.stop_flag = stop_flag
        self.metrics = metrics
        if self.metrics is None:
            self.metrics = {'turn': 0.0, 'speed': 0.0}
        self.lidar = RPLidar(self.port)

    def start(self):
        self.outfile = open(self.path, 'w')

    def record_line(self):
        """
        return a frame scan of 360 data points
        """
        try:
            print('Recording measurements into csv format... Press Crl+C to stop.')
            skip = True  # skip the ongoing scanning data point of current frame
            line = ''
            arr = np.empty(LIDAR_RESOLUTION, dtype=object)
            self.lidar.clean_input()
            for measurement in self.lidar.iter_measures():
                if self.stop_flag:
                    break
                if measurement[0]:
                    line = ''
                    if not skip:
                        for v in arr:
                            line += str(nvl(v, 0)) + ','
                        line += "{:.2f}".format(self.metrics['turn']) + '\n'
                        print(line)
                        self.outfile.write(line)
                        break

                    skip = False
                    arr = np.empty(LIDAR_RESOLUTION, dtype=object)
                elif not skip:
                    arr[min(round(measurement[2]), 359)] = measurement[3]

        except KeyboardInterrupt:
            print('Stopping.')
        finally:
            self.stop_flag = False

    def stop_record(self):
        """
        stop recording and write to csv file
        """
        self.stop_flag = True
        self.lidar.stop()
        self.lidar.disconnect()
        self.outfile.close()


if __name__ == '__main__':
    recorder = RecordCSV(port='COM6')
    recorder.start()
    recorder.record_line()
    recorder.stop_record()
