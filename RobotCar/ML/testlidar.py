import time

from rplidar import RPLidar, _process_scan

lidar = RPLidar('COM6')

lidar.connect()
lidar.start_motor()
lidar.start()

for i in range(10):
    time.sleep(1)
    print('counter {}'.format(i))
    new_scan = False
    while not new_scan:
        raw = lidar._read_response(5)
        new_scan, quality, angle, distance = _process_scan(raw)
        print('new scan:{}, angle: {}, distance: {} '.format(new_scan, angle, distance))
        if new_scan:
            print('new scan {}'.format(i))

lidar.reset()
lidar.stop()
lidar.stop_motor()
lidar.disconnect()
