import os.path
from typing import List, Tuple

import pygame as pg

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
TURQ = (64, 224, 208)


def start_visualization(
        maze: List[List[str]], solution: List[Tuple[int, int]],
        speed: int) -> pg.Surface:
    """
    Функция запускает визуализацию лабиринта и решения.

    :param maze: Список списков строк, представляющий лабиринт.
    :param solution: Список кортежей из двух элементов, представляющих координаты точек на
    пути от начальной до конечной точки.
    :param save_image: Флаг, указывающий на необходимость сохранения изображения лабиринта.
    :param save_text: Флаг, указывающий на необходимость сохранения текстового представления лабиринта.
    """
    # создание окна
    pg.init()
    width = len(maze[0])
    height = len(maze)

    scale = 600 // height if height >= width else 800 // width
    screen = pg.display.set_mode((width * scale, height * scale))

    visualize_maze(screen, maze, scale)
    if solution:
        visualize_solution(screen, solution, scale, speed)

    # нужно, чтобы окно не закрывалось после прохождения
    solving = True
    while solving:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                solving = False
    return screen


def visualize_maze(screen: pg.Surface, maze: List[List[str]],
                   scale: int) -> None:
    """
    Функция визуализирует лабиринт на экране.

    :param screen: Экран pygame.
    :param maze: Список списков строк, представляющий лабиринт.
    :param scale: Масштаб отображения лабиринта.
    """
    # нужно для определения координат финиша
    end_coord = 0

    for i in range(len(maze)):
        for j in range(len(maze[i])):
            if maze[i][j] == "1":
                pg.draw.rect(screen, BLACK,
                             (j * scale, i * scale, scale, scale))
            else:
                pg.draw.rect(screen, WHITE,
                             (j * scale, i * scale, scale, scale))
                end_coord = j * scale + scale // 4, i * scale + scale // 4

    # рисование старта и финиша
    start_image = pg.image.load(
        os.path.join('icons', 'start.png')).convert_alpha()
    finish_image = pg.image.load(
        os.path.join('icons', 'finish.png')).convert_alpha()
    start_image = pg.transform.scale(start_image, (scale, scale))
    finish_image = pg.transform.scale(finish_image, (scale // 2, scale // 2))
    screen.blit(start_image, (scale, scale))
    screen.blit(finish_image, end_coord)

    # обновление экрана
    pg.display.flip()


def visualize_solution(screen: pg.Surface, solution: List[Tuple[int, int]],
                       scale: int, speed: int) -> None:
    """
    Функция визуализирует решение лабиринта на экране.

    :param screen: Экран pygame.
    :param solution: Список кортежей из двух элементов, представляющих координаты точек на пути от
    начальной до конечной точки.
    :param scale: Масштаб отображения лабиринта.
    """
    # нужно для определения координат финиша
    end_coord = 0
    start_flag = 0

    for point in solution:
        pg.display.flip()
        pg.time.wait(110 - speed)

        pg.draw.rect(screen, TURQ,
                     (point[1] * scale, point[0] * scale, scale, scale))

        end_coord = point[1] * scale + scale // 4, point[
            0] * scale + scale // 4
        if not start_flag:  # рисование старта
            start_flag = 1
            start_image = pg.image.load(
                os.path.join('icons', 'start.png')).convert_alpha()
            start_image = pg.transform.scale(start_image, (scale, scale))
            screen.blit(start_image, (scale, scale))

    # рисование финиша
    finish_image = pg.image.load(
        os.path.join('icons', 'finish.png')).convert_alpha()
    finish_image = pg.transform.scale(finish_image, (scale // 2, scale // 2))
    screen.blit(finish_image, end_coord)
    pg.display.flip()
