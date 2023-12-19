# -*- encoding: utf-8 -*-
from flask import Flask
import serial
import time

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
TRIG = 23
ECHO = 24
cam_light = 17

GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)
GPIO.setup(cam_light,GPIO.OUT)

from flask_cors import CORS, cross_origin
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

ser = None

@app.route("/")
def home():
    global ser
    if(ser == None or ser.isOpen() == False):
        ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1.0)
        time.sleep(3)
        ser.reset_input_buffer
    return "Serial connected"

@app.route("/close")
def closeSer():
    global ser
    if(ser != None and ser.isOpen()):
        ser.close()
    return "Serial closed"


@app.route("/move/<string:direction>")
def move(direction):
    global ser
    if(ser != None and ser.isOpen()):
        ser.write(direction.encode('utf-8'))
    return "Move {}".format(direction)
    
def read_sensor():
    global TRIG
    global ECHO
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(TRIG,GPIO.OUT)
    GPIO.setup(ECHO,GPIO.IN)
    GPIO.output(TRIG, False)
    print ("Waiting For Sensor To Settle")
    time.sleep(2)
    distance = 200

    while True:
        GPIO.output(TRIG, False)
        print ("Waiting For Sensor To Settle")
        time.sleep(1)

        GPIO.output(TRIG, True)
        time.sleep(0.00001)
        GPIO.output(TRIG, False)
        
        while GPIO.input(ECHO)==0:
            pulse_start = time.time()
        
        while GPIO.input(ECHO)==1:
            pulse_end = time.time()
        
        pulse_duration = pulse_end - pulse_start        
        distance = pulse_duration * 17150        
        distance = round(distance, 2)
        if(distance <= 25):
            ser.write("S\n".encode('utf-8'))
            time.sleep(1)
            break

        print ("Distance: {} cm".format(distance))
    return distance

@app.route("/sound_off")
def sound_off():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(cam_light,GPIO.OUT)
    GPIO.output(cam_light, False)
    return 'Sound off'

@app.route("/fire_action")
def fire_action():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(cam_light,GPIO.OUT)
    last_time_check_fire = time.time()
    reset_fire_check = 10.0
    fire_cmd = ''
    try:
        """
        ser.write("S\n".encode('utf-8'))
        time.sleep(1)
        ser.write("6\n".encode('utf-8'))
        time.sleep(1)
        """
        count = 0
        while True:
            # action 1
            time_now = time.time()
            if time_now - last_time_check_fire >= reset_fire_check:
                last_time_check_fire = time_now
                print("Send Arduino Raspberry Pi is working on Fire")
                ser.write("wip\n".encode('utf-8'))
            # action 2
            if ser.in_waiting > 0:
                fire_cmd = ser.readline().decode('utf-8').rstrip()

            if(fire_cmd == "fire_on"):
                print("Received Fire Start Moving: " + str(fire_cmd))
                break
            
            if(fire_cmd == "fire_off"):
                GPIO.output(cam_light, False)
                print("Received Fire Start Moving: " + str(fire_cmd))
                fire_cmd = ''
            
            if(count >= 20):
                break
            
            time.sleep(1)
            
        """
        distance = read_sensor()
        while distance > 25:
            if(distance > 25):
                ser.write("F\n".encode('utf-8'))
                time.sleep(1.0)
                print("Sending F")
            ser.write("S\n".encode('utf-8'))
            print("Sending S")
            time.sleep(1.0)
        
        exitFlag = True
        """
        print("Start pumping...")
        ser.write("W\n".encode('utf-8'))
        time.sleep(1)
        GPIO.output(cam_light, True)
        #print("light on")
   
        time.sleep(1)
        # Start Pump
        print("Start pumping...")
        ser.write("W\n".encode('utf-8'))
        time.sleep(4)
        ser.write("w\n".encode('utf-8'))
        time.sleep(2)
        
        GPIO.output(cam_light, False)
        #print("light off")
        fire_cmd = ''
        
        return 'Done processing fire'
            
    except KeyboardInterrupt: # If there is a KeyboardInterrupt (when you press ctrl+c), exit the program
        pass
    finally:
        print("Cleaning up!")
        GPIO.cleanup()
        time.sleep(1)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
