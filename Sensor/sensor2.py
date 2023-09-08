# import curses and GPIO
import curses
import RPi.GPIO as GPIO
import threading

# set GPIO numbering mode and define output pins
GPIO.setmode(GPIO.BOARD)
GPIO.setup(31, GPIO.OUT)
GPIO.setup(32, GPIO.IN)

# Get the curses window, turn off echoing of keyboard to screen, turn on
# instant (no waiting) key response, and use special values for cursor keys
screen = curses.initscr()
curses.noecho()
curses.cbreak()
screen.keypad(True)

exitFlag = False


def sensor():
    block = False
    while True:
        if GPIO.input(32) == 1:
            if not block:
                print("block")
                GPIO.output(31,True)
                block = True
        elif GPIO.input(32) == 0:
            block = False
            GPIO.output(31,False)

        if exitFlag:
            break


t1 = threading.Thread(target=sensor)
t1.start()

try:
    while True:
        char = screen.getch()
        if char == ord('q'):
            exitFlag = True
            break

finally:
    t1.join()
    # Close down curses properly, inc turn echo back on!
    curses.nocbreak()
    screen.keypad(0)
    curses.echo()
    curses.endwin()
    GPIO.cleanup()
