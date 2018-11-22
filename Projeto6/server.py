from threading import Thread, Lock
from lib.snake import Snake
from lib.player import PlayerList, Player
from lib.food import Food, FoodSpawner
from lib.colisions import distance, is_between, is_out
import socketserver
import json
import pygame

PLAYERS = None
TICK = 0
SIZE = ()
BLACK = (0, 0, 0)
LOCK = Lock()

class PytronHandler(socketserver.BaseRequestHandler):
    """
    Classe Handler para o servidor do pytron.
    """
    def handle(self):
        global LOCK
        LOCK.acquire()
        try:
            data = json.loads(self.request[0].strip())
        except json.JSONDecodeError:
            print(self.request[0].strip())
            self.request[1].sendto("BAD REQUEST".encode('utf-8'), self.client_address)       
        try:
            if data['id'] == 0:
                self.newplayer(data)
            else:
                self.responseplayer(data)
            LOCK.release()
        except KeyError:
            self.request[1].sendto("BAD REQUEST".encode('utf-8'), self.client_address)

    def newplayer(self, data):
        global PLAYERS
        data["id"] = PLAYERS.spawn()
        data["direction"] = PLAYERS[-1].snake.direction
        self.responseplayer(data)

    def responseplayer(self, data):
        global PLAYERS, TICK, SIZE
        try:
            resposta = {'players':[], 'food':[]}
            for player in PLAYERS:
                if player.ident == data["id"]:
                    player.snake.change_direction(data["direction"])
                    resposta['you'] = player.to_dict()
                else:
                    resposta['players'].append(player.to_dict())
            for food in Food.list:
                resposta['food'].append(food.to_dict())
            resposta['tick'] = TICK
            resposta['size'] = SIZE
            self.request[1].sendto(json.dumps(resposta).encode('utf-8'), self.client_address)
        except KeyError:
            self.request[1].sendto("BAD REQUEST".encode('utf-8'), self.client_address)

class ServerThread(Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs={}, *, daemon=None, ip, port):
        super().__init__()
        self.ip, self.port = ip, port
        self.server = socketserver.UDPServer((self.ip, self.port), PytronHandler)
        
    def run(self):
        self.server.serve_forever()

    def stop(self):
        self.server.shutdown()



# Import a library of functions called 'pygame'

class GameThread(Thread):

    def __init__(self, group=None, target=None, name=None, args=(), kwargs={}, *, daemon=None, size, tick):
        super().__init__()
        self.size = size
        self.tick = tick
    def run(self):
        pygame.init()
        screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption("pytron")
        clock = pygame.time.Clock()
        done = False
        while not done:
            global LOCK
            clock.tick(self.tick)
            LOCK.acquire()
            global PLAYERS
            for event in pygame.event.get():
                if event.type == pygame.QUIT: # If user clicked close
                    done = True # Flag that we are DONE so we exit this loop
            screen.fill(BLACK)
            for food in Food.list:
                pygame.draw.circle(screen, food.color, (food.x, food.y), 3, 0)
            #Check and move all players.
            for player in PLAYERS:
                if player.snake.dead:
                    PLAYERS.remove(player)
                    continue
                player.snake.move()
                if is_out(player.snake.head, self.size[0], self.size[1]): #Check if player's head is inside the field
                    player.snake.die()
                    continue
                
                #Check if player's head colides with other player
                for other in PLAYERS:
                    for i in range(len(other.snake.joints) - 1):
                        if is_between(other.snake.joints[i], player.snake.head, other.snake.joints[i + 1]):
                            #colide with itself
                            if other == player:
                                #ignore last joint
                                if i < len(player.snake.joints) - 2:
                                    player.snake.die()
                            #colide with someone else
                            else:
                                player.snake.die()
                    if other != player:
                        if is_between(other.snake.head, player.snake.head, other.snake.joints[-1]):
                            player.snake.die()
                    
                #check if player eats a food
                for food in Food.list:
                    pygame.draw.circle(screen, food.color, (food.x, food.y), 3, 0)
                    if distance(player.snake.head, (food.x, food.y)) < 4:
                        player.snake.eat()
                        player.foodspawner.spawn()
                        food.consume()
                    
                    #draw the player
                for i in range(len(player.snake.joints) - 1):
                    pygame.draw.line(screen, player.snake.color, player.snake.joints[i], player.snake.joints[i + 1], 2)
                pygame.draw.line(screen, player.snake.color, player.snake.joints[-1], player.snake.head, 2)
            pygame.display.update()
            LOCK.release()
        pygame.quit()
        return

def main():
    global PLAYERS, TICK, SIZE
    print("Set server settings:")
    x, y = [int(i) for i in input("Board size: ").split()]
    maxi = int(input("Maximum numbers of players: "))
    SIZE = (x, y)
    PLAYERS = PlayerList(maxi, SIZE)
    TICK = int(input("Tickrate: "))
    ip = input("Ip: ")
    port = int(input("port: "))
    gt = GameThread(size=SIZE, tick=TICK, daemon=True)
    st = ServerThread(ip=ip, port=port, daemon=True)
    gt.start()
    st.start()
    gt.join()
    st.stop()
    return

if __name__ == "__main__":
    main()

