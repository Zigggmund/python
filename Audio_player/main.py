"""
Харитонов Дмитрий КИ22-17/1Б

В данном модуле созданы все методы для работы с аудиоплеером.

Также создан GUI плеера и есть методы для работы с JSON-файлом.

JSON-фал сохраняет в себе все плейлисты после выхода из программы,
также он хранит название последнего плейлиста, который был запущен.

Рализована работа с потоками через threading,
что необходимо для корректной работы плеера.
"""

import os
import json
import threading
import shutil  # работа с копированием файлов
import time
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, simpledialog
import pygame
from PIL import Image, ImageTk  # Изменение размеров картинок
from mutagen.mp3 import MP3  # для отслеживания длительности треков
from Composition import Composition
from PlayList import PlayList
from LinkedList import LinkedListItem
from App import App


def progress():
    """
    Метод отвечает за работу progressbar
    """
    if len(app.playlist) >= 1:  # для повторного выбора плейлиста
        current_time = pygame.mixer.music.get_pos() / 1000
        c_song = MP3(app.playlist.current.data.path)
        song_len = c_song.info.length
        converted_ct = time.strftime('%M:%S', time.gmtime(current_time))
        converted_sl = time.strftime('%M:%S', time.gmtime(song_len))
        if converted_ct == '59:59':
            converted_ct = '00:00'
        frame_progress.config(text=f'Время: {converted_ct} из {converted_sl}')
        progressbar.config(maximum=song_len - 1)
        progressbar.config(value=int(current_time))
        app.is_progress = progressbar.after(100, progress)


def activate_thread():
    """
    Метод перезапускает второй поток для воспроизведения музыки
    """
    print(f"Число активных потоков в данный момент:"
          f" {threading.active_count()}")
    if threading.active_count() == 2:
        app.is_thread = False
        app.thread_play.join()
        app.thread_play = (
            threading.Thread(target=play_all, daemon=True))


def create_btn(command, image, size, row, column, name):
    """
    Метод создает кнопку по заданным параметрам
    """
    buts = []
    if len(buttons) > 2:
        for button in buttons:
            if button.grid_info()['column'] == column:
                buts.append(button)
        for button in buts:
            buttons.remove(button)

    image = Image.open("images/" + image)
    new_image = ImageTk.PhotoImage(image.resize((size, size)))
    images[name] = new_image
    btn = tk.Button(frame_buttons, command=command, image=images[name],
                    activebackground='orange')
    btn.grid(row=row, column=column, padx=35)
    return btn


def rewrite(*args):
    """
    Метод для удобного вызова функций
    rewrite_json, rewrite_screen
    :param args: tuple, перезаписываемые элементы
    """

    def rewrite_json():
        """
        Метод записывает данные с playlist и сохраняет в json-файл
        """
        with open(os.path.join(current_dir, 'music', 'player_list.json'),
                  "w", encoding="utf-8") as file:
            player_list_json = []
            for playlist_ in app.player_list:
                songs = []
                for music in playlist_:
                    songs.append(os.path.basename(music.data.path))
                player_list_json.append(
                    {"name": playlist_.name, "songs": songs})
            to_json = {"player_list": player_list_json,
                       "current_playlist_name": app.playlist.name}
            json.dump(to_json, file, indent=4)

    def rewrite_screen():
        """
        Метод записывает треки в Listbox и выводит их на экран
        """
        box_songs.delete(0, tk.END)
        if not app.is_playlist_delete:
            for c_song in app.playlist:
                box_songs.insert(tk.END,
                                 os.path.basename(c_song.data.path))
        else:
            for c_playlist in app.player_list:
                box_songs.insert(tk.END,
                                 c_playlist.name)

    if "json" in args:
        rewrite_json()
    if "screen" in args:
        rewrite_screen()


def interact_play_buttons(status):
    """
    Данный метод блокирует или разблокировывает кнопки для нажатий
    :param status: состояние кнопки - отключена или включена
    """
    for button in buttons:
        button.config(state=status)


