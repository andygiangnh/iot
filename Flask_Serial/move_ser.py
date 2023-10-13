from flask import Flask
import serial
import time

app = Flask(__name__)

ser = None

@app.get("/")
def home():
    global ser
    if(ser == None or ser.isOpen() == False):
        ser = serial.Serial('COM11', 115200)
        time.sleep(3)
        ser.reset_input_buffer
    return "Serial connected"

@app.get("/close")
def closeSer():
    global ser
    if(ser != None and ser.isOpen()):
        ser.close()
    return "Serial closed"


@app.get("/move/<string:direction>")
def move(direction):
    global ser
    if(ser != None and ser.isOpen()):
        ser.write(direction.encode('utf-8'))
    return "Move {}".format(direction)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)