import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.ADC as ADC
import socket
import time
import curses
from curses import wrapper

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.settimeout(10)
s.connect(("192.168.7.1", 30000))

def emitSignal(signal): #signal = keystroke to server
    s.send(signal)
    s.close()

def main(stdscr):
    ADC.setup()
    GPIO.setup("P9_27", GPIO.IN)
    stdscr.clear()
    l = ADC.read("AIN1")
    while True:
        p = ADC.read("AIN0")
        l2 = ADC.read("AIN1")
        b = GPIO.input("P9_27")
        if (p < 0.1):
            emitSignal('A')
            stdscr.addstr(1, 40, "KEY = 'A'")
        elif(p > 0.9):
            emitSignal('D')
            stdscr.addstr(1, 40, "KEY = 'D'")
        else:
            stdscr.addstr(1, 40, "KEY = ' '")

        if(l2  > (l + 0.01)):
            emitSignal('E')
            stdscr.addstr(2, 40, "KEY = 'E'")
        else:
            stdscr.addstr(2, 40, "KEY = ' '")

        if(b == 1):
            emitSignal('P')
            stdscr.addstr(3, 40, "KEY = 'P'")
        else:
            stdscr.addstr(3, 40, "KEY = ' '")

        stdscr.addstr(1, 0, "Potenciometro = {}".format(p))
        stdscr.addstr(2, 0, "Luz = {}".format(l))
        stdscr.addstr(3, 0, "Botao = {}".format(b))
        stdscr.refresh()
        l = l2
        time.sleep(0.1)

if __name__ == '__main__':
    wrapper(main)
