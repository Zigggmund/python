"""
Модуль для сжатия изображений
"""

from quadtree import QuadTree, MAX_DEPTH
from PIL import Image, ImageDraw
from creatorGif import CreatorGif


def create_image(quadtree: QuadTree, level: int,
                 borders: bool) -> Image:
    """
    Создает изображение
    :param quadtree: Квадродерево
    :param level: Уровень глубины
    :param borders: Отображение границ
    :return: Сжатое изображение
    """
    image = Image.new('RGB', (quadtree.width, quadtree.height))
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, quadtree.width, quadtree.height), (0, 0, 0))
    leaf_nodes = quadtree.get_nodes(level)

    for node in leaf_nodes:
        if borders:
            draw.rectangle(node.coordinate_region, node.average_color,
                           outline=(0, 0, 0))
        else:
            draw.rectangle(node.coordinate_region, node.average_color)

    return image


def create_gif(gif: CreatorGif) -> None:
    """
    Сохраняет gif-изображение
    :param gif: gif-изображение
    """
    print("Создание gif-изображения")

    gif.frames[0].save(gif.path, save_all=True,
                       append_images=gif.frames[1:],
                       optimize=True,
                       duration=800,
                       loop=1)

    print("Gif-изображение успешно сохранено")

    gif.frames[0].close()
    gif.frames = []


def start(image: str, level: int, gif: bool, borders: bool) -> None:
    """
    Сжатие изображения
    :param image: Путь до изображения
    :param level: Уровень глубины
    :param borders: Отображение границ
    :param gif: Нужно ли создавать gif изображение
    """
    print("Создание изображения")
    original_image = Image.open(image)
    quadtree = QuadTree(original_image)

    image_name = image.split(".")[0].split("\\")[-1]
    image_extension = image.split(".")[-1]

    final_image = create_image(quadtree, level, borders)
    final_image.save(f"images\\{image_name}_quadtree.{image_extension}")
    print("Изображение успешно сохранено")

    if gif:
        gif = CreatorGif(image_name)
        for value in range(MAX_DEPTH + 1):
            gif.frames.append(create_image(quadtree, value, borders))

        create_gif(gif)
