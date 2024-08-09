"""
Модуль, во котором представлены методы для работы с
параметрами, заданными пользователем
"""

import os.path


def check_args(args):
    """
    Метод для проверки параметров, заданных пользователем
    """
    loaded = 0  # Загружен ли лабиринт с файла

    if args["load"]:
        if os.path.exists(args["load"]):
            if args["load"].split('.')[-1] == 'txt':
                loaded = 1
            else:
                print('File with maze has a wrong extension '
                      '(available - txt)!')
        else:
            print("File with maze not found!")

    if not loaded:
        args["load"] = None
        for i, name in enumerate(("Height", "Width")):
            if not (3 <= args["size"][i] <= 200):  # нужно изменить
                print(f"{name} must be a number from 3 to 200!")
                return ()

    if args["save_text"]:
        if len(args["save_text"].split(".")) == 2 and \
                args["save_text"].split(".")[-1] == "txt":
            pass
        else:
            print("Wrong extension (available - txt)!")
            args["save_text"] = None

    if args["save_image"]:
        if len(args["save_image"].split(".")) == 2 and \
                args["save_image"].split(".")[-1] in ("png", "jpg"):
            pass
        else:
            print("Wrong extension (available - png, jpg)!")
            args["save_image"] = None

    if args['speed']:
        if not (1 <= args['speed'] <= 10):
            print("Wrong speed: must be a number between 1 and 10")
            args['speed'] = None
    if not args['speed']:
        args['speed'] = 3
    args['speed'] *= 10

    return args['size'][0], args['size'][1], args["solution"], args["load"], \
        args["save_image"], args["save_text"], args['speed']
