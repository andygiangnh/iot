from motormodule import Motor
from joystickmodule import get_joystick


motor = Motor(3, 5, 7, 15, 11, 13)
while True:
    joystick = get_joystick()
    speed = joystick['hat1']
    turn = joystick['hat0']
    if joystick['axis1'] != 0:
        speed = joystick['axis1']
    if joystick['axis0'] != 0:
        turn = joystick['axis0']

    motor.move(speed, turn)

