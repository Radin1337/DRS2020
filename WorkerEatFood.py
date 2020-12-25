from Worker import Worker
import multiprocessing as mp
import time
from Models.Snake import Snake
from Models.Food import Food


class WorkerEatFood(Worker):
    def __init__(self, food, snakes, in_q: mp.Queue, out_q: mp.Queue):
        super().__init__()
        self.in_q = in_q
        self.out_q = out_q
        self.snakes = snakes
        self.food = food

    def work(self):
        while True:
            snks = list(map(lambda s: [s.head.x, s.head.y], self.snakes))
            fd = list(map(lambda ft: [ft.x, ft.y], self.food))
            self.in_q.put([snks, fd])

            ret = self.out_q.get()
            if ret[0] != -1:
                for f in range(len(self.food)):
                    self.update.emit([ret[0], ret[1]])

            time.sleep(0.001)
