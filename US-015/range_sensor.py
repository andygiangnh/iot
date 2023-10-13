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

## DISTANCE SENSOR ##
### Sensor
exitFlag = False
distance = 200

def sensor():
    global exitFlag
    global distance

    print ("Distance Measurement In Progress")

    try:
        while True and not exitFlag:
            GPIO.output(TRIG, False)
            print ("Waiting For Sensor To Settle")
            time.sleep(2)
            
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
                ser.write("S".encode('utf-8'))
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
        
        ser.write("S".encode('utf-8'))
        time.sleep(1)
        ser.write("5".encode('utf-8'))
        time.sleep(1)

        while distance > 25:
            if(distance > 25):
                ser.write("F".encode('utf-8'))
                time.sleep(1.0)
                print("Sending F")
            ser.write("S".encode('utf-8'))
            print("Sending S")
            time.sleep(1.0)
        
        exitFlag = True
        time.sleep(2)
        # Start Pump
        print("Start pumping...")
        ser.write("W".encode('utf-8'))
        time.sleep(3)
        ser.write("w".encode('utf-8'))
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