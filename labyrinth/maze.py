import random
import heapq

import files
import visualisation


def maze_generation(height: int, width: int) -> list[list[str]]:
    """
    Возвращает сгенерированный по алгоритму эйлера лабиринт.
    :param height: Высота лабиринта.
    :param width: Ширина лабиринта.
    :return: Построенный лабиринт.
    """
    # создание шаблона
    # длина и ширина больше заданных для корректного шаблона
    result_height = height * 2 + 1
    result_width = width * 2 + 1
    borders = ((0, result_height - 1), (0, result_width - 1))
    maze = [[] for _ in range(result_height)]

    for i in range(result_height):
        for j in range(result_width):
            element = '0'
            if i in borders[0] or j in borders[1] or (i % 2 == j % 2 == 0):
                element = '1'
            maze[i].append(element)

    # Генерация лабиринта
    print_maze(maze, 'Maze template:')
    row_set = [0] * width
    counter = 1
    random.seed()

    for i in range(height):
        # Присвоение уникальных множеств
        for j in range(width):
            if row_set[j] == 0:
                row_set[j] = counter
                counter += 1
        # Создание правых границ
        for j in range(width - 1):
            right_wall = random.randint(0, 1)
            if right_wall == 1 or row_set[j] == row_set[j + 1]:
                maze[i * 2 + 1][j * 2 + 2] = "1"
            else:
                changing_set = row_set[j + 1]
                for k in range(width):
                    if row_set[k] == changing_set:
                        row_set[k] = row_set[j]
        # Создание нижних границ
        for j in range(width):
            down_wall = random.randint(0, 1)
            count_current_set = sum(
                row_set[k] == row_set[j] for k in range(width))
            if down_wall == 1 and count_current_set != 1:
                maze[i * 2 + 2][j * 2 + 1] = "1"
        if i != height - 1:
            for j in range(width):
                count_hole = sum(
                    maze[i * 2 + 2][k * 2 + 1] == "0" and row_set[k] ==
                    row_set[j]
                    for k in range(width)
                )
                if count_hole == 0:
                    maze[i * 2 + 2][j * 2 + 1] = "0"
            for j in range(width):
                if maze[i * 2 + 2][j * 2 + 1] == "1":
                    row_set[j] = 0
    for j in range(width - 1):
        if row_set[j] != row_set[j + 1]:
            maze[-2][j * 2 + 2] = "0"
    return maze


def maze_solution(maze: list) -> list:
    """
    Решение лабиринта при помощи алгоритма Дейкстры
    :param maze: матрица лабиринта
    :return: список точек
    """
    # Начальная и конечная точки
    start = (1, 1)
    end = (len(maze) - 2, len(maze[0]) - 2)

    # Направления движения (вправо, влево, вниз, вверх)
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    # Словарь с расстояниями до каждой точки
    distances = {pos: float('inf') for pos in
                 [(i, j) for i in range(len(maze)) for j in
                  range(len(maze[0]))]}
    distances[start] = 0

    # Очередь для хранения точек и расстояний до них
    queue = [(0, start)]

    while queue:
        dist, current = heapq.heappop(queue)
        if current == end:  # Поиск кратчайшего пути
            path = [end]  # Хранит точки пути в обратном порядке
            while path[-1] != start:
                for dx, dy in directions:
                    nx, ny = path[-1][0] + dx, path[-1][1] + dy

                    if 0 <= nx < len(maze) and 0 <= ny < len(maze[0]) and \
                            maze[nx][ny] != '1':
                        if distances[path[-1]] - 1 == distances[(nx, ny)]:
                            path.append((nx, ny))
                            break
            return path[::-1]  # Путь от начала до конца

        for dx, dy in directions:
            nx, ny = current[0] + dx, current[1] + dy
            new_distance = dist + 1  # Расстояние до соседа

            if 0 <= nx < len(maze) and 0 <= ny < len(maze[0]) and \
                    maze[nx][ny] != '1':
                if new_distance < distances[(nx, ny)]:
                    # обновляем кратчайшее расстояние
                    distances[(nx, ny)] = new_distance
                    heapq.heappush(queue, (new_distance, (nx, ny)))
    return []


def print_maze(maze: list, name: str):
    print(name)
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            print(maze[i][j], end=' ')
        print()


def start_maze(width: int, height: int, solution: bool, load: str,
               save_image: str, save_text: str, speed: int):
    if load:
        maze = files.reading_maze_from_text(load)
        if not maze:
            print('Wrong maze in file!')
            return ()
    else:
        maze = maze_generation(width, height)
    print_maze(maze, "Generated maze:")

    path = []
    if solution:
        path = maze_solution(maze)
        if path:
            print("Maze solution:")
            print(path)
        else:
            print("Maze hasn't solution")
            solution = False
    screen = visualisation.start_visualization(maze, path, speed)
    files.save_maze(screen, maze, save_image, save_text)

# Тестовые значения
# a = maze_generation(4, 4)
# print_maze(a, "Generated maze:")
# print(maze_solution(a))
