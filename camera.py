from picamera import PiCamera
import time

camera = PiCamera()
camera.resolution = (1280,720)
camera.framerate = (25)

time.sleep(1)

camera.start_recording('/home/pi/Videos/vid_test.mjpg')
time.sleep(5)
camera.stop_recording()