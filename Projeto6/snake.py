
class snake():
    def __init__(self, pos_x, pos_y, color, direction):
        """
        Size of the snake
        """
        self.size = 1

        """
        List of snake joints
        """
        self.joints = [[pos_x, pos_y]]

        """
        Position of snake head
        """
        if (direction == 'n'):
            self.head = [pos_x, pos_y - 50]
        elif (direction == 's'):
            self.head = [pos_x, pos_y + 50]
        elif (direction == 'e'):
            self.head = [pos_x + 50, pos_y]
        elif (direction == 'w'):
            self.head = [pos_x - 50, pos_y]

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
        self.__delete_last()
        self.__create_next()

    def die(self):
        pass

    def eat(self):
        self.size += 1
        self.create_next()

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

    def __create_next(self):
        if (self.direction == 'n'):
            self.head[1] -= 1
        elif (self.direction == 's'):
            self.head[1] += 1
        elif (self.direction == 'e'):
            self.head[0] += 1
        elif (self.direction == 'w'):
            self.head[0] -= 1

    def __delete_last(self):
        tail = self.joints[0]
        if (len(self.joints) == 1):
            if (self.direction == 'n'):
                tail[1] -= 1
            elif (self.direction == 's'):
                tail[1] += 1
            elif (self.direction == 'e'):
                tail[0] += 1
            elif (self.direction == 'w'):
                tail[0] -= 1
        else:
            joint = self.joints[1]
            if (joint[0] > tail[0]):
                tail[0] += 1
            elif (joint[0] < tail[0]):
                tail[0] -= 1
            elif (joint[1] > tail[1]):
                tail[1] += 1
            elif (joint[1] < tail[1]):
                tail[1] -= 1
            else:
                self.joints.remove(tail)
                self.__delete_last()
