#!/usr/bin/env python3
import serial
import time

ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1.0)
time.sleep(3)
ser.reset_input_buffer()
print("Serial OK.")

try:
    while True:
        user_input = input("Command: ")
        if user_input in ['L', 'R', 'F', 'B','S']:
            print("Send command to Arduino: " + user_input)
            str_to_send = user_input + "\n"
            ser.write(str_to_send.encode('utf-8'))
        elif user_input == 'Q':
            break
except KeyboardInterrupt:
    print("Close serial communication.")
    ser.close()
    