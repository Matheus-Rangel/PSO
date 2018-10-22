# Import a library of functions called 'pygame'
import pygame
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
players = []
#Loop until the user clicks the close button.
done = False
clock = pygame.time.Clock()

while not done:

    clock.tick(60)
    player.move()
    # Clear the screen and set the screen background
    screen.fill(BLACK)

    #Draw snakes
    for player in players:
        for i in range(len(player.joints) - 1):
            pygame.draw.line(screen, player.color, player.joints[i], player.joints[i + 1], 2)
        pygame.draw.line(screen, player.color, player.joints[-1], player.head, 2)

    pygame.display.update()

pygame.quit()