def play_all():
    """
    Метод начинает проигрывание музыки с текущего трека
    """
    if not app.is_progress:
        progress()
    buttons.append(create_btn(pause, "pause.png", 90, 0, 1, "pause"))
    app.is_thread = True
    pygame.mixer.music.load(app.playlist.current.data.path)
    pygame.mixer.music.play()
    while (pygame.mixer.music.get_busy() or app.is_pause) and app.is_thread:
        pygame.time.Clock().tick(5)
    if app.is_thread:
        app.is_progress = None
        highlight_next()
        if len(app.playlist) > 1:
            app.playlist.current = app.playlist.current.next_item
        play_all()


def on_click():
    """
    Метод активируется при нажатии на трек/плейлист
    при is_delete = False трек проигрывается, в противном случае - удаляется
    при is_playlist_delete = True удаляется плейлист
    """
    if app.is_playlist_delete:  # удаление плейлиста
        playlist_name = box_songs.get(box_songs.curselection())
        for c_playlist in app.player_list:
            if c_playlist.name == playlist_name:
                if app.playlist.name == playlist_name:
                    print(
                        "Вы не можете удалить плейлист, который сейчас выбран")
                else:
                    app.player_list.remove(c_playlist)
                    rewrite('json', 'screen')
                if len(app.player_list) <= 1:
                    print("Слишком мало плейлистов; удаление невозможно")
                break
        return
    if not app.is_delete:  # добавление песни
        if box_songs.size() == 0:
            print("В этом плейлисте нет элементов")
        else:
            for c_song in app.playlist:
                song_path = os.path.join(current_dir, "music", box_songs.get(
                    box_songs.curselection()))
                if c_song.data.path == song_path:
                    app.playlist.current = c_song
            activate_thread()
            app.thread_play.start()
        return
    # удаление песни
    file_path = box_songs.get(box_songs.curselection())
    final_file_path = os.path.join(current_dir, "music", file_path)
    app.playlist.remove(Composition(final_file_path))
    rewrite("json", "screen")
    if len(app.playlist) == 0:
        print("Нет песен, которые можно удалить")
        exit_to_play()


def next_track():
    """
    Метод переключает на следующую композицию
    """
    highlight_next()
    if len(app.playlist) > 1:
        app.playlist.current = app.playlist.current.next_item
    else:
        print("Невозможно выполнить переход: 1 элемент в списке")
    activate_thread()
    app.thread_play.start()


def highlight_next():
    """
    Метод перемещает выделение на следующую композицию
    """
    for curselection in box_songs.curselection():
        if (app.playlist.current.data.path ==
                os.path.join(current_dir,
                             "music", box_songs.get(curselection))):
            box_songs.selection_clear(0, tk.END)
            if curselection + 1 >= len(app.playlist):
                box_songs.select_set(0)
            else:
                box_songs.select_set(curselection + 1)


def prev_track():
    """
    Метод переключает на предыдущую композицию и выделяет ее
    """
    for curselection in box_songs.curselection():
        if (app.playlist.current.data.path ==
                os.path.join(current_dir,
                             "music", box_songs.get(curselection))):
            box_songs.select_clear(0, tk.END)
            if curselection - 1 < 0:
                box_songs.select_set(len(app.playlist) - 1)
            else:
                box_songs.select_set(curselection - 1)

    if len(app.playlist) > 1:
        app.playlist.current = app.playlist.current.previous_item
    else:
        print("Невозможно выполнить переход: 1 элемент в списке")
    activate_thread()
    app.thread_play.start()


def stop():
    """
    Метод для полной остановки проигрывания музыки
    """
    frame_progress.config(text="Время: 00:00 из 00:00")
    app.is_progress = False
    pygame.mixer.music.stop()
    activate_thread()
    buttons.append(
        create_btn(lambda: app.thread_play.start(), "play.png", 90, 0, 1,
                   "play"))
    interact_play_buttons("disabled")


def pause():
    """
    Метод ставит воспроизведение музыки на паузу
    """
    progressbar.stop()

    app.is_pause = True
    pygame.mixer.music.pause()
    buttons.append(
        create_btn(unpause, "play.png", 90,
                   0, 1, "play"))


def unpause():
    """
    Метод начинает воспроизведение после паузы
    """
    app.is_pause = False
    pygame.mixer.music.unpause()
    buttons.append(create_btn(pause, "pause.png", 90, 0, 1, "pause"))


