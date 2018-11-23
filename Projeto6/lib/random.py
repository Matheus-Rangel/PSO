import random

def random_rgbcolor():
    """
    Returns a random tuple with rgb values from 0 to 255
    """
    red = random.randrange(50, 255)
    green = random.randrange(50, 255)
    blue = random.randrange(50, 255)
    return (red, green, blue)

def random_snake_direction():
    """
    Returns a random snake direction
    """
    directions = ('w', 'e', 'n', 's')
    return random.choice(directions)

def random_boleam(p):
    """
    Returns a random bolean, where the probability of been False is equal to p
    0<p<1
    """
    return random.uniform(0, 1) > p