import time
import multiprocessing as mp
from PyQt5.QtCore import Qt


class CollisionProcess(mp.Process):
    def __init__(self, input_q: mp.Queue,  output_q: mp.Queue):
        super().__init__(target=self.__checkCollision__, args=[input_q, output_q])

    def __checkCollision__(self, input_q: mp.Queue, output_q: mp.Queue):
        while True:
            data_from_q = None
            should_kill = False          
            while not input_q.empty():
                data_from_q = input_q.get()
            if data_from_q is not None:
                head = data_from_q[0]
                keys = data_from_q[1]
                body_parts = data_from_q[2]
                tails = data_from_q[3]
                
                direction = ''
                while keys:
                    if keys[0] == Qt.Key_Up:
                        direction = 'u'
                        if head[0] == 0 or self.checkForSnakeParts(head, body_parts, tails, direction):
                            should_kill = True
                    elif keys[0] == Qt.Key_Down:
                        direction = 'd'
                        if head[0] == 14 or self.checkForSnakeParts(head, body_parts, tails, direction):
                            should_kill = True
                    elif keys[0] == Qt.Key_Left:
                        direction = 'l'
                        if head[1] == 0 or self.checkForSnakeParts(head, body_parts, tails, direction):
                            should_kill = True
                    elif keys[0] == Qt.Key_Right:
                        direction = 'r'
                        if head[1] == 14 or self.checkForSnakeParts(head, body_parts, tails, direction):
                            should_kill = True
    
                    if should_kill is True:
                        output_q.put([head[0], head[1], keys[0]])
                        time.sleep(0.05)
                        break
                    else:
                        output_q.put([direction, keys[0]])
                        time.sleep(0.05)
                        break

            time.sleep(0.01)
            output_q.put([-1])
    
    @staticmethod
    def checkForSnakeParts(head, body_parts, tails, direction):
        if direction == 'u':
            for body_part in range(len(body_parts)):
                if head[0] - 1 == body_parts[body_part][0] and head[1] == body_parts[body_part][1]:
                    return True
            for tail in range(len(tails)):   
                if head[0] - 1 == tails[tail][0] and head[1] == tails[tail][1]:
                    return True
        elif direction == 'd':
            for body_part in range(len(body_parts)):
                if head[0] + 1 == body_parts[body_part][0] and head[1] == body_parts[body_part][1]:
                    return True
            for tail in range(len(tails)):   
                if head[0] + 1 == tails[tail][0] and head[1] == tails[tail][1]:
                    return True            
        elif direction == 'l':
            for body_part in range(len(body_parts)):
                if head[0] == body_parts[body_part][0] and head[1] - 1 == body_parts[body_part][1]:
                    return True
            for tail in range(len(tails)):   
                if head[0] == tails[tail][0] and head[1] - 1 == tails[tail][1]:
                    return True            
        elif direction == 'r':
            for body_part in range(len(body_parts)):
                if head[0] == body_parts[body_part][0] and head[1] + 1 == body_parts[body_part][1]:
                    return True
            for tail in range(len(tails)):   
                if head[0]  == tails[tail][0] and head[1] + 1 == tails[tail][1]:
                    return True
        else:
            return False
            