# import curses and GPIO
import curses
import RPi.GPIO as GPIO

# set GPIO numbering mode and define output pins
GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.IN)

# Get the curses window, turn off echoing of keyboard to screen, turn on
# instant (no waiting) key response, and use special values for cursor keys
screen = curses.initscr()
curses.noecho()
curses.cbreak()
screen.keypad(True)

try:
    found=False
    while True:
        char = screen.getch()
        if char == ord('q'):
            break

        if GPIO.input(7)==1:
            if not found:
                print("block")

            	found=True
        elif GPIO.input(7)==0:
            found=False

finally:
    # Close down curses properly, inc turn echo back on!
    curses.nocbreak()
    screen.keypad(0)
    curses.echo()
    curses.endwin()
    GPIO.cleanup()
