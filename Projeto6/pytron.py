# Import Socket interface and json serializer

# Import a library of functions called 'pygame'
import pygame

from lib.food import Food
from lib.colisions import distance, is_between, is_out
from lib.player import PlayerList

from lib.client import Client


def main():
    server_ip = input("Server Ip: ")
    server_port = int(input("Server Port: "))
    client = Client(server_ip, server_port)
    dados = client.connect()
    # Initialize the game engine
    pygame.init()
    # Define the colors we will use in RGB format
    BLACK = (0, 0, 0)
    # Set the height and width of the SCREEN
    SCREEN = pygame.display.set_mode(dados['size'])
    pygame.display.set_caption("pytron")
    #Loop until the user clicks the close button.
    DONE = False
    CLOCK = pygame.time.Clock()
    player_id = dados['you']['ident']
    player_direction = dados['you']['snake']['direction']
    while not DONE:
        dados = client.send(player_id, player_direction)
        CLOCK.tick(dados['tick'])
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                DONE = True # Flag that we are DONE so we exit this loop
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    player_direction = 'w'
                if event.key == pygame.K_w:
                    player_direction = 'n'
                if event.key == pygame.K_s:
                    player_direction = 's'
                if event.key == pygame.K_d:
                    player_direction = 'e'
        # Clear the SCREEN and set the SCREEN background
        SCREEN.fill(BLACK)
        #Check if PLAYER is out of the map
        
        #Draw Food
        for food in dados['food']:
            pygame.draw.circle(SCREEN, food['color'], (food['x'], food['y']), 3, 0)
        print(dados['you'])
        #Draw You
        player = dados['you']
        joints = player['snake']['joints']
        for i in range(len(joints) - 1):
            pygame.draw.line(SCREEN, player['snake']['color'], joints[i], joints[i + 1], 2)
        pygame.draw.line(SCREEN, player['snake']['color'], joints[-1], player['snake']['head'], 2)    
        
        #Draw SNAKES
        for player in dados['players']:
            joints = player['snake']['joints']
            for i in range(len(joints) - 1):
                pygame.draw.line(SCREEN, player['snake']['color'], joints[i], joints[i + 1], 2)
            pygame.draw.line(SCREEN, player['snake']['color'], joints[-1], player['snake']['head'], 2)

        pygame.display.update()
    pygame.quit()
if __name__ == "__main__":
    main() 