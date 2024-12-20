# import curses and GPIO
import RPi.GPIO as GPIO
import time
import math
import pygame

import os

os.environ["SDL_VIDEODRIVER"] = "dummy"  # fool the system to think it has a video
epsilon = 0.1

pygame.joystick.init()
pygame.init()
controller = pygame.joystick.Joystick(0)
controller.init()

print("Pygame count:{}".format(pygame.joystick.get_count()))


def motorOut(in1, in2, in3, in4):
    GPIO.output(5, in1)
    GPIO.output(7, in2)
    GPIO.output(13, in3)
    GPIO.output(11, in4)


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


# set GPIO numbering mode and define output pins
# 2 power sources
# power source 1: 5v for Raspberry Pi Zero board
# power source 2: 12v for motors, flashlight, sound
GPIO.setmode(GPIO.BOARD)
GPIO.setup(5, GPIO.OUT)  # Motor Left
GPIO.setup(7, GPIO.OUT)  # Motor Left
GPIO.setup(11, GPIO.OUT)  # Motor Right
GPIO.setup(13, GPIO.OUT)  # Motor Right
GPIO.setup(3, GPIO.OUT)  # Motor speed left
GPIO.setup(15, GPIO.OUT)  # Motor speed right

speedleft = GPIO.PWM(3, 100)
speedright = GPIO.PWM(15, 100)
speedleft.start(0)
speedright.start(0)

""" START MAIN PROGRAM LOOP """
axis1 = 0
axis2 = 0
reverseSpeedRatio = 1
turn_rate = math.pi * 1.4

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            break
        if event.type == pygame.JOYHATMOTION:
            speedleft.ChangeDutyCycle(100)
            speedright.ChangeDutyCycle(100)
            print("Hat value {}".format(event.value))
            x = event.value[0]
            y = event.value[1]
            print("X: {}, Y: {}".format(x, y))
            if x == -1:
                carMove("LEFT")
            elif x == 1:
                carMove("RIGHT")
            elif y == -1:
                carMove("DOWN")
            elif y == 1:
                carMove("UP")
            else:
                carMove("STOP")
        elif event.type == pygame.JOYAXISMOTION:
            print("Axis: {}, Value: {:.2f}".format(event.axis, event.value))

            if event.axis == 0:
                axis1 = event.value
            elif event.axis == 1:
                axis2 = event.value

            print("axis1: {}, axis2: {}".format(axis1, axis2))
            a = int(max(abs(axis1), abs(axis2)) * 100)
            b = 1
            if abs(axis2) >= epsilon:
                b = int(math.atan(abs(axis1) / abs(axis2)) / turn_rate * a)
            if axis2 > epsilon:
                if axis1 < 0 - epsilon:
                    outRight = a
                    outLeft = b
                elif axis1 > epsilon:
                    outLeft = a
                    outRight = b
                else:
                    outLeft = int(axis2 * 100)
                    outRight = outLeft

                print("outLeft: {:d}, outRight{:d}".format(outLeft, outRight))

                speedleft.ChangeDutyCycle(int(outLeft * reverseSpeedRatio))
                speedright.ChangeDutyCycle(int(outRight * reverseSpeedRatio))
                carMove("DOWN")
            elif axis2 < 0 - epsilon:
                if axis1 < 0 - epsilon:
                    outRight = a
                    outLeft = b
                elif axis1 > epsilon:
                    outLeft = a
                    outRight = b
                else:
                    outLeft = int(abs(axis2) * 100)
                    outRight = outLeft

                print("outLeft: {:d}, outRight{:d}".format(outLeft, outRight))

                speedleft.ChangeDutyCycle(outLeft)
                speedright.ChangeDutyCycle(outRight)
                carMove("UP")
            elif abs(axis2) <= epsilon:
                outRight = int(abs(axis1) * 100)
                outLeft = outRight
                speedleft.ChangeDutyCycle(outLeft)
                speedright.ChangeDutyCycle(outRight)

                if axis1 > epsilon:
                    carMove("LEFT")
                elif axis1 < 0 - epsilon:
                    carMove("RIGHT")
                else:
                    carMove("STOP")
