#!/usr/bin/env python3
"""Records measurements to a given file in csv format. Usage example:

$ ./record_csv.py out.txt"""
import sys
from rplidar import RPLidar, _process_scan
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
        self.lidar.get_info()

    def start(self):
        self.outfile = open(self.path, 'w')
        self.lidar.connect()
        self.lidar.start_motor()
        self.lidar.start()

    def record_line(self):
        """
        return a frame scan of 360 data points
        """
        print('Recording')
        line = ''
        arr = np.empty(LIDAR_RESOLUTION, dtype=object)
        try:
            new_scan = False
            skip = True  # skip the ongoing scanning data point of current frame
            count = 0
            while True:
                if new_scan and count > 1:
                    line = ''
                    if not skip:
                        for v in arr:
                            line += str(nvl(v, 0)) + ','
                        line += "{:.2f}".format(self.metrics['turn']) + '\n'
                        # print(line)
                        self.outfile.write(line)
                    break
                #  Read value from serial
                raw = self.lidar._read_response(5)
                new_scan, quality, angle, distance = _process_scan(raw)
                # print('new scan:{}, angle: {}, distance: {} '.format(new_scan, angle, distance))
                if new_scan:
                    count += 1
                    skip = False
                    print('new scan {}'.format(i))
                if count == 1 and not skip:
                    arr[min(round(angle), 359)] = distance

        except KeyboardInterrupt:
            print('Stopping.')
        finally:
            self.stop_flag = False
        return line

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
    for i in range(10):
        recorder.record_line()
    recorder.stop_record()
