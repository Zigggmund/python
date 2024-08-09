"""
Модуль хранит в себе класс Composition
"""


class Composition:
    """
    Класс содержит в себе
    path - путь до композиции, а также
    метод __eq__ для сравнения двух элементов
    метод __str__ для преобразования элемента в строку
    """

    def __init__(self, path):
        self.path = path

    def __eq__(self, other):
        if isinstance(other, Composition):
            return self.path == other.path
        return False

    def __str__(self):
        return f'{self.path}'
