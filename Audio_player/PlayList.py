"""
Модуль содержит класс PlayList
"""
from LinkedList import LinkedList


class PlayList(LinkedList):
    """
    Класс наследуется от класса LinkedList, содержит в себе
    current_item - текущий трек
    name - название плейлиста
    метод __eq__ для сравнения элементов
    """

    def __init__(self, name='No name'):
        super().__init__()
        self.current_item = None
        self.name = name

    @property
    def current(self):
        """
        Геттер для current
        :return: current_item
        """
        return self.current_item

    @current.setter
    def current(self, current_item):
        self.current_item = current_item

    def __eq__(self, other):
        if isinstance(other, PlayList):
            return self.name == other.name
        return False
