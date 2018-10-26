from json import JSONEncoder

class snake(JSONEncoder):
    def __init__(self, pos_x, pos_y, color, direction):
        """
        Size of the snake
        """
        self.size = 36

        """
        Snake speed
        """
        self.speed = 4

        """
        Amount of food stocked
        """
        self.reserve = 0

        """
        List of snake joints
        """
        self.joints = [[pos_x, pos_y]]

        """
        Position of snake head
        """
        if (direction == 'n'):
            self.head = [pos_x, pos_y - self.size]
        elif (direction == 's'):
            self.head = [pos_x, pos_y + self.size]
        elif (direction == 'e'):
            self.head = [pos_x + self.size, pos_y]
        elif (direction == 'w'):
            self.head = [pos_x - self.size, pos_y]

        """
        rgb Color of the snake
        """
        self.color = color

        """
        n = North, s = South, e = east, w = west
        """
        self.direction = direction

    def move(self):
        """
        Update snake position
        """
        if (self.reserve > 0):
            self.__create_next()
            self.reserve -= self.speed
            self.size += self.speed
        else:
            self.__create_next()
            self.__delete_last()

    def die(self):
        pass

    def eat(self):
        self.reserve += 18

    def change_direction(self, direction):
        if (self.direction == direction):
            return
        if(self.direction == 'n' and direction == 's'):
            return
        if(self.direction == 's' and direction == 'n'):
            return
        if(self.direction == 'e' and direction == 'w'):
            return
        if(self.direction == 'w' and direction == 'e'):
            return
        self.direction = direction
        self.joints.append(list(self.head))
        return

    #Create a dictionary to serialize has json
    def default(self):
        dict = {'joints':self.joints, 'head':self.head, 'color':self.color, 'direction':self.direction, 'size':self.size}
        return dict

    def __create_next(self):
        if (self.direction == 'n'):
            self.head[1] -= self.speed
        elif (self.direction == 's'):
            self.head[1] += self.speed
        elif (self.direction == 'e'):
            self.head[0] += self.speed
        elif (self.direction == 'w'):
            self.head[0] -= self.speed

    def __delete_last(self):
        tail = self.joints[0]
        if (len(self.joints) == 1):
            if (self.direction == 'n'):
                tail[1] -= self.speed
            elif (self.direction == 's'):
                tail[1] += self.speed
            elif (self.direction == 'e'):
                tail[0] += self.speed
            elif (self.direction == 'w'):
                tail[0] -= self.speed
        else:
            joint = self.joints[1]
            print("joint: {}, tail:{}".format(joint, tail))
            if (joint[0] > tail[0]):
                tail[0] += self.speed
            elif (joint[0] < tail[0]):
                tail[0] -= self.speed
            elif (joint[1] > tail[1]):
                tail[1] += self.speed
            elif (joint[1] < tail[1]):
                tail[1] -= self.speed
            else:
                self.joints.remove(tail)
                self.__delete_last()
