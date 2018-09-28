import socketserver
import pyautogui
import socket
def generateKeyStroke(key):
    pyautogui.typewrite(key.decode("utf-8"))

class JoystickHandler(socketserver.DatagramRequestHandler):
    def handle(self):
        key = self.rfile.read()
        generateKeyStroke(key)
        print("Signal = {}".format(key.decode("utf-8")))

if __name__ == "__main__":
    print ('Starting Joystick server, use <Ctrl-C> to stop')
    with socketserver.UDPServer(("192.168.7.1", 30000), JoystickHandler) as server:
        server.serve_forever()