def exit_to_play():
    """
    Метод выходит из выполнения команды меню и
    возвращает стандартное расположение кнопок
    """
    buttons.append(
        create_btn(lambda: app.thread_play.start(), "play.png", 90, 0, 1,
                   "play"))
    if app.is_playlist_delete:
        app.is_playlist_delete = False
        rewrite('screen')
    if app.is_delete:
        box_songs.bind("<<ListboxSelect>>", lambda event: on_click())
        buttons.append(
            create_btn(prev_track, "back.png", 60, 0, 0, "back"))
        buttons.append(
            create_btn(next_track, "next.png", 60, 0, 2, "next"))
    interact_play_buttons("disabled")
    app.is_delete = False
    if len(app.playlist) >= 1:
        interact_play_buttons("normal")
        box_songs.select_set(0)
        app.playlist.current = app.playlist.first_item
    info_text.config(text="Вы находитесь в режиме воспроизведения. \n"
                          f"Текущий плейлист - {app.playlist.name}""\n"
                          "Чтобы выбрать действие нажмите на меню")
    menubar.entryconfig("Меню", state="normal")
    box_songs.selection_clear(0, tk.END)
    box_songs.select_set(0)


def create_playlist():
    """
    Метод для создания плейлиста
    """
    stop()
    playlist_name = simpledialog.askstring(
        "Введите данные", "Введите название плейлиста, который хотите создать")
    if playlist_name and (
            playlist_name not in [c_playlist.name for c_playlist in
                                  app.player_list]):
        app.player_list.append(PlayList(playlist_name))
        rewrite("json")
    elif not playlist_name:
        print("Имя не должно быть пустым; плейлист не создан")
    else:
        print("Плейлист с таким именем уже есть; плейлист не создан")
    if len(app.playlist) > 0:
        interact_play_buttons("normal")


def open_playlist():
    """
    Метод для открытия выбранного плейлиста
    """
    play_name = box_songs.get(box_songs.curselection())
    for c_playlist in app.player_list:
        if c_playlist.name == play_name:
            app.playlist = c_playlist
            break
    box_songs.bind("<<ListboxSelect>>", lambda event: on_click())
    rewrite("json", "screen")
    exit_to_play()


def del_playlist():
    """
    Метод для удаления плейлиста
    """
    if len(app.player_list) <= 1:
        print("Слишком мало плейлистов; удаление невозможно")
        exit_to_play()
        return
    stop()
    app.is_playlist_delete = True
    interact_play_buttons('disabled')
    menubar.entryconfig("Меню", state="disabled")
    info_text.config(text="Вы находитесь в режиме удаления плейлистов \n"
                          "Чтобы удалить плейлист, нажмите на него. \n"
                          "Чтобы перейти в обычный режим нажмите на кнопку "
                          "ниже")
    buttons.append(
        create_btn(exit_to_play, "exit.jpg", 90,
                   0, 1, "exit"))
    box_songs.delete(0, tk.END)
    rewrite("screen")


def choose_playlist():
    """
    Метод для выбора плейлиста
    """
    if len(app.player_list) <= 1:
        print("Слишком мало плейлистов; выбор невозможен")
        return
    stop()
    interact_play_buttons('disabled')
    menubar.entryconfig("Меню", state="disabled")
    info_text.config(text="Вы находитесь в режиме выбора плейлистов \n"
                          "Чтобы выбрать плейлист, нажмите на него. \n")
    box_songs.delete(0, tk.END)
    for c_playlist in app.player_list:
        box_songs.insert(tk.END,
                         c_playlist.name)

    box_songs.bind("<<ListboxSelect>>", lambda event: open_playlist())


def add_song():
    """
    Метод добавляет новую песню в плейлист
    """
    file_path = filedialog.askopenfilename(
        initialdir=os.path.join(current_dir, "music"),
        filetypes=[("mp3 Files", "*.mp3")])
    if file_path:
        right_path = os.path.join(current_dir,
                                  "music", os.path.basename(file_path))
        if not os.path.exists(file_path):
            shutil.copy(file_path, right_path)
        if Composition(right_path) not in app.playlist:
            stop()
            app.playlist.append(LinkedListItem(Composition(right_path)))
            app.playlist.current = app.playlist.first_item
            rewrite("json", "screen")
            if len(app.playlist) == 1:
                interact_play_buttons("normal")
            box_songs.select_set(0)
            exit_to_play()
        else:
            print("Такая песня уже есть в плейлисте")


