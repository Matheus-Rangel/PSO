from random import randint
from . import colisions

class food():
    list = []
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

    def consume(self):
        food.list.remove(self)
        del self

class foodSpawner():
    def __init__(self, sizex, sizey, color, snakes):
        self.sizex = sizex
        self.sizey = sizey
        self.color = color
        self.snakes = snakes

    def spawn(self):
        valid = False
        while (not valid):
            x = randint(0, self.sizex)
            y = randint(0, self.sizey)
            valid = True
            for snake in self.snakes:
                for i in range(len(snake.joints) - 1):
                    if (colisions.is_between(snake.joints[i], (x,y), snake.joints[i + 1])):
                        valid = False
                        break
                if(not valid):
                    break
        food.list.append(food(x, y, self.color))
        return valid
