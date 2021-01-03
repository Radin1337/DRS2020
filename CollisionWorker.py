from Worker import Worker
import multiprocessing as mp
import time


class CollisionWorker(Worker):
    def __init__(self, players, list_of_players, num_of_players, snake, grid, keys, all_snakes, input_q: mp.Queue, output_q: mp.Queue):
        super().__init__()
        self.numOfPlayers = num_of_players
        self.playerOnMove = 0
        self.players = players
        self.listOfPlayers = list_of_players
        self.snake = self.players[self.listOfPlayers[self.playerOnMove]][0]
        self.grid = grid
        self.keys = keys
        self.all_snakes = all_snakes
        self.input_q = input_q
        self.output_q = output_q

    def work(self):
        while True:
            temp_head = [self.snake.head.x, self.snake.head.y]
            temp_tails = list(map(lambda s: [s.tail.x, s.tail.y], self.all_snakes))
            temp_body_parts = []
            for s in self.all_snakes:
                temp_body_parts.extend(list(map(lambda b: [b.x, b.y], s.body)))
            

            self.input_q.put([temp_head, self.keys, temp_body_parts, temp_tails])
            ret_val = self.output_q.get()
            if ret_val[0] != -1:
                if not isinstance(ret_val[0], str):
                    if self.snake.head.x == ret_val[0] and self.snake.head.y == ret_val[1]:
                        self.snake.kill_snake(self.grid)
                        self.keys.remove(ret_val[2])
                else:        
                    self.snake.move(self.grid, ret_val[0])
                    self.keys.remove(ret_val[1])
                    self.playerOnMove = self.playerOnMove + 1
                    if self.playerOnMove == self.numOfPlayers:
                        self.playerOnMove = 0
                    self.snake = self.players[self.listOfPlayers[self.playerOnMove]][0]
                self.update.emit()
                 
                while not self.output_q.empty():
                    self.output_q.get()

            time.sleep(0.001)
