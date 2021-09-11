# import curses and GPIO
import curses
import RPi.GPIO as GPIO
import threading

# set GPIO numbering mode and define output pins
GPIO.setmode(GPIO.BOARD)
GPIO.setup(32, GPIO.IN)

# Get the curses window, turn off echoing of keyboard to screen, turn on
# instant (no waiting) key response, and use special values for cursor keys
screen = curses.initscr()
curses.noecho()
curses.cbreak()
screen.keypad(True)

fla = False


def sensor():
    found = False
    while True:
        if GPIO.input(32) == 1:
            if not found:
                print("block")
                found = True
        elif GPIO.input(32) == 0:
            found = False

        if fla:
            break


t1 = threading.Thread(target=sensor)
t1.start()

try:
    while True:
        char = screen.getch()
        if char == ord('q'):
            fla = True
            break

finally:
    t1.join()
    # Close down curses properly, inc turn echo back on!
    curses.nocbreak()
    screen.keypad(0)
    curses.echo()
    curses.endwin()
    GPIO.cleanup()
