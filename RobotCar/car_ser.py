import time
import serial
import pygame

# setup serial communication with Arduino
ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1.0)
time.sleep(3)
ser.reset_input_buffer

# setup joystick control
pygame.joystick.init()
pygame.init()
controller = pygame.joystick.Joystick(0)
controller.init()

print("Pygame count:{}".format(pygame.joystick.get_count()))

last_time_check_fire = time.time()

axis1 = 0
axis2 = 0

while(True):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            break
        if event.type == pygame.JOYHATMOTION:
            print("Hat value {}".format(event.value))
            x = event.value[0]
            y = event.value[1]
            print("X: {}, Y: {}".format(x, y))
            if(x == -1):
                ser.write("L\n".encode('utf-8'))
            elif(x == 1):
                ser.write("R\n".encode('utf-8'))
            elif(y == -1):
                ser.write("B\n".encode('utf-8'))
            elif(y == 1):
                ser.write("F\n".encode('utf-8'))
            else:
                ser.write("S\n".encode('utf-8'))
        elif event.type == pygame.JOYAXISMOTION:
            # print("Axis: {}, Value: {:.2f}".format(event.axis, event.value))
            
            if event.axis == 0:
                axis1 = event.value                
            elif event.axis == 1:
                axis2 = event.value
            
            print("axis1: {}, axis2: {}".format(axis1, axis2))

            if axis1 < 0:
                ser.write("F\n".encode('utf-8'))
            elif axis1 > 0:
                ser.write("B\n".encode('utf-8'))
            elif axis2 < 0:
                ser.write("L\n".encode('utf-8'))
            elif axis2 > 0:
                ser.write("R\n".encode('utf-8'))
            else:
                ser.write("S\n".encode('utf-8'))