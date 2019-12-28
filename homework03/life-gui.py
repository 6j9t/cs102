import pygame
from pygame.locals import *

from life import GameOfLife
from ui import UI


class GUI(UI):

    def __init__(self, life: GameOfLife, cell_size: int=20, speed: int=10) -> None:
        super().__init__(life)
        self.width = self.life.cols * cell_size
        self.height = self.life.rows * cell_size
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = self.width, self.height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed

    def draw_lines(self) -> None:
        # Copy from previous assignment
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (0, y), (self.width, y))

    def draw_grid(self) -> None:
        # Copy from previous assignment
        for i in range(self.cell_height):
            for j in range(self.cell_width):
                if self.life.curr_generation[i][j] == 1:
                    pygame.draw.rect(self.screen, pygame.Color('green'), (
                    j * self.cell_size + 1, i * self.cell_size + 1, self.cell_size - 1, self.cell_size - 1))

    def run(self) -> None:
        # Copy from previous assignment
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))

        # Создание списка клеток
        # PUT YOUR CODE HERE

        running = True
        pause = False
        while running:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    pause = True
                if event.type == pygame.KEYUP:
                    pause = False
                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    x, y = pos
                    x = int(x / self.cell_size)
                    y = int(y / self.cell_size)
                    self.life.curr_generation[y][x] = 1
                if event.type == QUIT:
                    running = False
            self.screen.fill(pygame.Color('white'))
            self.draw_lines()
            self.draw_grid()
            # Отрисовка списка клеток
            # Выполнение одного шага игры (обновление состояния ячеек)
            # PUT YOUR CODE HERE
            if not pause:
                if not self.life.is_max_generations_exceeded:
                    self.life.step()
                else:
                    pygame.display.set_caption('max generations exceeded')
            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()


if __name__ == '__main__':
    life = GameOfLife((12,16), max_generations=50)
    gui = GUI(life)
    gui.run()
