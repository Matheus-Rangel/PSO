import socketserver
import pyautogui
import socket

class JoystickHandler(socketserver.DatagramRequestHandler):
    def handle(self):
        key = self.rfile.read().decode("utf-8")
        pyautogui.typewrite(key)
        print("Signal = {}".format(key))

if __name__ == "__main__":
    print ('Starting Joystick server, use <Ctrl-C> to stop')
    with  socketserver.ThreadingUDPServer(("192.168.7.1", 30000), JoystickHandler) as server:
        server.serve_forever()
