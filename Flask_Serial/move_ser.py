from flask import Flask
import serial
import time
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

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
