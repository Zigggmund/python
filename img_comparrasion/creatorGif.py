"""
Модуль с классом CreatorGif
"""
import os


class CreatorGif:
    """
    Класс для Gif-изображений
    """

    def __init__(self, img_name: str) -> None:
        """
        Конструктор класса, который будет сохранять гиф-изображения
        """
        # кадры
        self.frames = []

        path = f"gifs\\{img_name}_gif.gif"
        # создание папки (если ее нет)
        if not os.path.exists("gifs"):
            os.mkdir("gifs")
        # удаление предыдущей гифки (если она есть)
        if os.path.exists(path):
            os.remove(path)

        self.__path = path

    @property
    def path(self):
        """
        Геттер для пути
        """
        return self.__path
