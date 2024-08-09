"""
Модуль, во котором представлены методы для работы с
параметрами, заданными пользователем
"""

import os.path


def check_args(args):
    """
    Метод для проверки параметров, заданных пользователем
    """
    if not os.path.exists(args["image"]):
        print("Файл не найден!")
        return ()

    if not (args["image"].split('.')[-1] in ("png", "jpg", "jpeg")):
        print("Недопустимое расширение (допустимые - png, jpg, jpeg)!")
        return ()

    if not args["level"] in range(0, 9):
        if args["level"]:
            print("Значение уровня сжатия должно быть числом от 0 до 8!")
        print("Уровень сжатия автоматически задан как 8")
        args["level"] = 8

    return args["image"], args["level"], args["gif"], args["borders"]
