import RPi.GPIO as GPIO
import time
import serial
import threading
GPIO.setmode(GPIO.BCM)

TRIG = 23
ECHO = 24

GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)

ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1.0)
time.sleep(3)
ser.reset_input_buffer

last_time_check_fire = time.time()
reset_fire_check = 10.0

## DISTANCE SENSOR ##
### Sensor
exitFlag = False
distance = 200

def sensor():
    global exitFlag
    global distance

    print ("Distance Measurement In Progress")

    try:
        GPIO.output(TRIG, False)
        print ("Waiting For Sensor To Settle")
        time.sleep(2)

        while True and not exitFlag:
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

            print ("Distance: {} cm".format(distance))
    except:
        pass

## START main ##
def main():
    try:
        global distance
        global ser
        global exitFlag

        global last_time_check_fire
        global reset_fire_check
        
        ser.write("S\n".encode('utf-8'))
        time.sleep(1)
        ser.write("6\n".encode('utf-8'))
        time.sleep(1)

        while True:
            # action 1
            time_now = time.time()
            if time_now - last_time_check_fire >= reset_fire_check:
                last_time_check_fire = time_now
                print("Send Arduino Raspberry Pi is working on Fire")
                ser.write("working_on_fire_out\n".encode('utf-8'))
            # action 2
            if ser.in_waiting > 0:
                fire_cmd = ser.readline().decode('utf-8').rstrip()
                if(fire_cmd == "fire_start"):
                    print("Received Fire Start Moving: " + str(fire_cmd))
                    break
            time.sleep(2)

        while distance > 25:
            if(distance > 25):
                ser.write("F\n".encode('utf-8'))
                time.sleep(1.0)
                print("Sending F")
            ser.write("S\n".encode('utf-8'))
            print("Sending S")
            time.sleep(1.0)
        
        exitFlag = True
        time.sleep(2)
        # Start Pump
        print("Start pumping...")
        ser.write("W\n".encode('utf-8'))
        time.sleep(3)
        ser.write("w\n".encode('utf-8'))
        time.sleep(2)
            
    except KeyboardInterrupt: # If there is a KeyboardInterrupt (when you press ctrl+c), exit the program
        pass
    finally:
        print("Cleaning up!")
        exitFlag = True
        sensorThread.join()
        GPIO.cleanup()
        ser.close()
        time.sleep(2)

if __name__ == '__main__':
    sensorThread = threading.Thread(target=sensor)
    sensorThread.start()
    main()