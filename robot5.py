# import curses and GPIO
import curses
import RPi.GPIO as GPIO
import re
import time
import argparse
import threading

from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.virtual import viewport
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT, TINY_FONT, SINCLAIR_FONT, LCD_FONT

# create matrix device
serial = spi(port=0, device=0, gpio=noop())
device = max7219(serial, cascaded=1, block_orientation=0, rotate=0)
print("Created device")

def demo(msg):
    # start demo
    print(msg)
    show_message(device, msg, fill="white", font=proportional(LCD_FONT), scroll_delay=0.1)
    time.sleep(1)

#set GPIO numbering mode and define output pins
GPIO.setmode(GPIO.BOARD)
GPIO.setup(7,GPIO.OUT)
GPIO.setup(11,GPIO.OUT)
GPIO.setup(13,GPIO.OUT)
GPIO.setup(15,GPIO.OUT)
GPIO.setup(16,GPIO.OUT)
GPIO.setup(18,GPIO.OUT)
GPIO.setup(29,GPIO.OUT)
GPIO.setup(31,GPIO.OUT)

# Get the curses window, turn off echoing of keyboard to screen, turn on
# instant (no waiting) key response, and use special values for cursor keys
GPIO.output(31,True)
screen = curses.initscr()
curses.noecho()
curses.cbreak()
screen.keypad(True)
t1 = threading.Thread(target=demo, args=("Hello everyone",))
t2 = threading.Thread(target=demo, args=("Shine bright like a diamond",))
try:
        while True:
            char = screen.getch()
            if char == ord('q'):
                break
            elif char == ord('a'):
                demo("Khanh An")
            elif char == ord('s'):
                demo("Suri")
            elif char == ord('l') or char == ord('L'):
                GPIO.output(29,True)
            elif char == ord('o') or char == ord('O'):
                GPIO.output(29,False)
            elif char == ord('k') or char == ord('K'):
                GPIO.output(31,False)
            elif char == ord('i') or char == ord('I'):
                GPIO.output(31,True)
            elif char == curses.KEY_UP:
                if not t1.isAlive() and not t2.isAlive():
                    t1 = threading.Thread(target=demo, args=("Hello everyone",))
                    t1.start()
                GPIO.output(7,False)
                GPIO.output(11,True)
                GPIO.output(13,False)
                GPIO.output(15,True)
                GPIO.output(16,False)
                GPIO.output(18,False)
            elif char == curses.KEY_DOWN:
                if not t1.isAlive() and not t2.isAlive():
                    t2 = threading.Thread(target=demo, args=("Shine bright like a diamond",))
                    t2.start()
                GPIO.output(7,True)
                GPIO.output(11,False)
                GPIO.output(13,True)
                GPIO.output(15,False)
                GPIO.output(16,False)
                GPIO.output(18,False)
            elif char == curses.KEY_RIGHT:
                GPIO.output(7,True)
                GPIO.output(11,False)
                GPIO.output(13,False)
                GPIO.output(15,True)
                GPIO.output(16,True)
                GPIO.output(18,False)
            elif char == curses.KEY_LEFT:
                GPIO.output(7,False)
                GPIO.output(11,True)
                GPIO.output(13,True)
                GPIO.output(15,False)
                GPIO.output(16,False)
                GPIO.output(18,True)
            elif char == 10:
                GPIO.output(7,False)
                GPIO.output(11,False)
                GPIO.output(13,False)
                GPIO.output(15,False)
                GPIO.output(16,False)
                GPIO.output(18,False)
finally:
    #Close down curses properly, inc turn echo back on!
    curses.nocbreak()
    screen.keypad(0)
    curses.echo()
    curses.endwin()
    GPIO.cleanup()

