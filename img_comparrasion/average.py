"""
Модуль, содержащий методы для подсчета средних значений
"""

from typing import List, Tuple


def weighted_average(hist: List[int]) -> Tuple[int, float]:
    """
    Возвращает взвешенное среднее значение цвета и
    ошибку из гистограммы пикселей
    :param hist: Список количества пикселей для каждого диапазона
    :return: Взвешенное среднее значение цвета и ошибку
    """
    total = sum(hist)
    value, error = 0, 0
    if total > 0:
        # Формула для взвешенного среднего значения:
        # умножение каждого значения на его вес,
        # а затем деление общего произведения на количество пикселей
        value = sum(i * x for i, x in enumerate(hist)) / total
        # Формула для ошибки:
        # среднеквадратичное отклонение каждого значения от
        # взвешенного среднего
        error = sum(x * (value - i) ** 2 for i, x in enumerate(hist)) / total
        error **= 0.5
    return value, error


def color_average(hist: List[int]) -> Tuple[Tuple[int, int, int], float]:
    """
    Возвращает средний цвет RGB из заданной гистограммы
    количества цветов пикселей
    :param hist: Список количества пикселей для каждого диапазона
    :return: Cредний цвет и ошибку
    """
    red, red_error = weighted_average(hist[:256])
    green, green_error = weighted_average(hist[256:512])
    blue, blue_error = weighted_average(hist[512:768])
    error = red_error * 0.2989 + green_error * 0.5870 + blue_error * 0.1140
    return (int(red), int(green), int(blue)), error
