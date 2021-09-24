""" Raspberry Pi Python Code for QTR-1RC IR Sensor
    by tobyonline copyleft 2016 robot-resource.blogspot.com http://tobyonline.co.uk """

import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

IRPIN = 15 #assumes you've connected the IR Out wire to GPIO4
ENPIN = 14

def irsensor1(): #function to get value from IR sensor
    GPIO.setup(ENPIN, GPIO.OUT) #Set your chosen pin to an output
    GPIO.output(ENPIN, GPIO.HIGH) #turn on the power 5v to the sensor
    print(GPIO.output)

    GPIO.setup(IRPIN, GPIO.OUT) #Set your chosen pin to an output
    GPIO.output(IRPIN, GPIO.HIGH) #turn on the power 5v to the sensor
    time.sleep(0.01) #charge the tiny capacitor on the sensor for 0.1sec
    pulse_start = time.time() #start the stopwatch
    GPIO.setup(IRPIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # set pin to pull down to ground 0v
    while GPIO.input(IRPIN)> 0:
        pass #wait while the capacitor discharges to zero
    if  GPIO.input(IRPIN)==0:
        pulse_end = time.time() #when it hits zero stop the stopwatch
    pulse_duration = pulse_end - pulse_start
    print("duration:", pulse_duration) #print the time so you can adjust sensitivity
    if pulse_duration > 0.0006: #adjust this value to change the sensitivity
        colour_seen = "black"
    else:
        colour_seen = "white"
    return colour_seen

while True:
    colour_seen = irsensor1() #call the function and get the output colour_seen
    print(colour_seen)
    time.sleep(1) #pause for 1 second before repeating, use ctrl+z to stop

GPIO.cleanup() #always good practice to clean-up the GPIO settings at the end :) tobyonline