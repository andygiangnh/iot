# import curses and GPIO
import curses
import RPi.GPIO as GPIO
import re
import time
import argparse
import threading
import os # adding so that we can shutdown PI

from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.virtual import viewport
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT, TINY_FONT, SINCLAIR_FONT, LCD_FONT

### for Led Matrix display ###
# create matrix device
serial = spi(port=0, device=0, gpio=noop())
device = max7219(serial, cascaded=1, block_orientation=0, rotate=0)
print("Created device")

def ledShow(msg):
    # start ledShow
    print(msg)
    show_message(device, msg, fill="white", font=proportional(LCD_FONT), scroll_delay=0.1)
    time.sleep(1)
###

def motorOut(in1, in2, in3, in4):
    GPIO.output(7, in1)
    GPIO.output(11, in2)
    GPIO.output(13, in3)
    GPIO.output(15, in4)

def carMove(direction, ledMatrix):
    if not ledMatrix.isAlive():
        ledMatrix = threading.Thread(target=ledShow, args=(direction,))
        ledMatrix.start()
    if direction == "UP":
        motorOut(False, True, False, True)
    elif direction == "DOWN":
        motorOut(True, False, True, False)
    elif direction == "LEFT":
        motorOut(False, True, True, False)
    elif direction == "RIGHT":
        motorOut(True, False, False, True)
    else:
        motorOut(False, False, False, False)

#set GPIO numbering mode and define output pins
# 2 power sources
# power source 1: 5v for Raspberry Pi Zero board
# power source 2: 12v for motors, flashlight, sound
GPIO.setmode(GPIO.BOARD)
GPIO.setup(7,GPIO.OUT)  # Motor Left
GPIO.setup(11,GPIO.OUT) # Motor Left
GPIO.setup(13,GPIO.OUT) # Motor Right
GPIO.setup(15,GPIO.OUT) # Motor Right
GPIO.setup(16,GPIO.OUT) # Light - turn left
GPIO.setup(18,GPIO.OUT) # Light - turn right
GPIO.setup(29,GPIO.OUT) # Light - flash (12v) - same power source with motors
GPIO.setup(31,GPIO.OUT) # Sound
GPIO.setup(32,GPIO.IN) # Sound

# Get the curses window, turn off echoing of keyboard to screen, turn on
# instant (no waiting) key response, and use special values for cursor keys
screen = curses.initscr()
curses.noecho()
curses.cbreak()
screen.keypad(True)

### Sensor
exitFlag = False
isBlocked = False

def sensor():
    while True:
        if GPIO.input(32) == 0:
            if not isBlocked:
                print("Obstacle detected!")
                carMove("STOP", ledMatrix)
            GPIO.output(31,False)
            isBlocked = True
        elif GPIO.input(32) == 1:
            isBlocked = False
            GPIO.output(31,True)

        if exitFlag:
            print("exit Sensor")
            time.sleep(1)
            break

sensorThread = threading.Thread(target=sensor)
sensorThread.start()

###

### START MAIN PROGRAM LOOP ###

try:
    ledMatrix = threading.Thread(target=ledShow, args=("READY!",))
    ledMatrix.start()
    time.sleep(2)
    while True:
        char = screen.getch()
        if char == ord('q'):
            exitFlag = True
            break
        elif char == ord('S'):
            time.sleep(3)
            ledMatrix = threading.Thread(target=ledShow, args=("SHUTDOWN!",))
            ledMatrix.start()
            os.system('sudo shutdown now')
        elif char == ord('a'):
            ledShow("Khanh An")
        elif char == ord('s'):
            ledShow("Suri")
        elif char == ord('l') or char == ord('L'):
            GPIO.output(29,True)
        elif char == ord('o') or char == ord('O'):
            GPIO.output(29,False)
        elif char == ord('k') or char == ord('K'):
            GPIO.output(31,False)
        elif char == ord('i') or char == ord('I'):
            GPIO.output(31,True)
        elif char == curses.KEY_UP:
            if GPIO.input(32) == 1:
                carMove("UP", ledMatrix)
            # Lights
            GPIO.output(16,False)
            GPIO.output(18,False)
        elif char == curses.KEY_DOWN:
            carMove("DOWN", ledMatrix)
            # Lights
            GPIO.output(16,False)
            GPIO.output(18,False)
        elif char == curses.KEY_RIGHT:
            carMove("RIGHT", ledMatrix)
            # Lights
            GPIO.output(16,True)
            GPIO.output(18,False)
        elif char == curses.KEY_LEFT:
            carMove("LEFT", ledMatrix)
            # Lights
            GPIO.output(16,False)
            GPIO.output(18,True)
        elif char == 10: # Enter key pressed
            carMove("STOP", ledMatrix)
            # Lights
            GPIO.output(16,False)
            GPIO.output(18,False)
finally:
    #Close down curses properly, inc turn echo back on!
    sensorThread.join()
    curses.nocbreak()
    screen.keypad(0)
    curses.echo()
    curses.endwin()
    GPIO.cleanup()

