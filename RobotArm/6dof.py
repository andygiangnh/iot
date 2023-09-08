#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Libraries
import time    #https://docs.python.org/fr/3/library/time.html
from adafruit_servokit import ServoKit    #https://circuitpython.readthedocs.io/projects/servokit/en/latest/

#Constants
nbPCAServo=10

#Parameters
MIN_IMP  =[500, 500, 500, 500, 500, 500, 500, 500, 500, 500]
MAX_IMP  =[2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500]

LOWR_ANG = [0, 30, 60, 70, 90, 90, 90, 90, 0, 50]
ZERO_ANG  =[90, 40, 90, 90, 90, 90, 90, 90, 90, 70]
MAX_ANG  =[180, 100, 120, 110, 90, 90, 90, 90, 180, 120]

#Objects
pca = ServoKit(channels=16)

# function init 
def init():

    for i in range(nbPCAServo):
        pca.servo[i].set_pulse_width_range(MIN_IMP[i] , MAX_IMP[i])


# function main 
def main():

    pcaScenario();


# function pcaScenario 
def pcaScenario():
    """Scenario to test servo"""
    for i in range(nbPCAServo):
        for j in range(ZERO_ANG[i],MAX_ANG[i],1):
            print("Send angle {} to Servo {}".format(j,i))
            pca.servo[i].angle = j
            time.sleep(0.02)
        for j in range(MAX_ANG[i],LOWR_ANG[i],-1):
            print("Send angle {} to Servo {}".format(j,i))
            pca.servo[i].angle = j
            time.sleep(0.02)
        for j in range(LOWR_ANG[i],ZERO_ANG[i],1):
            print("Send angle {} to Servo {}".format(j,i))
            pca.servo[i].angle = j
            time.sleep(0.02)    
        # pca.servo[i].angle=None #disable channel
        time.sleep(0.5)




if __name__ == '__main__':
    init()
    main()