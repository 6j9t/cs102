import curses

from life import GameOfLife
from ui import UI


class Console(UI):

    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

    def draw_borders(self, screen) -> None:
        """ Отобразить рамку. """
        screen.border(0)

    def draw_grid(self, screen) -> None:
        """ Отобразить состояние клеток. """
        grid = self.life.curr_generation
        for i in range(len(grid)):
            for j in range(len([0])):
                if grid[i][j] == 1:
                    screen.addstr(j + 1, i + 1, '*')

    def run(self) -> None:
        screen = curses.initscr()
        # PUT YOUR CODE HERE
        running = True
        while running:
            screen.clear()
            self.draw_borders(screen)
            self.draw_grid(screen)
            self.life.step()
            if self.life.is_max_generations_exceeded:
                running = False
            screen.refresh()
        curses.endwin()

#if __name__ == '__main__':
    life = GameOfLife((24,80), max_generations=50)
    ui = Console(life)
    ui.run()
