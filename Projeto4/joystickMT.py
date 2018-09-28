import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.ADC as ADC
import socket
import time
import threading

def emitSignal(signal): #signal = keystroke to server
    s.send(signal)
    s.close()

class joystickSocket():
    self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def __init__(self, timeout = 10, ip = "192.168.7.1", porta = 30000):
        self.s.settimeout(10)
        self.s.connect((ip, porta))

    def emitSignal(self, signal): #signal = keystroke to server
        self.s.send(signal)
    
    def __del__(self):
        self.s.close()

lock = threading.Lock()

class pot(Thread.threading):
    AIN = "AIN0"
    def __init__(joy_socket = joystickSocket()):

    def run(self):
        while True:
            p = ADC.read(self.AIN)
            if (p < 0.3):
                self.joy_socket.emitSignal('A')
            elif(p > 0.7):
                lock.acquire()
                self.joy_socket.emitSignal('D')
                lock.release()


class luz(Thread.threading):

    def run(self):


class bot(Thread.threading):

    def run(self):


def luz():
    l = ADC.read("AIN1")
    while True:
        l2 = ADC.read("AIN1")
        if(l2  > (l + 0.01)):
            emitSignal('E')
        l = l2

def bot():
    GPIO.setup("P9_27", GPIO.IN)
    while True:
        b = GPIO.input("P9_27")
        if b:
            emitSignal('B')



if __name__ == '__main__':
    ADC.setup()
    tpot = threading.Thread(target= pot)
    tluz = threading.Thread(target= luz)
    tbot = threading.Thread(target= bot)
    tpot.start()
    tluz.start()
    tbot.start()
