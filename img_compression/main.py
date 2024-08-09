import argparse
import params
import images

# пример вызова
# python main.py -i images\cat.jpg -b -l 4
# python main.py -i images\cat.jpg -l 2 -g

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", '--image', type=str,
                        help="Путь до изображения", required=True)
    parser.add_argument("-l", '--level', type=int,
                        help="Уровень сжатия")
    parser.add_argument("-g", '--gif', action="store_true",
                        help="Создать gif-изображение")
    parser.add_argument("-b", '--borders', action="store_true",
                        help="Отобразить границы")
    args = vars(parser.parse_args())

    args = params.check_args(args)
    if args:
        images.start(args[0], args[1], args[2], args[3])
    else:
        print("Сжатие не выполнено")
    print("Выполнение программы завершено")
