"""
Реализация квадродерева через 3 класса
"""

import average
import threading
from typing import Optional, Tuple, List, Union
from PIL import Image

MAX_DEPTH = 8  # Максимальная глубина узла


class Point:
    """Класс точки"""

    def __init__(self, x_coordinate: float, y_coordinate: float) -> None:
        """
        Конструктор точки
        :param x_coordinate: Координата x
        :param y_coordinate: Координата y
        """
        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate

    def __repr__(self) -> str:
        """
        Строковое представление точки
        :return: Cтроковое представление точки
        """
        return f"Точка с координатами " \
               f"({self.x_coordinate}, {self.y_coordinate})"

    def __eq__(self, another: "Point") -> bool:
        """
        Сравнение 2 точек
        :param another: Точка для сравнения
        :return: Результат сравнения
        """
        return self.x_coordinate == another.y_coordinate and \
            self.y_coordinate == another.y_coordinate


class QuadtreeNode:
    """
    Класс узла квадродерева
    """

    def __init__(self, image: Image,
                 coordinate_region: Tuple[float, float, float, float],
                 depth: int) -> None:
        """
        Конструктор узла квадродерева
        :param image: Изображение
        :param coordinate_region: Координатная область
        :param depth: Глубина
        """
        # дочерние узлы
        self.__children = None
        # Узел является листом?
        self.__is_leaf = False
        # точки узла
        self.node_points = []
        # координаты граничных точек
        self.__coordinate_region = coordinate_region
        # глубина
        self.__depth = depth

        left_right = self.__coordinate_region[0] + (
                self.__coordinate_region[2] - self.__coordinate_region[0]) / 2
        top_bottom = self.__coordinate_region[1] + (
                self.__coordinate_region[3] - self.__coordinate_region[1]) / 2

        # координаты центральной точки
        self.__node_center_point = Point(left_right, top_bottom)

        # Обрезка части изображения по координатам
        image = image.crop(coordinate_region)
        # histogram возвращает список количества пикселей
        # для каждого диапазона на изображении

        # цвет и ошибка
        self.__average_color, self.__error = average.color_average(
            image.histogram())

    @property
    def children(self) -> Optional[list]:
        """
        Геттер для дочерних узлов
        """
        return self.__children

    @property
    def is_leaf(self) -> bool:
        """
        Геттер для переменной "является ли узел листом или нет?"
        """
        return self.__is_leaf

    @is_leaf.setter
    def is_leaf(self, value: bool) -> None:
        """
        Сеттер для переменной "является ли узел листом или нет?"
        """
        self.__is_leaf = value

    @property
    def coordinate_region(self) -> Tuple[float, float, float, float]:
        """
        Геттер для координат граничных точек
        """
        return self.__coordinate_region

    @property
    def depth(self) -> int:
        """
        Геттер для глубины
        """
        return self.__depth

    @property
    def node_center_point(self) -> Point:
        """
        Геттер для координаты центральной точки узла
        """
        return self.__node_center_point

    @property
    def average_color(self) -> Tuple[int, int, int]:
        """
       Геттер для значения цвета
        """
        return self.__average_color

    @property
    def error(self) -> float:
        """
        Геттер для значения ошибки
        """
        return self.__error

    def __repr__(self) -> str:
        """
        Строковое представление узла
        :return: Строковое представление узла
        """
        return f"Узел дерева {self.__coordinate_region}"

    def split(self, image: Image) -> None:
        """
        Разбивает данную секцию изображения на четыре равных блока
        :param image: Изображение
        """

        left, top, right, bottom = self.__coordinate_region

        top_left = QuadtreeNode(image, (
            left, top, self.__node_center_point.x_coordinate,
            self.__node_center_point.y_coordinate),
                                self.__depth + 1)
        top_right = QuadtreeNode(image, (
            self.__node_center_point.x_coordinate, top, right,
            self.__node_center_point.y_coordinate),
                                 self.__depth + 1)
        bottom_left = QuadtreeNode(image,
                                   (left,
                                    self.__node_center_point.y_coordinate,
                                    self.__node_center_point.x_coordinate,
                                    bottom),
                                   self.__depth + 1)
        bottom_right = QuadtreeNode(image,
                                    (self.__node_center_point.x_coordinate,
                                     self.__node_center_point.y_coordinate,
                                     right, bottom),
                                    self.__depth + 1)

        self.__children = [top_left, top_right, bottom_left, bottom_right]

    def find_node(self, point, search_list: list = None) -> Tuple[
        "QuadtreeNode", Union[List["QuadtreeNode"], list]]:
        """
        Возвращает узел, содержащий точку и путь до него
        :param point: Искомая точка
        :param search_list: Cписок узлов
        :return: Узел и список узлов
        """
        if not search_list:
            search_list = []

        search_list.append(self)

        if self.children is not None:
            if point.x_coordinate < self.__node_center_point.x_coordinate:
                if point.y_coordinate < self.__node_center_point.y_coordinate:
                    if self.children[0] is not None:
                        return self.children[0].find_node(point, search_list)
                else:
                    if self.children[2] is not None:
                        return self.children[2].find_node(point, search_list)

            else:
                if point.y_coordinate < self.__node_center_point.y_coordinate:
                    if self.children[1] is not None:
                        return self.children[1].find_node(point, search_list)
                else:
                    if self.children[3] is not None:
                        return self.children[3].find_node(point, search_list)

        return self, search_list

    def find_node_by_point(self, search_point: Point) -> "QuadtreeNode":
        """
        Возвращает узел, содержащий точку
        :param search_point: Искомая точка
        :return: Необходимый узел.
        """
        return self.find_node(search_point)[0]

    def insert_point(self, point: Point):
        """
        Вставляет точку в подходящий узел
        :param point: Точка, которая должна быть вставлена
        :return: Рекурсия
        """
        if self.children is not None:
            if point.x_coordinate < self.__node_center_point.x_coordinate:
                if point.y_coordinate < self.__node_center_point.y_coordinate:
                    return self.children[0].insert_point(point)
                else:
                    self.children[2].insert_point(point)

            else:
                if point.y_coordinate < self.__node_center_point.y_coordinate:
                    return self.children[1].insert_point(point)
                else:
                    self.children[3].insert_point(point)

        self.node_points.append(point)

    def remove_point(self, delete_point: Point) -> None:
        """
        Удаляет точку
        :param delete_point: Удаляемая точка
        """
        current_node, _ = self.find_node(delete_point)

        if current_node is not None:
            for point in current_node.node_points:
                if point == delete_point:
                    current_node.node_points.remove(point)


