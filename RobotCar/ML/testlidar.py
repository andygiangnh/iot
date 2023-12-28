import time

from rplidar import RPLidar, _process_scan

lidar = RPLidar('COM6')

lidar.connect()
lidar.motor_speed = 300
lidar.start_motor()


for i in range(10):
    print('counter {}'.format(i))
    """
    method single_measure will start scanning process if it not started
    """
    print(lidar.scanning)  # lidar is actively scanning
    print(lidar.read_single_measure())

    # increase the time will result in more data in the serial buffer
    time.sleep(0.05)


lidar.stop()
print(lidar.scanning)
lidar.disconnect()
print('Done')
