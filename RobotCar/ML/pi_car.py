from motormodule import Motor
from joystickmodule import get_joystick
from record_csv import RecordCSV


motor = Motor(3, 5, 7, 15, 13, 11)
metrics = {'turn': 0.0, 'speed': 1.0}
recorder = RecordCSV(port='/dev/ttyUSB0')

while True:
    joystick = get_joystick()
    speed = 0 - joystick['hat1']
    turn = joystick['hat0']
    if joystick['axis1'] != 0:
        speed = joystick['axis1']
    if joystick['axis0'] != 0:
        turn = joystick['axis0']
    # print("speed: {}, turn: {}".format(speed, turn))
    if abs(speed) < 0.1 and abs(turn) < 0.1:
        motor.stop()
    else:
        motor.move(speed, turn, 0)

    metrics = {'turn': turn, 'speed': speed}

    if joystick['b'] == 1:
        recorder.start()
    elif joystick['a'] == 1:
        recorder.stop_record()
    elif joystick['x'] == 1:
        break

