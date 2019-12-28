import pathlib
import random

from typing import List, Optional, Tuple


Cell = Tuple[int, int]
Cells = List[int]
Grid = List[Cells]


class GameOfLife:
    
    def __init__(
        self,
        size: Tuple[int, int],
        randomize: bool=True,
        max_generations: Optional[float]=float('inf')
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

    def create_grid(self, randomize: bool=False) -> Grid:
        # Copy from previous assignment
        list = [[0 for i in range(self.cols)] for i in range(self.rows)]
        if randomize == 1:
            for i in range(self.rows):
                for j in range(self.cols):
                    list[i][j] = random.randrange(0, 2)
        return list

    def get_neighbours(self, cell: Cell) -> Cells:
        # Copy from previous assignment
        y, x = cell
        ans = []
        for xx, yy in [(x - 1, y - 1), (x - 1, y), (x - 1, y + 1), (x, y - 1), (x, y + 1), (x + 1, y - 1), (x + 1, y),
                       (x + 1, y + 1)]:
            if 0 <= yy < self.rows and 0 <= xx < self.cols:
                ans.append((yy, xx))
        answer = []
        for i in range(len(ans)):
            y, x = ans[i]
            answer.append(self.curr_generation[y][x])
        return answer

    def get_next_generation(self) -> Grid:
        # Copy from previous assignment
        newgen = self.create_grid()
        for y in range(self.rows):
            for x in range(self.cols):
                if self.curr_generation[y][x] == 0:
                    if self.get_neighbours((y, x)).count(1) == 3:
                        newgen[y][x] = 1
                else:
                    if self.get_neighbours((y, x)).count(1) in [2, 3]:
                        newgen[y][x] = 1
                    else:
                        newgen[y][x] = 0
        return newgen

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        self.prev_generation=self.curr_generation
        self.curr_generation=self.get_next_generation()
        self.generations+=1

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        return self.generations >= self.max_generations

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        return self.prev_generation!= self.curr_generation

    @staticmethod
    def from_file(filename: pathlib.Path) -> 'GameOfLife':
        """
        Прочитать состояние клеток из указанного файла.
        """
        file1 = open(filename, "r")
        grid = [[i for i in list(j)] for j in file1.readlines()]
        for i in range (len(grid)-1):
            grid[i].pop(len(grid[i])-1)
        x = len(grid)
        y = len(grid[0])
        game = GameOfLife((x,y))
        game.curr_generation = grid
        return game


    @staticmethod
    def save(grid, filename: str) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        file1 = open(filename,"w")
        for x in grid:
            file1.write("{} \n".format(x))

if __name__ == '__main__':
    random.seed(1234)
    life = GameOfLife((5,5))
    for i in range(len(life.curr_generation)):
        print(life.curr_generation[i])
    print("\n")
    life.step()
    for i in range(len(life.prev_generation)):
        print(life.prev_generation[i])
    print("\n")
    for i in range(len(life.curr_generation)):
        print(life.curr_generation[i])
    print("\n")
    random.seed(4321)
    life = GameOfLife((10,10), max_generations=50)
    while life.is_changing and not life.is_max_generations_exceeded:
        life.step()
    print(life.generations)
    print("\n")
    life = GameOfLife.from_file('glider.txt')
    for i in range(len(life.curr_generation)):
        print(life.curr_generation[i])
    print("\n")
    random.seed(1234)
    life = GameOfLife((5,5))
    for i in range(4):
        life.step()
    life.save(life.curr_generation, "glider-4-steps.txt")