def del_song():
    """
    Метод включает режим удаления элементов
    """
    if len(app.playlist) == 0:
        print("Нет песен, которые можно удалить")
        return
    stop()
    app.is_delete = True
    interact_play_buttons('disabled')
    menubar.entryconfig("Меню", state="disabled")
    info_text.config(text="Вы находитесь в режиме удаления песен \n"
                          "Чтобы удалить песню, нажмите по ней. \n"
                          "Чтобы перейти в обычный режим нажмите на кнопку "
                          "ниже")
    buttons.append(
        create_btn(exit_to_play, "exit.jpg", 90,
                   0, 1, "exit"))


def change_order():
    """
    Метод включает режим перестановки элементов
    """
    if len(app.playlist) <= 1:
        print("Слишком мало песен для перестановки")
        return
    stop()
    app.is_delete = True  # для обработки выхода  в обычный режим
    buttons.append(
        create_btn(exit_to_play, "exit.jpg", 90,
                   0, 1, "exit"))
    buttons.append(
        create_btn(move_up, "back.png", 60, 0, 0, "move_up"))
    buttons.append(
        create_btn(move_down, "next.png", 60, 0, 2, "move_down"))
    menubar.entryconfig("Меню", state="disabled")
    info_text.config(text="Вы находитесь в режиме перестановки песен \n"
                          "Нажмите левую кнопку чтобы поменять песню \n"
                          "предыдущей, правую - со следующей\n"
                          "Чтобы перейти в обычный режим нажмите на кнопку "
                          "ниже")
    box_songs.bind("<<ListboxSelect>>", lambda event: change_order())


def move_up():
    """
    Метод для перестановки песни с предыдущей перед ней
    """
    file_path = box_songs.get(box_songs.curselection())
    final_file_path = os.path.join(current_dir, "music", file_path)
    if final_file_path not in (app.playlist[0].path, app.playlist[1].path):
        for i, c_song in enumerate(app.playlist):
            if c_song.data.path == final_file_path:
                app.playlist.remove(Composition(final_file_path))
                app.playlist.insert(app.playlist[i - 2], LinkedListItem(
                    Composition(final_file_path)))
                rewrite("json", "screen")
                box_songs.select_clear(0, tk.END)
                box_songs.select_set(i - 1)
                break
    elif app.playlist[1].path == final_file_path:
        app.playlist.remove(Composition(final_file_path))
        app.playlist.append_left(
            LinkedListItem(Composition(final_file_path)))
        rewrite("json", "screen")
        box_songs.select_clear(0, tk.END)
        box_songs.select_set(0)
    else:
        print("Элемент находится на самом верху, перемещение не выполнено")


def move_down():
    """
    Метод для перестановки песни со следующей за ней
    """
    file_path = box_songs.get(box_songs.curselection())
    final_file_path = os.path.join(current_dir, "music", file_path)
    if final_file_path not in (app.playlist[len(app.playlist) - 2].path,
                               app.playlist[len(app.playlist) - 1].path):
        for i, c_song in enumerate(app.playlist):
            if c_song.data.path == final_file_path:
                app.playlist.remove(Composition(final_file_path))
                app.playlist.insert(app.playlist[i], LinkedListItem(
                    Composition(final_file_path)))
                rewrite("json", "screen")
                box_songs.select_clear(0, tk.END)
                box_songs.select_set(i + 1)
                break
    elif app.playlist[len(app.playlist) - 2].path == final_file_path:
        app.playlist.remove(Composition(final_file_path))
        app.playlist.append_right(
            LinkedListItem(Composition(final_file_path)))
        rewrite("json", "screen")
        box_songs.select_clear(0, tk.END)
        box_songs.select_set(len(app.playlist) - 1)
    else:
        print("Элемент находится в самом низу, перемещение не выполнено")