class QuadTree:
    """Класс квадродерева"""

    def __init__(self, image: Image) -> None:
        """
        Конструктор квадродерева
        :param image: Исходное изображение
        """
        # ширина и высота соответственно
        self.__width, self.__height = image.size
        # корневой узел
        self.__root = QuadtreeNode(image, image.getbbox(), 0)
        # максимальная глубина, полученная через рекурсию
        self.__max_depth = 0

        self.__build_tree(image, self.__root)

    @property
    def width(self) -> int:
        """
        Геттер для ширины изображения
        """
        return self.__width

    @property
    def height(self) -> int:
        """
        Геттер для высоты изображения
        """
        return self.__height

    @property
    def root(self) -> QuadtreeNode:
        """
        Геттер для корневого узла
        """
        return self.__root

    @property
    def max_depth(self) -> int:
        """
        Геттер для максимальной глубины, полученной через рекурсию
        """
        return self.__max_depth

    def __build_tree(self, image: Image, node: QuadtreeNode) -> None:
        """
        Рекурсивно добавляет узлы, пока не будет достигнута макс. глубина
        :param image: Исходное изображение
        :param node: Узел
        """
        value_threshold = 13  # Порог значения

        if (node.depth >= MAX_DEPTH) or (node.error <= value_threshold):
            if node.depth > self.__max_depth:
                self.__max_depth = node.depth
            node.is_leaf = True
            return None

        threads = []
        node.split(image)

        for child in node.children:
            thread = threading.Thread(target=self.__build_tree,
                                      args=(image, child))
            thread.start()
            threads.append(thread)

        for process in threads:
            process.join()

        return None

    def get_rec_nodes(self, node: QuadtreeNode, depth: int,
                      leaf_nodes: list) -> None:
        """
        Рекурсивно получает листовые узлы в зависимости от того, является ли
        узел листом или достигнута ли заданная глубина
        :param node: Узел
        :param depth: Значение глубины
        :param leaf_nodes: Список листьев
        """
        if node.is_leaf is True or node.depth == depth:
            leaf_nodes.append(node)
        elif node.children is not None:
            for child in node.children:
                self.get_rec_nodes(child, depth, leaf_nodes)

    def get_nodes(self, depth: int) -> list:
        """
        Возвращает листья дерева
        :param depth: Значение глубины рекурсии.
        :return: Список листьев
        """

        if depth > self.__max_depth:
            raise ValueError('Дана глубина больше, чем высота деревьев')

        leaf_nodes = []
        self.get_rec_nodes(self.__root, depth, leaf_nodes)
        return leaf_nodes
