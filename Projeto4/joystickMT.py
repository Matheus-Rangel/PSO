import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.ADC as ADC
import socket
import time
import threading

class joystickSocket():
    def __init__(self, timeout = 10, ip = "192.168.7.1", porta = 30000):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.settimeout(10)
        self.s.connect((ip, porta))

    def emitSignal(self, signal): #signal = keystroke to server
        self.s.send(signal)

    def __del__(self):
        self.s.close()

class Pot(threading.Thread):
    def __init__(self, joy_socket = joystickSocket(), AIN = "AIN0"):
        threading.Thread.__init__(self)
        self.joy_socket = joy_socket
        self.AIN = AIN
        return

    def run(self):
        while True:
            p = ADC.read(self.AIN)
            if (p < 0.3):
                self.joy_socket.emitSignal('A')
            elif(p > 0.7):
                self.joy_socket.emitSignal('D')
            time.sleep(0.1)


class Luz(threading.Thread):

    def __init__(self, joy_socket = joystickSocket(), AIN = "AIN1"):
        threading.Thread.__init__(self)
        self.joy_socket = joy_socket
        self.AIN = AIN
        return

    def run(self):
        l = ADC.read(self.AIN)
        while True:
            l2 = ADC.read(self.AIN)
            if(l2  > (l + 0.01)):
                self.joy_socket.emitSignal('E')
            l = l2
            time.sleep(0.1)

class Bot(threading.Thread):

    def __init__(self, joy_socket = joystickSocket(), PIO = "P9_27"):
        threading.Thread.__init__(self)
        self.joy_socket = joy_socket
        self.PIO = PIO
        return

    def run(self):
        GPIO.setup(self.PIO, GPIO.IN)
        while True:
            if GPIO.input(self.PIO):
                self.joy_socket.emitSignal('P')
            time.sleep(0.1)

if __name__ == '__main__':
    ADC.setup()
    pot = Pot()
    luz = Luz()
    bot = Bot()
    pot.start()
    luz.start()
    bot.start()
