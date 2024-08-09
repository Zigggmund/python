"""
Модуль хранит в себе класс App
"""


class App:
    """
    Класс содержит основные поля, необходимые
    для работы приложения
    """
    thread_flag = False
    is_pause = False
    is_progress = False
    is_delete = False
    is_playlist_delete = False

    thread_play = None
    player_list = []
    playlist = None
