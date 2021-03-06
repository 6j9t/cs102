from typing import Tuple, List, Set, Optional
import random
import time


def read_sudoku(filename: str) -> List[List[str]]:
    """ Прочитать Судоку из указанного файла """
    digits = [c for c in open(filename).read() if c in '123456789.']
    grid = group(digits, 9)
    return grid


def display(grid: List[List[str]]) -> None:
    """Вывод Судоку """
    width = 2
    line = '+'.join(['-' * (width * 3)] * 3)
    for row in range(9):
        print(''.join(grid[row][col].center(width) + ('|' if str(col) in '25' else '') for col in range(9)))
        if str(row) in '25':
            print(line)
    print()


def group(values: List[str], n: int) -> List[List[str]]:
    """
    Сгруппировать значения values в список, состоящий из списков по n элементов

    >>> group([1,2,3,4], 2)
    [[1, 2], [3, 4]]
    >>> group([1,2,3,4,5,6,7,8,9], 3)
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    """
    list = [[0 for i in range(n)] for i in range(len(values) // n)]
    for i in range(0, len(values)):
        list[i // n][i % n] = values[i]
    return list


def get_row(grid: List[List[str]], pos: Tuple[int, int]) -> List[str]:
    """ Возвращает все значения для номера строки, указанной в pos

    >>> get_row([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '2', '.']
    >>> get_row([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (1, 0))
    ['4', '.', '6']
    >>> get_row([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (2, 0))
    ['.', '8', '9']
    """
    return grid[pos[0]]


def get_col(grid: List[List[str]], pos: Tuple[int, int]) -> List[str]:
    """ Возвращает все значения для номера столбца, указанного в pos

    >>> get_col([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '4', '7']
    >>> get_col([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (0, 1))
    ['2', '.', '8']
    >>> get_col([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (0, 2))
    ['3', '6', '9']
    """
    list = []
    for i in range(len(grid)):
        list.append(grid[i][pos[1]])
    return list


def get_block(grid: List[List[str]], pos: Tuple[int, int]) -> List[str]:
    """ Возвращает все значения из квадрата, в который попадает позиция pos

    >>> grid = read_sudoku('puzzle1.txt')
    >>> get_block(grid, (0, 1))
    ['5', '3', '.', '6', '.', '.', '.', '9', '8']
    >>> get_block(grid, (4, 7))
    ['.', '.', '3', '.', '.', '1', '.', '.', '6']
    >>> get_block(grid, (8, 8))
    ['2', '8', '.', '.', '.', '5', '.', '7', '9']
    """
    list = []
    x = pos[0] // 3
    y = pos[1] // 3
    for i in range(3):
        for j in range(3):
            list.append(grid[i + 3 * x][j + 3 * y])
    return list


def find_empty_positions(grid: List[List[str]]) -> Optional[Tuple[int, int]]:
    """ Найти первую свободную позицию в пазле

    >>> find_empty_positions([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']])
    (0, 2)
    >>> find_empty_positions([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']])
    (1, 1)
    >>> find_empty_positions([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']])
    (2, 0)
    """
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == '.':
                return (i, j)
    return None


def find_possible_values(grid: List[List[str]], pos: Tuple[int, int]) -> Set[str]:
    """ Вернуть множество возможных значения для указанной позиции

    >>> grid = read_sudoku('puzzle1.txt')
    >>> values = find_possible_values(grid, (0,2))
    >>> values == {'1', '2', '4'}
    True
    >>> values = find_possible_values(grid, (4,7))
    >>> values == {'2', '5', '9'}
    True
    """
    list = set('123456789')
    list.difference_update(get_col(grid, pos))
    list.difference_update(get_row(grid, pos))
    list.difference_update(get_block(grid, pos))
    return list


def solve(grid: List[List[str]]) -> Optional[List[List[str]]]:
    """ Решение пазла, заданного в grid """
    """ Как решать Судоку?
        1. Найти свободную позицию
        2. Найти все возможные значения, которые могут находиться на этой позиции
        3. Для каждого возможного значения:
            3.1. Поместить это значение на эту позицию
            3.2. Продолжить решать оставшуюся часть пазла

    >>> grid = read_sudoku('puzzle1.txt')
    >>> solve(grid)
    [['5', '3', '4', '6', '7', '8', '9', '1', '2'], ['6', '7', '2', '1', '9', '5', '3', '4', '8'], ['1', '9', '8', '3', '4', '2', '5', '6', '7'], ['8', '5', '9', '7', '6', '1', '4', '2', '3'], ['4', '2', '6', '8', '5', '3', '7', '9', '1'], ['7', '1', '3', '9', '2', '4', '8', '5', '6'], ['9', '6', '1', '5', '3', '7', '2', '8', '4'], ['2', '8', '7', '4', '1', '9', '6', '3', '5'], ['3', '4', '5', '2', '8', '6', '1', '7', '9']]
    """
    pos = find_empty_positions(grid)
    if pos == None:
        return grid
    x = pos[0]
    y = pos[1]
    list = find_possible_values(grid, pos)
    for i in list:
        grid[x][y] = i
        if solve(grid) != None:
            return grid
    grid[x][y] = '.'
    return None


def check_solution(solution: List[List[str]]) -> bool:
    """ Если решение solution верно, то вернуть True, в противном случае False
    >>> check_solution([['5', '4', '4', '6', '7', '8', '9', '1', '2'], ['6', '7', '2', '1', '9', '5', '3', '4', '8'], ['1', '9', '8', '3', '4', '2', '5', '6', '7'], ['8', '5', '9', '7', '6', '1', '4', '2', '3'], ['4', '2', '6', '8', '5', '3', '7', '9', '1'], ['7', '1', '3', '9', '2', '4', '8', '5', '6'], ['9', '6', '1', '5', '3', '7', '2', '8', '4'], ['2', '8', '7', '4', '1', '9', '6', '3', '5'], ['3', '4', '5', '2', '8', '6', '1', '7', '9']])
    False
    >>> check_solution([['5', '3', '4', '6', '7', '8', '9', '1', '2'], ['6', '7', '2', '1', '9', '5', '3', '4', '8'], ['1', '9', '8', '3', '4', '2', '5', '6', '7'], ['8', '5', '9', '7', '6', '1', '4', '2', '3'], ['4', '2', '6', '8', '5', '3', '7', '9', '1'], ['7', '1', '3', '9', '2', '4', '8', '5', '6'], ['9', '6', '1', '5', '3', '7', '2', '8', '4'], ['2', '8', '7', '4', '1', '9', '6', '3', '5'], ['3', '4', '5', '2', '8', '6', '1', '7', '9']])
    True
    >>> check_solution([['5', '3', '4', '6', '7', '8', '9', '1', '2'], ['5', '7', '2', '1', '9', '5', '3', '4', '8'], ['1', '9', '8', '3', '4', '2', '5', '6', '7'], ['8', '5', '9', '7', '6', '1', '4', '2', '3'], ['4', '2', '6', '8', '5', '3', '7', '9', '1'], ['7', '1', '3', '9', '2', '4', '8', '5', '6'], ['9', '6', '1', '5', '3', '7', '2', '8', '4'], ['2', '8', '7', '4', '1', '9', '6', '3', '5'], ['3', '4', '5', '2', '8', '6', '1', '7', '9']])
    False
    >>> check_solution([['5', '3', '4', '6', '7', '8', '9', '1', '2'], ['6', '7', '5', '1', '9', '5', '3', '4', '8'], ['1', '9', '8', '3', '4', '2', '5', '6', '7'], ['8', '5', '9', '7', '6', '1', '4', '2', '3'], ['4', '2', '6', '8', '5', '3', '7', '9', '1'], ['7', '1', '3', '9', '2', '4', '8', '5', '6'], ['9', '6', '1', '5', '3', '7', '2', '8', '4'], ['2', '8', '7', '4', '1', '9', '6', '3', '5'], ['3', '4', '5', '2', '8', '6', '1', '7', '9']])
    False
    """
    list = set('123456789')
    for i in range(len(solution)):
        if set(get_row(solution, (i, 0))) != list:
            return False
    for i in range(len(solution)):
        if set(get_col(solution, (0, i))) != list:
            return False
    for i in range(0, len(solution), 3):
        for j in range(0, len(solution), 3):
            if set(get_block(solution, (i, j))) != list:
                return False
    return True


def generate_sudoku(N: int) -> List[List[str]]:
    """ Генерация судоку заполненного на N элементов

    >>> grid = generate_sudoku(40)
    >>> sum(1 for row in grid for e in row if e == '.')
    41
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(1000)
    >>> sum(1 for row in grid for e in row if e == '.')
    0
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(0)
    >>> sum(1 for row in grid for e in row if e == '.')
    81
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    """
    grid = solve([['.' for i in range(9)] for i in range(9)])
    grid = mix(grid)
    if N > 81:
        N = 81
    dotnumber = 81 - N
    while dotnumber != 0:
        x = random.randrange(0, 9)
        y = random.randrange(0, 9)
        if (grid[x][y] != '.'):
            grid[x][y] = '.'
            dotnumber -= 1
    return grid


def transposing(grid: List[List[str]]) -> List[List[str]]:
    # Транспонирование матрицы
    grid = list(map(list, zip(*grid)))
    return grid


def swap_rows_small(grid: List[List[str]]) -> List[List[str]]:
    # Обмен двух строк в пределах одного блока
    area = random.randrange(0, 3, 1)
    line1 = random.randrange(0, 3, 1)
    N1 = area * 3 + line1
    line2 = random.randrange(0, 3, 1)
    while (line1 == line2):
        line2 = random.randrange(0, 3, 1)
    N2 = area * 3 + line2
    grid[N1], grid[N2] = grid[N2], grid[N1]
    return grid


def swap_colums_small(grid: List[List[str]]) -> List[List[str]]:
    # Обмен двух столбцов в пределах одного блока
    grid = transposing(grid)
    grid = swap_rows_small(grid)
    grid = transposing(grid)
    return grid


def swap_rows_area(grid: List[List[str]]) -> List[List[str]]:
    # Обмен двух райнов (наборов по 3 строки одного блока)
    area1 = random.randrange(0, 3, 1)
    area2 = random.randrange(0, 3, 1)
    while (area1 == area2):
        area2 = random.randrange(0, 3, 1)
    for i in range(0, 3):
        N1, N2 = area1 * 3 + i, area2 * 3 + i
        grid[N1], grid[N2] = grid[N2], grid[N1]
    return grid


def swap_colums_area(grid: List[List[str]]) -> List[List[str]]:
    # Обмен двух районов (наборов по 3 столбца одного блока)
    grid = transposing(grid)
    grid = swap_rows_area(grid)
    grid = transposing(grid)
    return grid


def mix(grid: List[List[str]]) -> List[List[str]]:
    # Рандомизация генератора судоку.
    mix_func = ['transposing(grid)',
                'swap_rows_small(grid)',
                'swap_colums_small(grid)',
                'swap_rows_area(grid)',
                'swap_colums_area(grid)']
    # Цикл выполняется 30 раз. Это число взято случайно
    for i in range(1, 30):
        id_func = random.randrange(0, len(mix_func), 1)
        eval(mix_func[id_func])
    return grid


if __name__ == '__main__':
    for fname in ['puzzle1.txt', 'puzzle2.txt', 'puzzle3.txt']:
        grid = read_sudoku(fname)
        display(grid)
        start = time.time()
        solution = solve(grid)
        end = time.time()
        print(f'{fname}: {end-start}')
        if not solution:
            print(f"Puzzle {fname} can't be solved")
        else:
            display(solution)
            if check_solution(solution):
                print("Solution is correct")
            else:
                print("Oops")
