import os
from typing import List
import pygame as pg


def reading_maze_from_text(path_to_file: str) -> List[List[str]]:
    """
    Функция считывает лабиринт из текстового файла и
    возвращает его в виде списка списков строк.

    :param path_to_file: Путь к текстовому файлу с лабиринтом.
    :return: Список списков строк, представляющий лабиринт.
    """
    maze = []
    with open(path_to_file, "r", encoding="utf-8") as file:
        for line in file:
            if line.strip():
                if all(el in ('0', '1') for el in line.strip()):
                    maze.append(list(line.strip()))
                else:
                    print('File with maze can contain only spaces, 1 and 0!')
                    return []

    try:
        # Проверка на наличие границ
        # Проверка на наличие входной и выходной точек
        i = 0
        while i > -2:
            if all(maze[i][j] == '1' for j in range(len(maze[i]))):
                if all(maze[j][i] == '1' for j in range(len(maze))):
                    if maze[1][1] == '0' and maze[-2][-2] == '0':
                        i -= 1
                        continue
                    else:
                        print('First cell and end cell must be free!')
                else:
                    print('File with maze must have borders!')
            else:
                print('File with maze must have borders!')
            raise IndexError

        # Проверка на одно и то же количество всех столбцов
        # Проверка на попадание в диапазон возможных рядов/столбцов
        if 3 <= len(maze[0]) - 2 <= 200 and 3 <= len(maze) - 2 <= 200:
            flag = 1
            for i in range(len(maze)):
                flag = 1 if len(maze[i]) == len(maze[0]) else 0
            else:
                print('There are different number of items in rows!')

            if flag:
                print('Loading was successfully')
                return maze
        else:
            print('Width and height must be between 3 '
                  'and 200 (excluding boundary)!')
    except IndexError:
        pass
    return []


def save_maze(
        screen: pg.Surface, maze: List[List[str]], save_image: str,
        save_text: str) -> None:
    """
    Функция сохраняет изображение и текстовое представление лабиринта.
    :param screen: Экран pygame.
    :param maze: Список списков строк, представляющий лабиринт.
    :param image: Путь для сохранения изображения лабиринта.
    :param text: Путь для сохранения текстового представления лабиринта.
    """
    current_path = os.getcwd()
    # счетчик для сохранения
    count = 1

    if save_image:
        while os.path.exists(os.path.join('save_images', save_image)):
            count += 1
            save_image = save_image.split('.')[0].split(' ')[
                             0] + ' ' + str(count) + '.' + save_image.split('.')[1]
        pg.image.save(screen, os.path.join('save_images', save_image))
        print(f"Изображение сохранено в 'save_images/{save_image}'")

    count = 1
    if save_text:
        while os.path.exists(os.path.join('save_text', save_text)):
            count += 1
            save_text = save_text.split('.')[0].split(' ')[
                            0] + ' ' + str(count) + '.' + save_text.split('.')[1]
        with open(os.path.join("save_text", save_text), "w",
                  encoding="utf-8") as file:
            for row in maze:
                file.write("".join(row) + "\r\n")
        print(f"Текст сохранен в 'maze_text/{save_text}'")
