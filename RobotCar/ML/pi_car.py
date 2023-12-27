from motormodule import Motor
from joystickmodule import get_joystick


motor = Motor(3, 5, 7, 15, 13, 11)
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

    if joystick['x'] == 1:
        break

