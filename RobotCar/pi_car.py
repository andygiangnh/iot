# import curses and GPIO
import RPi.GPIO as GPIO
import time
import math
import pygame

pygame.joystick.init()
pygame.init()
controller = pygame.joystick.Joystick(0)
controller.init()

print("Pygame count:{}".format(pygame.joystick.get_count()))

def motorOut(in1, in2, in3, in4):
    GPIO.output(5, in1)
    GPIO.output(7, in2)
    GPIO.output(11, in3)
    GPIO.output(13, in4)

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
GPIO.setup(5,GPIO.OUT)  # Motor Left
GPIO.setup(7,GPIO.OUT) # Motor Left
GPIO.setup(11,GPIO.OUT) # Motor Right
GPIO.setup(13,GPIO.OUT) # Motor Right
GPIO.setup(3,GPIO.OUT) # Motor speed left
GPIO.setup(15,GPIO.OUT) # Motor speed right

speedleft  = GPIO.PWM(3, 100)
speedright = GPIO.PWM(15, 100)
speedleft.start(10)
speedright.start(10)

### START MAIN PROGRAM LOOP ###
axis1 = 0
axis2 = 0
reverseSpeedRatio = 1.0

while(True):
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
            if(x == -1):
                carMove("RIGHT")
            elif(x == 1):
                carMove("LEFT")
            elif(y == -1):
                carMove("DOWN")
            elif(y == 1):
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
            
            if axis2 > 0:
                if axis1 < 0:
                    outRight = int(max(abs(axis1), axis2) * 100)
                    outLeft = int(math.atan(abs(axis1)/axis2) / (math.pi) * outRight)
                elif axis1 > 0:
                    outLeft = int(max(axis1, axis2) * 100)
                    outRight = int(math.atan(axis1/axis2) / (math.pi) * outLeft)
                else:
                    outLeft = int(axis2 * 100)
                    outRight = outLeft
                
                print("outLeft: {:d}, outRight{:d}".format(outLeft, outRight))

                speedleft.ChangeDutyCycle(int(outLeft * reverseSpeedRatio))
                speedright.ChangeDutyCycle(int(outRight * reverseSpeedRatio))                
                carMove("DOWN")
            elif axis2 < 0:
                if axis1 < 0:
                    outRight = int(max(abs(axis1), abs(axis2)) * 100)
                    outLeft = int(math.atan(abs(axis1)/abs(axis2)) / (math.pi) * outRight)
                elif axis1 > 0:
                    outLeft = int(max(axis1, abs(axis2)) * 100)
                    outRight = int(math.atan(axis1/abs(axis2)) / (math.pi) * outLeft)
                else:
                    outLeft = int(abs(axis2) * 100)
                    outRight = outLeft
                
                print("outLeft: {:d}, outRight{:d}".format(outLeft, outRight))

                speedleft.ChangeDutyCycle(outLeft)
                speedright.ChangeDutyCycle(outRight)                
                carMove("UP")
            elif axis2 == 0:
                outRight = int(abs(axis1) * 100)
                outLeft = outRight
                speedleft.ChangeDutyCycle(outLeft)
                speedright.ChangeDutyCycle(outRight)
                
                if axis1 > 0:
                    carMove("LEFT")
                elif axis1 < 0:
                    carMove("RIGHT")
                else:
                    carMove("STOP")
