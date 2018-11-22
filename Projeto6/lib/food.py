from random import randint
from . import colisions

class Food():
    list = []
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

    def consume(self):
        Food.list.remove(self)
        del self
        
    def to_dict(self):
        dic = {'x':self.x, 'y':self.y, 'color':self.color}
        return dic

class FoodSpawner():
    def __init__(self, sizex, sizey, color, players):
        self.sizex = sizex
        self.sizey = sizey
        self.color = color
        self.players = players

    def spawn(self):
        #Finding a valid space to spawn the food
        valid = False
        while not valid:
            x = randint(0, self.sizex)
            y = randint(0, self.sizey)
            valid = True
            for player in self.players:
                snake = player.snake
                for i in range(len(snake.joints) - 1):
                    if colisions.is_between(snake.joints[i], (x,y), snake.joints[i + 1]):
                        valid = False
                        break
                if not valid:
                    break
        Food.list.append(Food(x, y, self.color))
        return valid
