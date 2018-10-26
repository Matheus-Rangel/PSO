# Import a library of functions called 'pygame'
import pygame
from math import pi

from lib.snake import snake
from lib.food import food, foodSpawner
from lib.colisions import distance, is_between, is_out

# Initialize the game engine
pygame.init()

# Define the colors we will use in RGB format
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
CIAN = (0, 255, 255)
# Set the height and width of the screen
size = (1200, 720)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("pytron")
player = snake(color=GREEN, pos_x = 600, pos_y = 300, direction='n')
snakes = [player]
spawner = foodSpawner(sizex=size[0], sizey = size[1], color=CIAN, snakes = snakes)
#Loop until the user clicks the close button.
done = False
clock = pygame.time.Clock()

while not done:

    clock.tick(30)
    player.move()
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done=True # Flag that we are done so we exit this loop
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                player.change_direction(direction = 'w')
            if event.key == pygame.K_w:
                player.change_direction(direction = 'n')
            if event.key == pygame.K_s:
                player.change_direction(direction = 's')
            if event.key == pygame.K_d:
                player.change_direction(direction = 'e')

    # Clear the screen and set the screen background
    screen.fill(BLACK)
    #Check if player is out of the map
    if (is_out(player.head, size[0], size[1])):
        done = True
        break
    #Spawn Food
    if not food.list:
        spawner.spawn()
        print('Food Spawned')
        print(food.list[0])
    for food in food.list:
        pygame.draw.circle(screen, food.color, (food.x, food.y), 3, 0)
        d = distance(player.head, (food.x, food.y))
        if (d < 4):
            player.eat()
            food.consume()

    #Draw snakes
    for i in range(len(player.joints) - 1):
        #Verificar se a cabeca colide com alguma linha do corpo
        if is_between(player.joints[i], player.head, player.joints[i + 1]):
            if (i < len(player.joints) - 2):
                done = True
                break
        pygame.draw.line(screen, player.color, player.joints[i], player.joints[i + 1], 2)
    pygame.draw.line(screen, player.color, player.joints[-1], player.head, 2)

    pygame.display.update()

pygame.quit()
