import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.ADC as ADC
import socket
import time
import threading

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.settimeout(10)
s.connect(("192.168.7.1", 30000))

def emitSignal(signal): #signal = keystroke to server
    s.send(signal)
    s.close()

def pot():
    while True:
        p = ADC.read("AIN0")
        if (p < 0.3):
            emitSignal('A')
        elif(p > 0.7):
            emitSignal('D')

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
