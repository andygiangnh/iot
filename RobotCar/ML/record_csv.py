#!/usr/bin/env python3
'''Records measurments to a given file in csv format. Usage example:

$ ./record_measurments.py out.txt'''
import sys
from rplidar import RPLidar
import numpy as np


PORT_NAME = '/dev/ttyUSB0'

def nvl(value, default):
    return value if value is not None else default

def run(path):
    '''Main function'''
    lidar = RPLidar(PORT_NAME)
    outfile = open(path, 'w')
    MAX_MEASUREMENT = 360

    try:
        print('Recording measurments... Press Crl+C to stop.')
        skip = True
        count = 0
        line = ''
        arr = np.empty(MAX_MEASUREMENT, dtype=object)
        for measurment in lidar.iter_measures():
            if measurment[0] == True:
                line = ''
                if not skip:
                    for v in arr:
                        line += str(nvl(v,0)) + ','
                    print(line[:-1] + '\n')
                    outfile.write(line[:-1] + '\n')
                
                skip = False
                count = 0                
                arr = np.empty(MAX_MEASUREMENT, dtype=object)
            elif not skip:
                arr[min(round(measurment[2]),359)] = measurment[3]
                count += 1            
            
    except KeyboardInterrupt:
        print('Stoping.')
    lidar.stop()
    lidar.disconnect()
    outfile.close()

if __name__ == '__main__':
    run(sys.argv[1])
