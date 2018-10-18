# Import a library of functions called 'pygame'
import pygame
from math import pi
from snake import snake

# Initialize the game engine
pygame.init()

# Define the colors we will use in RGB format
BLACK = (  0,   0,   0)
GREEN = (  0, 255,   0)

# Set the height and width of the screen
size = (1200, 720)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("pytron")
player = snake(color=GREEN, pos_x = 600, pos_y = 300, direction='n')
#Loop until the user clicks the close button.
done = False
clock = pygame.time.Clock()

while not done:
    # This limits the while loop to a max of 10 times per second.
    # Leave this out and we will use all CPU we can.
    clock.tick(60)
    player.move()
    for event in pygame.event.get(): # User did something
        print(event)
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

    # All drawing code happens after the for loop and but
    # inside the main while done==False loop.

    # Clear the screen and set the screen background
    screen.fill(BLACK)

    # Draw on the screen a GREEN line from (0,0) to (50.75)
    # 5 pixels wide.
    for i in range(len(player.joints) - 1):
        pygame.draw.line(screen, player.color, player.joints[i], player.joints[i + 1], 2)
    pygame.draw.line(screen, player.color, player.joints[-1], player.head, 2)


    pygame.display.update()

# Be IDLE friendly
pygame.quit()