if __name__ == "__main__":
    # объявление основных переменных
    images = {}  # необходимо для правильного вывода на экран картинок
    buttons = []
    app = App()
    app.thread_play = threading.Thread(target=play_all, daemon=True)
    app.playlist = PlayList()
    pygame.mixer.init()
    current_dir = os.getcwd()

    # создание окна
    root = tk.Tk()
    root['bg'] = 'black'
    root.title("Audioplayer")
    root.geometry("500x570")
    root.resizable(width=False, height=False)

    # загрузка json-файла
    with open(os.path.join(current_dir, 'music', 'player_list.json'),
              "r", encoding="utf-8") as json_file:
        json_list = json.load(json_file)
        app.playlist.name = json_list["current_playlist_name"]
        player_list = json_list["player_list"]
        for playlist in player_list:
            if playlist["name"] == app.playlist.name:
                for song in playlist['songs']:
                    app.playlist.append(LinkedListItem(
                        Composition(
                            os.path.join(current_dir, "music", song))))
                app.player_list.append(app.playlist)
            else:
                cur_playlist = PlayList(playlist["name"])
                for song in playlist['songs']:
                    cur_playlist.append(LinkedListItem(
                        Composition(
                            os.path.join(current_dir, "music", song))))
                app.player_list.append(cur_playlist)

    # создание фреймов
    box_songs = tk.Listbox(root, height=13, width=75, fg='#FFA500',
                           font=("Times_new_roman", 12), background="#292929",
                           selectbackground="gray", selectforeground="white",
                           justify='center', selectmode=tk.SINGLE)
    box_songs.pack(padx=25, pady=10, expand=False)
    frame_progress = tk.LabelFrame(root, text="Здесь будет время",
                                   labelanchor='n', height=60, width=450,
                                   fg="#FFA500", background="#292929")
    frame_progress.pack(pady=10, padx=0)
    frame_progress.pack_propagate(False)
    frame_text = tk.LabelFrame(root, height=80, width=450,
                               background="#292929")
    frame_text.pack(pady=10, padx=0)
    frame_text.pack_propagate(False)
    frame_buttons = tk.LabelFrame(root, height=110, width=450,
                                  background="#292929")
    frame_buttons.pack(padx=0, pady=5)
    frame_buttons.grid_propagate(False)

    # создание кнопок
    info_text = ttk.Label(frame_text, font=("Times_new_roman", 11, 'bold'),
                          anchor="center", justify="center",
                          text="Вы находитесь в режиме воспроизведения. \n"
                               f"Текущий плейлист - {app.playlist.name}""\n"
                               "Чтобы выбрать действие нажмите на меню",
                          background="", foreground="#FFA500")
    info_text.pack()
    progressbar = ttk.Progressbar(frame_progress, orient='horizontal',
                                  length=400,
                                  mode="determinate", value=-1)
    progressbar.pack(padx=0, pady=4, ipady=5)
    buttons.append(
        create_btn(prev_track, "back.png", 60, 0, 0, "back"))
    buttons.append(
        create_btn(lambda: app.thread_play.start(), "play.png", 90,
                   0, 1, "play"))
    buttons.append(
        create_btn(next_track, "next.png", 60, 0, 2, "next"))

    box_songs.bind("<<ListboxSelect>>", lambda event: on_click())

    # создание меню
    menubar = tk.Menu(root)
    root.config(menu=menubar)
    org_menu = tk.Menu(menubar, tearoff=False)
    menubar.add_cascade(label="Меню", menu=org_menu)
    org_menu.add_command(label='Выбрать плейлист', command=choose_playlist)
    org_menu.add_command(label='Создать плейлист', command=create_playlist)
    org_menu.add_command(label='Удалить плейлисты', command=del_playlist)
    org_menu.add_command(label='Добавить песню', command=add_song)
    org_menu.add_command(label='Удалить песни', command=del_song)
    org_menu.add_command(label='Изменить порядок песен',
                         command=change_order)

    rewrite("playlist", "screen")
    app.playlist.current = app.playlist.first_item
    if len(app.playlist) == 0:
        interact_play_buttons("disabled")
    else:
        box_songs.select_set(0)

    root.mainloop()
