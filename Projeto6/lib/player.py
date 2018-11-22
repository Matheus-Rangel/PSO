from lib.snake import Snake
from lib.food import FoodSpawner
from lib.random import random_rgbcolor, random_snake_direction

class Player():
    ident = 0
    def __init__(self, snake, foodspawner):
        self.snake = snake
        self.foodspawner = foodspawner
        Player.ident += 1
        self.ident = Player.ident
    def to_dict(self):
        """
        Convert Player atributes to a dictionary
        """
        return {"snake" : self.snake.to_dict(), "ident": self.ident}

class PlayerList(list):
    """
    List with players objects
    """
    def __init__(self, maximum, size):
        list.__init__(self)
        #maximum numbers of players
        self.maximum = maximum
        self.size = size

    def spawn(self):
        """
        Spawn a new snake
        """
        if self.__len__() >= self.maximum:
            return 0
        else:
            color = random_rgbcolor()
            snake = Snake(int(self.size[0]/2), int(self.size[1]/2), color, random_snake_direction())
            foodspawner = FoodSpawner(self.size[0], self.size[1], color, self)
            foodspawner.spawn()
            self.append(Player(snake, foodspawner))
            return Player.ident
