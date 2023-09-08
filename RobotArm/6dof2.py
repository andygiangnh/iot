#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Libraries
import time    #https://docs.python.org/fr/3/library/time.html
from adafruit_servokit import ServoKit    #https://circuitpython.readthedocs.io/projects/servokit/en/latest/
import curses

screen = curses.initscr()
curses.noecho()
curses.cbreak()
screen.keypad(True)
class Servo:

    #Parameters
    MIN_IMP = 500
    MAX_IMP = 2500
    
    def __init__(self, index, lower, zero, max):
        self.index = index
        self.lower = lower
        self.zero = zero
        self.current = zero
        self.max = max
    
    def decrease(self):
        if self.current > self.lower:
            self.current -= 1
            pca.servo[self.index].angle = self.current
            time.sleep(0.02)

    def increase(self):
        if self.current < self.max:
            self.current += 1
            pca.servo[self.index].angle = self.current
            time.sleep(0.02)

#Objects
pca = ServoKit(channels=16)
servos = []

# function init 
def init():

    servos.append(Servo(0, 0, 90, 180))
    servos.append(Servo(1, 20, 40, 120))
    servos.append(Servo(2, 60, 90, 120))
    servos.append(Servo(3, 0, 90, 120))

    servos.append(Servo(8, 0, 90, 180))
    servos.append(Servo(9, 50, 70, 120))

    for i in range(0, len(servos),1):
        pca.servo[servos[i].index].set_pulse_width_range(Servo.MIN_IMP , Servo.MAX_IMP)


# function main 
def main():

    # pcaScenario();
    try:
        while True:
            char = screen.getch()
            if char == ord('q'):
                break
            elif char == curses.KEY_UP:
                servos[1].increase()
            elif char == curses.KEY_DOWN:
                servos[1].decrease()
            elif char == curses.KEY_LEFT:
                servos[0].increase()
            elif char == curses.KEY_RIGHT:
                servos[0].decrease()
            elif char == ord('w') or char == ord('W'):
                servos[5].increase()
            elif char == ord('x') or char == ord('X'):
                servos[5].decrease()
            elif char == ord('a') or char == ord('A'):
                servos[4].increase()
            elif char == ord('d') or char == ord('D'):
                servos[4].decrease()
            elif char == ord('n') or char == ord('n'):
                servos[3].increase()
            elif char == ord('y') or char == ord('Y'):
                servos[3].decrease()
            elif char == ord('g') or char == ord('G'):
                servos[2].decrease()
            elif char == ord('j') or char == ord('J'):
                servos[2].increase()

    finally:
        curses.nocbreak()
        screen.keypad(0)
        curses.echo()
        curses.endwin()

# function pcaScenario 
def pcaScenario():
    """Scenario to test servo"""
    for i in range(0, len(servos),1):
        for j in range(servos[i].zero, servos[i].max,1):
            print("Send angle {} to Servo {}".format(j,i))
            pca.servo[servos[i].index].angle = j
            time.sleep(0.02)
        for j in range(servos[i].max,servos[i].lower,-1):
            print("Send angle {} to Servo {}".format(j,i))
            pca.servo[servos[i].index].angle = j
            time.sleep(0.02)
        for j in range(servos[i].lower,servos[i].zero,1):
            print("Send angle {} to Servo {}".format(j,i))
            pca.servo[servos[i].index].angle = j
            time.sleep(0.02)


if __name__ == '__main__':
    init()
    main()