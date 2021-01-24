from Worker import Worker
import multiprocessing as mp
import time
from Models.Snake import Snake
from Models.Food import Food


class WorkerForce(Worker):
    def __init__(self, force, players, snakes, maxMovesPerSnake, playerSnakeId,myUniqueID, in_q: mp.Queue, out_q: mp.Queue, grid):
        super().__init__()
        self.in_q = in_q
        self.out_q = out_q
        self.snakes = snakes
        self.players = players
        self.force = force
        self.grid = grid
        self.MyUniqueID = myUniqueID
        self.MaxMovesPerSnake = maxMovesPerSnake
        self.PlayerSnakeId = playerSnakeId
    def work(self):
        while True:
            snks = list(map(lambda s: [s.head.x, s.head.y], self.snakes))
            ff = list(map(lambda ft: [ft.x, ft.y], self.force))
            self.in_q.put([snks, ff])

            ret = self.out_q.get()
            if ret[0] != -1:
                for f in self.force:
                    if f.x == ret[0] and f.y == ret[1]:
                        self.force.remove(f)
                        break
                for s in self.snakes:
                    if s.head.x == ret[2] and s.head.y == ret[3]:
                        s.eat = 1
                        if self.PlayerSnakeId[0] == self.MyUniqueID:
                            self.MaxMovesPerSnake[self.PlayerSnakeId[1]] = \
                                self.MaxMovesPerSnake[self.PlayerSnakeId[1]] + 1
                            break
                self.update.emit()

                while not self.out_q.empty():
                    self.out_q.get()

            time.sleep(0.001)