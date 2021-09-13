# import curses and GPIO
import curses
import RPi.GPIO as GPIO
import re
import time
import argparse
import threading
import os # adding so that we can shutdown PI

def motorOut(in1, in2, in3, in4):
    GPIO.output(7, in1)
    GPIO.output(11, in2)
    GPIO.output(13, in3)
    GPIO.output(15, in4)

def carMove(direction):
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
GPIO.setup(29,GPIO.OUT) # Light - flash (12v) - same power source with motors
GPIO.setup(31,GPIO.OUT) # Sound
GPIO.setup(32,GPIO.IN)  # Sensor
GPIO.setup(33,GPIO.OUT) # Motor speed left
GPIO.setup(35,GPIO.OUT) # Motor speed right

speedleft  = GPIO.PWM(33, 100)
speedright = GPIO.PWM(35, 100)
speedleft.start(100)
speedright.start(100)

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
                carMove("STOP")
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
    while True:
        char = screen.getch()
        if char == ord('q'):
            exitFlag = True
            break
        elif char == ord('S'):
            time.sleep(3)
            os.system('sudo shutdown now')
        elif char == ord('l') or char == ord('L'):
            GPIO.output(29,True)
        elif char == ord('o') or char == ord('O'):
            GPIO.output(29,False)
        elif char == ord('k') or char == ord('K'):
            GPIO.output(31,False)
        elif char == ord('i') or char == ord('I'):
            GPIO.output(31,True)
        elif char == ord('1'):
            speedleft.ChangeDutyCycle(20)
            speedright.ChangeDutyCycle(20)
        elif char == ord('2'):
            speedleft.ChangeDutyCycle(66)
            speedright.ChangeDutyCycle(66)
        elif char == ord('3'):
            speedleft.ChangeDutyCycle(100)
            speedright.ChangeDutyCycle(100)
        elif char == curses.KEY_UP:
            if GPIO.input(32) == 1:
                carMove("UP")
        elif char == curses.KEY_DOWN:
            carMove("DOWN")
        elif char == curses.KEY_RIGHT:
            carMove("RIGHT")
        elif char == curses.KEY_LEFT:
            carMove("LEFT")
        elif char == 10: # Enter key pressed
            carMove("STOP")
finally:
    #Close down curses properly, inc turn echo back on!
    sensorThread.join()
    curses.nocbreak()
    screen.keypad(0)
    curses.echo()
    curses.endwin()
    GPIO.cleanup()

